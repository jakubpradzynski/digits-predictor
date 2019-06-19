# digits-predictor
App for bachelor thesis

### Requirements
For the proper functioning of the application, you need: 
1. Java > 8
2. Python 3
3. Pip 3
4. Maven

### Before start
Before you start, make sure you have the necessary Python libraries installed:
```bash
pip3 install tensorflow keras matplotlib scikit-learn pillow
```

### Training models
Before you run web app, you need to train ML models:
1. ANN ```python3 ann-train.py```
2. SVN ```python3 svn-train.py```

### Web app
For run web app just apply command:
```bash
mvn spring-boot:run
```