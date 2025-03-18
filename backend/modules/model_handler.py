import os
import tensorflow as tf
from google.cloud import storage

class ModelHandler:
    def __init__(self, model_path, bucket_name, blob_name, credentials_info):
        self.download_model(model_path, bucket_name, blob_name, credentials_info)
        self.model = tf.keras.models.load_model(model_path)

    def download_model(self, model_path, bucket_name, blob_name, credentials_info):
        storage_client = storage.Client(credentials=credentials_info)
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(blob_name)
        blob.download_to_filename(model_path)

    def predict(self, img_array):
        predictions = self.model.predict(img_array)
        return predictions