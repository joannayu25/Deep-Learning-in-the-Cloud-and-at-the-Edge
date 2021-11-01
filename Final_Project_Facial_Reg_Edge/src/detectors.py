import os
from os.path import isdir
from os.path import join
import numpy as np
import dlib

import cv2
import tensorflow as tf

class FaceDetector():
    def __init__(self, detector_specs):
        self.detector_name = detector_specs[0]
#         print(self.detector_name)
        if len(detector_specs) > 1:
            self.detector_file = detector_specs[1]
        if self.detector_name == "OPENCV":
            self.scale_factor = detector_specs[2]
            self.min_neighbors = detector_specs[3]
        elif self.detector_name == "HW7":
            self.detection_threshold = detector_specs[2]
        elif self.detector_name == "DLIB":
            pass
        else:
            print("Wrong Model Name")
        self.initialize_detector()
        
    def initialize_detector(self):
        if self.detector_name == "OPENCV":
            self.face_cascade = cv2.CascadeClassifier(self.detector_file)
        elif self.detector_name == "HW7":
            self.FROZEN_GRAPH_NAME = self.detector_file
            self.output_dir=''
            self.frozen_graph = tf.compat.v1.GraphDef()
            with open(os.path.join(self.output_dir, self.FROZEN_GRAPH_NAME), 'rb') as f:
                self.frozen_graph.ParseFromString(f.read())
            self.INPUT_NAME='image_tensor'
            self.BOXES_NAME='detection_boxes'
            self.CLASSES_NAME='detection_classes'
            self.SCORES_NAME='detection_scores'
            self.MASKS_NAME='detection_masks'
            self.NUM_DETECTIONS_NAME='num_detections'
            self.input_names = [self.INPUT_NAME]
            self.output_names = [self.BOXES_NAME, self.CLASSES_NAME, self.SCORES_NAME, self.NUM_DETECTIONS_NAME]
            self.tf_config = tf.compat.v1.ConfigProto()
            self.tf_config.gpu_options.allow_growth = True
            self.tf_sess = tf.compat.v1.Session(config=self.tf_config)
            tf.import_graph_def(self.frozen_graph, name='')
            self.tf_input = self.tf_sess.graph.get_tensor_by_name(self.input_names[0] + ':0')
            self.tf_scores = self.tf_sess.graph.get_tensor_by_name('detection_scores:0')
            self.tf_boxes = self.tf_sess.graph.get_tensor_by_name('detection_boxes:0')
            self.tf_classes = self.tf_sess.graph.get_tensor_by_name('detection_classes:0')
            self.tf_num_detections = self.tf_sess.graph.get_tensor_by_name('num_detections:0')
        elif self.detector_name == "DLIB":
            self.dlib_detector = dlib.get_frontal_face_detector()
    def detect_faces(self, image):
        if self.detector_name == "OPENCV":
            faces = self.face_cascade.detectMultiScale(image, self.scale_factor, self.min_neighbors)
        elif self.detector_name == "HW7":
            image_resized = cv2.resize(image, (300, 300))
            self.scores, self.boxes, self.classes, self.num_detections = self.tf_sess.run([self.tf_scores, self.tf_boxes, self.tf_classes, self.tf_num_detections], feed_dict={
                self.tf_input: image_resized[None, ...]
            })
            self.boxes = self.boxes[0] # index by 0 to remove batch dimension
            self.scores = self.scores[0]
            self.classes = self.classes[0]
            self.num_detections = self.num_detections[0]
            faces = []
            for i in range(int(self.num_detections)):
                if self.scores[i] >= self.detection_threshold:
                    self.box = self.boxes[i] * np.array([image.shape[0], image.shape[1], image.shape[0], image.shape[1]])
                    self.box = self.box.astype(int)
                    y = self.box[0]
                    x = self.box[1]
                    h = self.box[2] + 1 - self.box[0]
                    w = self.box[3] + 1 - self.box[1]
                    faces.append([x,y,w,h])
        elif self.detector_name == "DLIB":
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            rects = self.dlib_detector(image, 0)
            faces = []
            for rect in rects:
                x = rect.left()
                y = rect.top()
                w = rect.right() - rect.left()
                h = rect.bottom() - rect.top()
                faces.append([x,y,w,h])
        return faces