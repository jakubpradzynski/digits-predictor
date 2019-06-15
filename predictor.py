import pickle
import matplotlib.image as mpimg
import numpy as np
from PIL import Image
from keras.models import load_model

def load_image(filename):
    return mpimg.imread(filename)


def rgb2gray(rgb):
    return np.dot(rgb[..., :3], [0.299, 0.587, 0.114])


def convert_image_to_gray(image):
    return rgb2gray(image)


def flatten_to_one_dimensional(image):
    return image.flatten()


def fix_numbers(image):
    new_image = []
    for i in range(0, image.__len__()):
        value = image[i]
        if value > 0.999999:
            value = 0
        else:
            value = (value - 1) * (-1)
        new_image.append(value)
    return new_image


def to_numpy_array(image):
    return np.asarray(image)


def add_black_background_and_resize(filename):
    image = Image.open(filename)
    image.convert("RGBA")  # Convert this to RGBA if possible

    pixel_data = image.load()

    if image.mode == "RGBA":
        # If the image has an alpha channel, convert it to white
        # Otherwise we'll get weird pixels
        for y in range(image.size[1]):  # For each row ...
            for x in range(image.size[0]):  # Iterate through each column ...
                # Check if it's opaque
                if pixel_data[x, y][3] < 255:
                    # Replace the pixel data with the colour white
                    pixel_data[x, y] = (0, 0, 0, 255)

    # Resize the image thumbnail
    image.thumbnail([28, 28], Image.ANTIALIAS)
    image.save(filename)


def add_white_background_and_resize(filename):
    image = Image.open(filename)
    image.convert("RGBA")  # Convert this to RGBA if possible

    pixel_data = image.load()

    if image.mode == "RGBA":
        # If the image has an alpha channel, convert it to white
        # Otherwise we'll get weird pixels
        for y in range(image.size[1]):  # For each row ...
            for x in range(image.size[0]):  # Iterate through each column ...
                # Check if it's opaque
                if pixel_data[x, y][3] < 255 or	 pixel_data[x, y] == (0, 0, 0, 255):
                    # Replace the pixel data with the colour white
                    pixel_data[x, y] = (255, 255, 255, 255)
                else:
                    pixel_data[x, y] = (0, 0, 0, 255)

    # Resize the image thumbnail
    image.thumbnail([28, 28], Image.ANTIALIAS)
    image.save(filename)



class ImagePrepare:
    @staticmethod
    def prepare_for_cnn(filename):
        add_black_background_and_resize(filename)
        img = Image.open(filename).convert("L")
        img = np.resize(img, (28, 28, 1))
        im2arr = np.array(img)
        im2arr = im2arr / 255.0
        return im2arr.reshape(1, 28, 28, 1)

    @staticmethod
    def prepare_for_svm(filename):
        add_white_background_and_resize(filename)
        image = load_image(filename)
        image_in_gray = convert_image_to_gray(image)
        to_one_dimensional = flatten_to_one_dimensional(image_in_gray)
        fixed_numbers = fix_numbers(to_one_dimensional)
        return [to_numpy_array(fixed_numbers)]


class SVMPredict:
    def __init__(self):
        self.model = self.load_svm_model()

    def load_svm_model(self):
        return pickle.load(open("svm_model.sav", "rb"))

    def predict(self, image):
        return int(self.model.predict(image)[0])

    def predict_probability(self, image):
        return self.model.predict_proba(image)[0]


class CNNPredict:
    def __init__(self):
        self.model = self.load_cnn_model()

    def load_cnn_model(self):
        return load_model("cnn_model.h5")

    def predict(self, image):
        return int(self.model.predict_classes(image)[0])

    def predict_probability(self, image):
        return self.model.predict_proba(image)[0]


def predict_digit():
        svm_filename = "predict_svm.png"
        cnn_filename = "predict_cnn.png"
        prepared_for_svm = ImagePrepare.prepare_for_svm(svm_filename)
        svm_predict = SVMPredict().predict(image=prepared_for_svm)
        print("SVM PREDICT: " + str(svm_predict))
        print("SVM PROBABILITY: " + str(
            SVMPredict().predict_probability(image=prepared_for_svm)[svm_predict]))
        prepared_for_cnn = ImagePrepare.prepare_for_cnn(cnn_filename)
        cnn_predict = CNNPredict().predict(image=prepared_for_cnn)
        print("CNN PREDICT: " + str(cnn_predict))
        print("CNN PROBABILITY: " + str(
            CNNPredict().predict_probability(image=prepared_for_cnn)[cnn_predict]))

predict_digit()
