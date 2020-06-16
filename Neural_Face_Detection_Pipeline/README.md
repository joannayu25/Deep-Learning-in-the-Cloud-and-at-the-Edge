# Neural Face Detection Pipeline
**Joanna Yu**
**Wednesday 4pm, Summer 2020**

## Introduction
The objective of this assignment is to modify the processing pipeline implemented in homework 3 (IoT 101) and replace the OpenCV-based face detector with a Deep Learning-based one. The one I used is a mobilenet SSD (Single Shot Multibox Detector) based face detector with pretrained model provided, powered by tensorflow object detection API, trained by WIDERFACE dataset.

### Pipeline
Recall that the original pipeline uses the Jetson TX2 as the edge device to capture faces using OpenCV. The messaging protocol is MQTT. The cloud part is run using IBM Cloud and Object Storage. All components are packaged in Docker containers. All containers run in Alpine except the face detection piece, which runs in CUDA Ubuntu.

The only change is that instead of using the Cascade Classifier from OpenCV to perform the face detection, I am now using a mobilenet SSD (Single Shot multibox Detector) based face detector. 

### Tensorflow Face Detector

