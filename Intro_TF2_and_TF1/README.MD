# TensorFlow2 and TensorFlow 1
## Joanna Yu
## Wednesday 4pm, Summer 2020

**1. What is TensorFlow? Which company is the leading contributor to TensorFlow?**
> TensorFlow is an end-to-end open source platform for machine learning. It has a comprehensive, flexible ecosystem of tools, libraries and community resources that lets researchers push the state-of-the-art in ML and developers easily build and deploy ML powered applications. TensorFlow was developed by the Google Brain team for internal Google use. It was released under the Apache License 2.0 on November 9, 2015.

**2. What is TensorRT? How is it different from TensorFlow?**
> The NVIDIA TensorRT™ is an SDK for high-performance deep learning inference. It includes a deep learning inference optimizer and runtime that delivers low latency and high-throughput for deep learning inference applications. TensorFlow is the actual platform for machine learning.

**3. What is ImageNet? How many images does it contain? How many classes?**
> The ImageNet project is a large visual database designed for use in visual object recognition software research. As of May 2020, it contains 14,197,122 images and 21,841 classes.

**4. Please research and explain the differences between MobileNet and GoogleNet (Inception) architectures.**
> The GoogleNet (Inception) architecture is based on the idea of concatenating layers so the network can choose what to learn from those layers. The MobileNet is designed to be lightweight since it's for mobile applications. Instead of convolution layers, MobileNet uses depthwise separable convolutions.

**5. In your own words, what is a bottleneck?**
> The bottleneck is the part of the neural network where the representation shrinks substantially. It's usually near the final layer where the classification will happen.

**6. How is a bottleneck different from the concept of layer freezing?**
> Layer freezing refers to the fact that layer weights are untouched during transfer learning. The bottleneck refers to the part of the neural network near the final layer where the representation shrinks substantially.

**7. In the TF1 lab, you trained the last layer (all the previous layers retain their already-trained state). Explain how the lab used the previous layers (where did they come from? how were they used in the process?)**
> The previous layers were trained using the ImageNet dataset. The weights of those layers are pre-determined and untouched in the new training being done. 

**8. How does a low `--learning_rate` (step 7 of TF1) value (like 0.005) affect the precision? How much longer does training take?**
> Precision increased slightly by a couple percentage points. Training took a little longer.

**9. How about a `--learning_rate` (step 7 of TF1) of 1.0? Is the precision still good enough to produce a usable graph?**
> Using such a large learning rate causes a lot of oscillation on the accuracy numbers. Eventually the accuracies stablized. 

**10. For step 8, you can use any images you like. Pictures of food, people, or animals work well. You can even use ImageNet images. How accurate was your model? Were you able to train it using a few images, or did you need a lot?**
> I used some food pictures and the model did really well with small number of pictures. 

**11. Run the TF1 script on the CPU (see instructions above) How does the training time compare to the default network training (section 4)? Why?**
> Training time was about the same probably because MobileNet does not really need a GPU for optimized calculations. 

**12. Try the training again, but this time do export ARCHITECTURE="inception_v3" Are CPU and GPU training times different?**
> CPU took longer since Inception_v3 can take advantage of the GPU.

**13. Given the hints under the notes section, if we trained Inception_v3, what do we need to pass to replace ??? below to the label_image script? Can we also glean the answer from examining TensorBoard**
> `python -m scripts.label_image --input_layer=Mul --input_height=299 --input_width=299  --graph=tf_files/retrained_graph.pb --image=tf_files/flower_photos/daisy/21652746_cc379e0eea_m.jpg`


