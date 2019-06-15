import keras
from keras.datasets import mnist
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import Flatten
from keras.layers.convolutional import Conv2D
from keras.layers.convolutional import MaxPooling2D
from keras.models import Sequential
from keras.optimizers import Adam

# Load MNIST data set and split to train and test sets
(train_images, train_labels), (test_images, test_labels) = mnist.load_data()

# Reshaping to format which CNN expects (batch, height, width, channels)
train_images = train_images.reshape(train_images.shape[0], train_images.shape[1], train_images.shape[2], 1).astype(
    "float32")
test_images = test_images.reshape(test_images.shape[0], test_images.shape[1], test_images.shape[2], 1).astype("float32")

# Normalize images from 0-255 to 0-1
train_images /= 255
test_images /= 255

# Use one hot encode to set classes
number_of_classes = 10

train_labels = keras.utils.to_categorical(train_labels, number_of_classes)
test_labels = keras.utils.to_categorical(test_labels, number_of_classes)

# Create model, add layers
model = Sequential()
model.add(Conv2D(32, (5, 5), input_shape=(train_images.shape[1], train_images.shape[2], 1), activation="relu"))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(32, (3, 3), activation="relu"))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.5))
model.add(Flatten())
model.add(Dense(128, activation="relu"))
model.add(Dropout(0.5))
model.add(Dense(number_of_classes, activation="softmax"))

# Compile model
model.compile(loss="categorical_crossentropy", optimizer=Adam(), metrics=["accuracy"])

# Learn model
model.fit(train_images, train_labels, validation_data=(test_images, test_labels), epochs=7, batch_size=200)

# Test obtained model
score = model.evaluate(test_images, test_labels, verbose=0)
print("Model loss = {}".format(score[0]))
print("Model accuracy = {}".format(score[1]))

# Save model
model_filename = "cnn_model.h5"
model.save(model_filename)
print("CNN model saved in file: {}".format(model_filename))
