import datetime as dt
import pickle

from sklearn import svm, metrics
from sklearn.datasets import fetch_mldata
from sklearn.model_selection import train_test_split

# Load MNIST data set
mnist_data_set = fetch_mldata("MNIST original", data_home="./")

# Assign images and labels to variables
digits_images = mnist_data_set.data
digits_labels = mnist_data_set.target

# Normalize images from 0-255 to 0-1
digits_images = digits_images / 255.0

# Random split data set (85% train, 15% test)
train_images, test_images, train_labels, test_labels = train_test_split(digits_images, digits_labels, test_size=0.15,
                                                                        random_state=42)

# Set SVM classifier
param_C = 5
param_gamma = 0.05
classifier = svm.SVC(C=param_C, gamma=param_gamma, probability=True, verbose=True)

# Start learning classifier
learning_start_time = dt.datetime.now()
print("Start learning at {}".format(str(learning_start_time)))
classifier.fit(train_images, train_labels)

# End learning classifier
learning_end_time = dt.datetime.now()
print("Stop learning {}".format(str(learning_end_time)))
learning_elapsed_time = learning_end_time - learning_start_time
print("Learning time {}".format(str(learning_elapsed_time)))

# Test obtained model
predict_result_on_test_images = classifier.predict(test_images)
print("Model accuracy = {}".format(metrics.accuracy_score(test_labels, predict_result_on_test_images)))

# Save model
model_filename = "svm_model.sav"
pickle.dump(classifier, open(model_filename, "wb"))
print("SVM model saved in file: {}".format(model_filename))
