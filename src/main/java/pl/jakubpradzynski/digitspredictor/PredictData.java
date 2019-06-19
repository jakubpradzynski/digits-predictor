package pl.jakubpradzynski.digitspredictor;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import lombok.ToString;

import java.io.Serializable;

@AllArgsConstructor
@NoArgsConstructor
@Getter
@Setter
@ToString
public class PredictData implements Serializable {

    private String decodedUrl;
    private byte[] image;
    private String svmPredict;
    private String svmProbability;
    private String annPredict;
    private String annProbability;

}
