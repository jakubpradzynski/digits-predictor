# digits-predictor
App for bachelor thesis

### About project
The project was created as part of a BA thesis in Computer Science at the University of Nicolaus Copernicus in Toruń.

Author: Jakub Prądzyński.

The project is to present the operation of machine learning models distinguishing hand-written numbers. 
It is based on the open MNIST database. 
Contains scripts teaching models of Support Vector Machine and Artificial Neural Network. 
Access a simple GUI through the browser to be able to draw any digit yourself and check how well-trained models will manage.

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

### Using
App run on port 8080.
Available on http://locaclhost:8080