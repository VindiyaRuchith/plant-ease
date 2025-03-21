import tensorflow as tf
from tensorflow.keras.models import load_model

class ModelHandler:
    def __init__(self, model_path):
        self.model = load_model(model_path)

    def predict(self, img_array):
        """Make predictions using the model."""
        predictions = self.model.predict(img_array)
        return predictions
