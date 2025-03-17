import numpy as np
import tensorflow as tf
import cv2

class XAIHandler:
    def __init__(self, model):
        self.model = model

    def hires_cam(self, img_array, class_index):
        """Generate a heatmap using HiRes-CAM."""
        try:
            last_conv_layer = [layer for layer in self.model.layers if 'conv' in layer.name][-1]

            grad_model = tf.keras.models.Model([self.model.input], [last_conv_layer.output, self.model.output])

            with tf.GradientTape() as tape:
                conv_outputs, predictions = grad_model(img_array)
                loss = predictions[:, class_index]  

            grads = tape.gradient(loss, conv_outputs)
            heatmap = conv_outputs * grads  
            heatmap = np.maximum(heatmap, 0)  
            heatmap = np.mean(heatmap, axis=-1)[0]
            heatmap /= np.max(heatmap) + 1e-8  

            heatmap = cv2.resize(heatmap, (224, 224))
            return heatmap

        except Exception as e:
            raise ValueError(f"Error in HiRes-CAM: {str(e)}")
