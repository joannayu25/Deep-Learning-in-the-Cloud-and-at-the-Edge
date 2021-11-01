# Import packages
import os
from os.path import isdir
from os.path import join
import importlib

import numpy as np
from keras.models import load_model as keras_load_model
from tensorflow.keras.models import load_model as tf_load_model
# from keras.models import Model


class FaceEncoder():
    
    def __init__(self, encoder_name, encoder_file_path):
        if encoder_name == "facenet_keras":
            self.encoder_model = keras_load_model(encoder_file_path)

    # get the face embedding for one face
    def get_embedding(self, face_pixels):
        # scale pixel values
        face_pixels = face_pixels.astype('float32')
        # standardize pixel values across channels (global)
        mean, std = face_pixels.mean(), face_pixels.std()
        face_pixels = (face_pixels - mean) / std
        # transform face into one sample
        samples = np.expand_dims(face_pixels, axis=0)
        # make prediction to get embedding
        yhat = self.encoder_model.predict(samples)
        return yhat[0]