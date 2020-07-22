# OpenAI Gym

**Joanna Yu**

**Wednesday 4pm, Summer 2020**

## Introduction
In this assignment, we will be training a lunar lander module to land properly using the Jetson TX2. The goal is to train the lunar module to land better. The model with the original parameter configuration will not converge and the lunar module will never learn to land well. By modifying the parameters (lines 30-43 of the python code), we should be able to train the module in fewer than 500 iterations. Here are the original parameters:

```
        self.density_first_layer = 16
        self.density_second_layer = 8
        self.num_epochs = 1
        self.batch_size = 64
        self.epsilon_min = 0.01
```


## About the Model
We are using a container base image with all the OpenAI Gym prerequisites installed. 

The python code is in agent_lunar_lander.py.

In the python code, the `env.step()` method directs the lander module to take another step (equivalent to one frame of video) and returns several fields: `state`, `reward`, `done`, and `info`. 

 - The `state` is a vector with eight values (x and y position, x and y velocity, lander angle and angular velocity, boolean for left leg contact with ground, boolean for right leg contact with ground). The state information is used to build the model using Keras.
 - The `reward` is a value indicating whether or not the step was "good" or "bad". A reward greater than 200 indicates a successful landing.
 - The `done` field is a boolean indicating whether or not the module has landed. 
 - `info` is not used.

We are using a Sequential model for the lander. A Sequential model is appropriate for a plain stack of layers where each layer has exactly one input tensor (current state) and one output tensor (best move to make). The "moves" that can be made are firing the thrusters (right, left, up) to adjust the speed and trajectory.


## Training and Testing
To run the environment, use these commands (ensure all the files from the hw11 github folder are in the current directory on the TX2):

```
# Add user to the Docker group
sudo usermod -aG docker $USER

# reboot to make the previous step take effect
docker build -t hw11 -f Dockerfile.agent .

# enable video sharing from the container
xhost +

# maximize performance on the device
sudo jetson_clocks --store
sudo jetson_clocks
time docker run -it --rm --net=host --runtime nvidia  -e DISPLAY=$DISPLAY -v /tmp/.X11-unix/:/tmp/.X11-unix:rw --privileged -v /data/videos:/tmp/videos hw11

# don't forget to turn off the fan on the device
sudo jetson_clocks --restore
```

When the process starts, you will see the animation of the lunar lander on your screen and the training will start.

Training output looks like this:

```
0 	: Episode || Reward:  -355.4552185273774 	|| Average Reward:  -355.4552185273774 	 epsilon:  0.995
1 	: Episode || Reward:  -302.69548515410156 	|| Average Reward:  -329.0753518407395 	 epsilon:  0.990025
2 	: Episode || Reward:  -197.1461440026914 	|| Average Reward:  -285.09894922805677 	 epsilon:  0.985074875
3 	: Episode || Reward:  -251.29447991556844 	|| Average Reward:  -276.64783189993466 	 epsilon:  0.9801495006250001
4 	: Episode || Reward:  -312.69842116384507 	|| Average Reward:  -283.85794975271676 	 epsilon:  0.9752487531218751
5 	: Episode || Reward:  -193.10620553981315 	|| Average Reward:  -268.73265905056616 	 epsilon:  0.9703725093562657
6 	: Episode || Reward:  -125.35339813322857 	|| Average Reward:  -248.2499074909465 	 epsilon:  0.9655206468094844
7 	: Episode || Reward:  -95.87496167296544 	|| Average Reward:  -229.20303926369886 	 epsilon:  0.960693043575437
8 	: Episode || Reward:  -10.731355125180073 	|| Average Reward:  -204.92840769275233 	 epsilon:  0.9558895783575597
```

The training will end when either the Average Reward is greater than 200, or 2000 iterations have passed. But it is recommended that we kill the model if it ever hits 800.

After the training, it will run a test process. The output will look like this:

```
DQN Training Complete...
Starting Testing of the trained model...
0       : Episode || Reward:  219.64614710147364
1       : Episode || Reward:  204.5401595978414
2       : Episode || Reward:  191.82778586724473
3       : Episode || Reward:  300.26513457499857
4       : Episode || Reward:  265.38375246986914
5       : Episode || Reward:  231.17971859331598
6       : Episode || Reward:  158.1286447553571
.
.
.
Average Reward:  243.09916996497867
```

The lunar landing mp4 files are stored in `/data/videos` on the TX2. 

**Sample videos are stored in object storage: https://hw11-lunar-landing.s3.us-south.cloud-object-storage.appdomain.cloud**

## Results

| Model | First Layer  | Second Layer | Epoch | Batch Size | Epsilon Min | Episodes to Reach Convergence  | Avg Reward (Testing) |
|---|---|---|---|---|---|---|---|
| Base  | 16  | 8  | 1 | 64   |   0.01 | - | - |
| #1 | 256   | 256  |1   | 64  |0.01| 507 | 219.02 |
| #2  | 256   | 256  |1   | 128  |0.01| 482 | 230.65 |
|  #3 |  256   | 256  |2   | 64  |0.01| 497 |242.22 |


## Questions and Answers
1) What parameters did you change? 
> As shown in the table above, I increased the number of hidden units in the first and second layers substantially. I also increased the batch size and epoch. 

2) What values did you try?
> As shown in the table above, I increased the number of hidden units in the first and second layers to 256. I also tried doubling the number of epochs to 2 and the batch size to 128. 

3) Did you try any other changes that made things better or worse?
> The changes made and the corresponding performance is shown in the table above. It is worth noting that with a batch size of 128, the TX2 seems to really struggle and regularly gives out low memory warnings so training is rather slow. 

4) Did they improve or degrade the model? Did you have a test run with 100% of the scores above 200?
> Increaing the first two layers, the epoch, and batch size definitely improve the model. But the effect varies. Increasing the batch size takes very long to train because of memory constraints. None of the test runs have 100% scores over 200. The logs are in the archive folder in this repo. Experiment #1 actually has testing scores as low as -23. Experiment #3 is the best performing one.

5) Based on what you observed, what conclusions can you draw about the different parameters and their values? 
> Increasing the number of hidden units allows the model to learn more about the different state and environment combinations. Increasing the batch size is beneficial but the TX2 complains about memory if the batch size is doubled to 128. The batch size allows the model to learn more state and environment combinations at the same time. Increasing the epoch allows the model to go through the data more than once and learn more from the data. 

6) What is the purpose of the epsilon value?
> The epsilon value allows us to control the balance between exploration and exploitation. A high epsilon value allows the lunar to explore using random action. As the lunar learns from training, epsilon decreases because the action of the lunar is being trained, so the randomness decreases. 

7) Describe "Q-Learning".
> Q-learning refers to the reinforcement learning algorithm where an agent can decide what action to take given the provided policy and the current situation. A model of the environment is not required. Therefore, the agent has certain amount of freedom to handle problems with somewhat random transitions and rewards.