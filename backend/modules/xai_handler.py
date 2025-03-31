import numpy as np
import tensorflow as tf
import cv2

class XAIHandler:
    def __init__(self, model):
        self.model = model # store the trained model for generating heatmaps

    def hires_cam(self, img_array, class_index):
        # Generate a heatmap using HiRes-CAM with summation across channels
        try:
            # Find the last convolutional layer
            last_conv_layer = [layer for layer in self.model.layers if 'conv' in layer.name][-1]
            # Create a model that outputs the activations of the last conv layer and the final predictions
            grad_model = tf.keras.models.Model([self.model.input], [last_conv_layer.output, self.model.output])

            with tf.GradientTape() as tape:
                # Forward pass to get conv layer outputs and predictions
                conv_outputs, predictions = grad_model(img_array)
                loss = predictions[:, class_index] # Focus on the class of interest

            # Compute gradients of the class score with respect to the conv layer outputs
            grads = tape.gradient(loss, conv_outputs)

            # Multiply the conv outputs with the gradients
            # and apply ReLU to get the heatmap
            heatmap = conv_outputs * grads
            heatmap = np.maximum(heatmap, 0)

            # HiRes-CAM uses summation accross channels instead of average
            heatmap = np.sum(heatmap, axis=-1)[0] # Remove batch dimension
            # Normalize the heatmap to [0, 1]
            heatmap /= np.max(heatmap) + 1e-8
            # Resize the heatmap to the original image size
            heatmap = cv2.resize(heatmap, (224, 224))
            return heatmap

        except Exception as e:
            raise ValueError(f"Error in HiRes-CAM: {str(e)}")
    
    def grad_cam_plus(self, img_array, class_index):
        # Generate a heatmap using Grad-CAM++.
        try:
            # Get the last convolutional layer
            last_conv_layer = [layer for layer in self.model.layers if 'conv' in layer.name][-1]
            # Build a model that returns conv layer activations and final predictions
            grad_model = tf.keras.models.Model([self.model.input], [last_conv_layer.output, self.model.output])
            
            # Use nested gradient tapes to compute higher-order gradients 
            with tf.GradientTape() as tape1:
                with tf.GradientTape() as tape2:
                    with tf.GradientTape() as tape3:
                        conv_outputs, predictions = grad_model(img_array)
                        loss = predictions[:, class_index] # Target class score
                    grads = tape3.gradient(loss, conv_outputs) # First derivative
                first_derivative = tape2.gradient(loss, conv_outputs) # First derivative
            second_derivative = tape1.gradient(first_derivative, conv_outputs) # Second derivative
            
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
            # Combine conv outputs with linearization weights to get the heatmap.
            heatmap = tf.reduce_sum(deep_linearization_weights[0] * conv_outputs, axis=-1)
            heatmap = tf.maximum(heatmap, 0)
            heatmap /= tf.reduce_max(heatmap) + 1e-8
            
            # Resize the heatmap to the original image size
            heatmap = cv2.resize(heatmap.numpy(), (224, 224))
            return heatmap

        except Exception as e:
            raise ValueError(f"Error in Grad-CAM++: {str(e)}")
