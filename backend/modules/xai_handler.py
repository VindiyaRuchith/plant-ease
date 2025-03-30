import numpy as np
import tensorflow as tf
import cv2

class XAIHandler:
    def __init__(self, model):
        self.model = model

    def hires_cam(self, img_array, class_index):
        # Generate a heatmap using HiRes-CAM with summation across channels
        try:
            last_conv_layer = [layer for layer in self.model.layers if 'conv' in layer.name][-1]
            grad_model = tf.keras.models.Model([self.model.input], [last_conv_layer.output, self.model.output])

            with tf.GradientTape() as tape:
                conv_outputs, predictions = grad_model(img_array)
                loss = predictions[:, class_index]

            grads = tape.gradient(loss, conv_outputs)
            heatmap = conv_outputs * grads
            heatmap = np.maximum(heatmap, 0)
            # Instead of averaging, sum across the channels:
            heatmap = np.sum(heatmap, axis=-1)[0]
            heatmap /= np.max(heatmap) + 1e-8
            heatmap = cv2.resize(heatmap, (224, 224))
            return heatmap

        except Exception as e:
            raise ValueError(f"Error in HiRes-CAM: {str(e)}")
    
    def grad_cam_plus(self, img_array, class_index):
        # Generate a heatmap using Grad-CAM++.
        try:
            # Get the last convolutional layer
            last_conv_layer = [layer for layer in self.model.layers if 'conv' in layer.name][-1]
            # Build a model that maps the input image to the activations of the last conv layer
            # and the model's output predictions.
            grad_model = tf.keras.models.Model([self.model.input], [last_conv_layer.output, self.model.output])
            
            with tf.GradientTape() as tape1:
                with tf.GradientTape() as tape2:
                    with tf.GradientTape() as tape3:
                        conv_outputs, predictions = grad_model(img_array)
                        loss = predictions[:, class_index]
                    grads = tape3.gradient(loss, conv_outputs)
                first_derivative = tape2.gradient(loss, conv_outputs)
            second_derivative = tape1.gradient(first_derivative, conv_outputs)
            
            # Compute the alpha coefficients for Grad-CAM++.
            alpha_num = second_derivative
            alpha_denom = 2 * second_derivative + tf.square(grads)
            # Prevent division by zero by adding a small constant where needed.
            alpha_denom = tf.where(tf.equal(alpha_denom, 0.0), tf.ones_like(alpha_denom) * 1e-10, alpha_denom)
            alphas = alpha_num / alpha_denom
            
            # We only keep positive gradients.
            weights = tf.maximum(grads, 0.0)
            # Combine the alphas with the weights over the spatial dimensions.
            deep_linearization_weights = tf.reduce_sum(alphas * weights, axis=(1, 2))
            
            # Multiply the weights with the conv outputs and sum over the channels.
            conv_outputs = conv_outputs[0]  # Remove batch dimension
            heatmap = tf.reduce_sum(deep_linearization_weights[0] * conv_outputs, axis=-1)
            heatmap = tf.maximum(heatmap, 0)
            heatmap /= tf.reduce_max(heatmap) + 1e-8
            
            heatmap = cv2.resize(heatmap.numpy(), (224, 224))
            return heatmap

        except Exception as e:
            raise ValueError(f"Error in Grad-CAM++: {str(e)}")
