package pl.jakubpradzynski.digitspredictor;

import org.apache.tomcat.util.codec.binary.Base64;
import org.springframework.stereotype.Service;

import javax.imageio.ImageIO;
import javax.servlet.http.HttpServletResponse;
import java.awt.image.BufferedImage;
import java.io.BufferedReader;
import java.io.ByteArrayInputStream;
import java.io.File;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.URI;
import java.net.URISyntaxException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.LinkedList;
import java.util.List;

@Service
public class MainService {

    private LinkedList predicts = new LinkedList();

    void streamFile(HttpServletResponse response)
            throws IOException, URISyntaxException {
        byte[] data = Files.readAllBytes(Paths.get(getClass().getClassLoader().getResource("bachelor-thesis.pdf").toURI()));
        response.setContentType("application/pdf");
        response.setHeader("Content-disposition", "attachment; filename=" + "praca_licencjacka.pdf");
        response.setContentLength(data.length);
        response.getOutputStream().write(data);
        response.getOutputStream().flush();
    }

    List predict(String imageUrl) throws URISyntaxException, IOException {
        PredictData newPredict = new PredictData();
        String decodedUrl = new URI(imageUrl).getPath();
        newPredict.setDecodedUrl(decodedUrl);
        newPredict.setImage(base64ToByteArray(newPredict.getDecodedUrl()));
        predictInModels(newPredict);
        predicts.add(newPredict);
        return predicts;
    }

    private void predictInModels(PredictData predictData) throws IOException {
        saveImage(predictData, "predict_svm.png");
        saveImage(predictData, "predict_ann.png");
        try {
            predictFromPythonScript(predictData);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }

    private byte[] base64ToByteArray(String base64) {
        return new Base64().decode(base64.split(",")[1]);
    }

    private void saveImage(PredictData predictData, String name) throws IOException {
        BufferedImage image;
        ByteArrayInputStream bis = new ByteArrayInputStream(predictData.getImage());
        image = ImageIO.read(bis);
        bis.close();
        File outputfile = new File(name);
        ImageIO.write(image, "png", outputfile);
    }

    private void predictFromPythonScript(PredictData predictData) throws IOException, InterruptedException {
        String command = "python3 predictor.py";
        Process p = Runtime.getRuntime().exec(command);
        p.waitFor();
        BufferedReader bri = new BufferedReader(new InputStreamReader(p.getInputStream()));
        BufferedReader bre = new BufferedReader(new InputStreamReader(p.getErrorStream()));
        String line;
        while ((line = bri.readLine()) != null) {
            readResult(line, predictData);
            System.out.println(line);
        }
        bri.close();
        while ((line = bre.readLine()) != null) {
            System.out.println(line);
        }
        bre.close();
        p.waitFor();
        p.destroy();
    }

    private void readResult(String line, PredictData predictData) {
        String[] split = line.split(": ");
        if (split.length != 2) {
            System.err.println("SOMETHING WENT WRONG IN PREDICTOR.PY");
        } else {
            if (split[0].contains("SVM PREDICT")) {
                predictData.setSvmPredict(split[1]);
            } else if (split[0].contains("SVM PROBABILITY")) {
                predictData.setSvmProbability(split[1]);
            } else if (split[0].contains("ANN PREDICT")) {
                predictData.setAnnPredict(split[1]);
            } else if (split[0].contains("ANN PROBABILITY")) {
                predictData.setAnnProbability(split[1]);
            }
        }
    }

    void clearHistory() {
        predicts.clear();
    }
}
