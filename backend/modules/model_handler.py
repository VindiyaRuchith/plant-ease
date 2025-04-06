import tensorflow as tf
from tensorflow.keras.models import load_model

class ModelHandler:
    def __init__(self, model_path):
        # No custom objects needed if the model was re-saved using TF 2.13.1
        self.model = load_model(model_path)

    def predict(self, img_array):
        return self.model.predict(img_array)
