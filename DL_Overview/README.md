# Deep Learning Overview
## Joanna Yu
## Wednesday 4pm, Summer 2020

## ConvnetJS MNIST Demo

1) There is an input layer. The next layer is a 5x5 convolution layer with 8 filters and a stride of 1, padding of 2 and relu activation function. The next layer is a 2x2 pooling layer with a stride of 2. The next layer is a 5x5 convolution layer with 16 filters and a stride of 1, padding of 2, and relu activation function. The next layer is a 3x3 pooling layer with a stride of 3. The last layer, the output layer, performs softmax and outputs into one of the 10 classes.  

2) Changing the number and size of filters affects accuracy, both for better and worse depending on how they are changed. 

3) Removing the pooling layer decreases accuracy.

4) Adding one more layer doesn't seem to improve the accurancy much.

5) Increasing the batch size seems to reduce accuracy.

6) ~98%


