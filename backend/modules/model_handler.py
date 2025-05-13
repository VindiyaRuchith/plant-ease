import tensorflow as tf
from tensorflow.keras.models import load_model

class ModelHandler:
    def __init__(self, model_path):
        # Load the pre-trained model from the specified path
        self.model = load_model(model_path)

    def predict(self, img_array):
        return self.model.predict(img_array)
