package pl.jakubpradzynski.digitspredictor;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.ResponseBody;

import javax.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.net.URISyntaxException;
import java.util.List;

@Controller
public class MainController {

    private final MainService mainService;

    public MainController(MainService mainService) {
        this.mainService = mainService;
    }

    @RequestMapping("/")
    public String start() {
        return "index.html";
    }

    @RequestMapping("/info")
    public String info() {
        return "redirect:https://github.com/jakubpradzynski/digits-predictor/blob/master/README.md";
    }

    @RequestMapping("/app")
    public String app() {
        return "app.html";
    }

    @RequestMapping("/file")
    public void generateReport(HttpServletResponse response) throws Exception {
        mainService.streamFile(response);
    }

    @RequestMapping(value = "/predict", method = RequestMethod.POST)
    @ResponseBody
    public List predict(@RequestBody String imageUrl) throws URISyntaxException, IOException {
        return mainService.predict(imageUrl);
    }

    @RequestMapping(value = "/clearHistory", method = RequestMethod.GET)
    @ResponseBody
    public void clearHistory() {
        mainService.clearHistory();
    }
}
