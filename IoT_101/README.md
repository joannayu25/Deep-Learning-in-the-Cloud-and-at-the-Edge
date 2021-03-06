# Internet of Things 101
### Joanna Yu
### Wednesday 4pm, Summer 2020

## Introduction
The overall goal of the assignment is to be able to capture faces in a video stream coming from the edge in real time, transmit them to the cloud in real time, and save these faces in the cloud for long term storage. The general pipeline is depicted in the following picture. The pipeline uses the Jetson TX2 as the edge device to capture faces using OpenCV. The messaging protocol is MQTT. The cloud part is run using IBM Cloud and Object Storage. All components are packaged in Docker containers. All containers run in Alpine except the face detection piece, which runs in CUDA Ubuntu.

![pipeline_diagram](/IoT_101/hw03.png)

## Edge: Bridge Network
A bridge network called `hw3_bridge` is created so containers can connect to it.

For debugging purposes, containers connected to `hw3_bridge` can be listed by running `inspect`.

`sudo docker network inspect hw3_bridge`

## Edge: Broker
A Docker image, `broker_image`, is first created for the MQTT broker using the lightweight Alpine Linux distro with `Dockerfile.broker`. Then a container, called 'mosquitto', is created to start the MQTT broker. 

```
sudo docker build -t broker_image -f Dockerfile.broker .
sudo docker run --name mosquitto --network hw3_bridge -p 1883:1883 -ti broker_image sh
/usr/sbin/mosquitto
```

If successful, the output should be similar to:
```
1589786753: mosquitto version 1.6.8 starting
1589786753: Using default config.
1589786753: Opening ipv4 listen socket on port 1883.
1589786753: Opening ipv6 listen socket on port 1883.
```
The broker will now accept connections from other clients. 

## Edge: Face Detection 
Face detection, `face_detect.py`, uses OpenCV's pre-trained frontal face HARR Cascade Classifier. Once one or more faces are detected, they will be marked by rectangles. The faces will then be cropped and sent to the broker under the topic `face_detection_topic`. The QoS is set to 0 as messages should not be lost between the face detection client and the broker since the transmission does not involve an external network.  
   
A Docker image, `face_detect_image`, is first created for the face detection client with file `Dockerfile.face_detect`. A container called `face_detection` is created from the image.
```
sudo docker build -t face_detect_image -f Dockerfile.face_detect .
xhost +
sudo docker run --name face_detection -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix --rm --privileged --network hw3_bridge -it face_detect_image bash
```
Once inside the container, `face_detection.py` is loaded to start the app. It will connect to the MQTT broker (`mosquitto` container), bring up the USB camera, start detecting faces, and publish the faces as binary messages to the MQTT broker. 

`python face_detection.py`

On the broker side, Once the face_detection client connects to the MQTT broker, the output should be similar to:
```
1589788678: New connection from 172.19.0.4 on port 1883.
1589788678: New client connected from 172.19.0.4 as auto-2CE86754-2ACF-2339-6B60-90CD0F0D1F6C (p2, c1, k60).
```

## Edge: Forwarder
A Docker image, `forwarder_image`, is first created for the MQTT forwarder client using the lightweight Alpine Linux distro with `Dockerfile.forwarder`. Then a container called 'forwarder' is created to start the MQTT client and connect to the broker.
```
sudo docker build -t forwarder_image -f Dockerfile.forwarder .
sudo docker run --name forwarder --network hw3_bridge -ti forwarder_image sh
```
Once inside the container, start the client so it can connect to the local broker. The output should be similar to:
```
/hw3 # python mqtt_forwarder.py 
connected to local broker with rc: 0
```

The forwarder first connects to the broker and subscribes to the `face_detection_topic`. Upon receiving messages, the forwarder will then re-publish the message to the cloud broker under the same topic name (`face_detection_topic`) with QoS 0. Since faces typically show up in camera for at least a couple seconds and during that time, many copies of the faces are being re-published by the forwarder. There is good assurance that many copies will get to the cloud broker even at QoS 0.

## Cloud: Setup

A new and lightweight virtual machine is provisioned (2 CPUs and 4G of RAM) to run the cloud broker and client.

`ibmcloud sl vs create --hostname=face-detect-ibm --domain=w251.cloud --cpu=2 --memory=4096 --datacenter=sjc03 --san --os=UBUNTU_16_64 --disk=100 --key=MY_KEY`

Install Docker and verify that it has been installed:
```
apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    software-properties-common
	
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"

apt-get update
apt-get install -y docker-ce
docker run hello-world
```
Install IBM Cloud CLI:

`curl -fsSL https://clis.ng.bluemix.net/install/linux | sh`

Install IBM CLoud Storage:
```
sudo apt-get update
sudo apt-get install automake autotools-dev g++ git libcurl4-openssl-dev libfuse-dev libssl-dev libxml2-dev make pkg-config
git clone https://github.com/s3fs-fuse/s3fs-fuse.git
cd s3fs-fuse
./autogen.sh
./configure
make
sudo make install
```

Object storage instance named `jy-obj-store` and a bucket named `hw3-faces2` are created. The service key named `jy_obj_store_key` is created with HMAC enabled using CLI:
```
ibmcloud resource service-key-create jy_obj_store_key Writer --instance-name jy-obj-store --parameters '{"HMAC":true}'
```

To configure s3fs-fuse, set up the credential using the access key ID and secret access key from Service Credentials.
```
echo "<Access_Key_ID>:<Secret_Access_Key>" > $HOME/.cos_creds
chmod 600 $HOME/.cos_creds
```

Mount the bucket:
```
sudo mkdir -m 777 /mnt/mybucket
sudo s3fs hw3-faces /mnt/mybucket -o passwd_file=$HOME/.cos_creds -o sigv2 -o use_path_request_style -o url=https://s3.us-south.cloud-object-storage.appdomain.cloud
```
*Note: The content of the bucket should be visible in `/mnt/mybucket` if the mounting is successful. Otherwise, the debug log can be accessed by adding the -f option at the end.* 


## Cloud: Broker
A Docker image, `cloud_broker_image`, is first created for the MQTT broker using the lightweight Alpine Linux distro with `Dockerfile.broker`. Then a container called 'mosquitto' is created to start the MQTT broker.
```
docker build -t cloud_broker_image -f Dockerfile.broker .
docker run --name mosquitto -p 1883:1883 -ti cloud_broker_image sh
/usr/sbin/mosquitto
```
If successful, the output should be similar to:
```
1589961735: mosquitto version 1.6.8 starting
1589961735: Using default config.
1589961735: Opening ipv4 listen socket on port 1883.
1589961735: Opening ipv6 listen socket on port 1883.
```

As the forwarder successfully connects to the cloud broker, the output should be:
```
1589961958: New connection from 73.92.34.175 on port 1883.
1589961958: New client connected from 73.92.34.175 as auto-437985CB-8401-E25B-CDDD-86ACC85B8328 (p2, c1, k60).
```

## Cloud: MQTT Client
A MQTT client is created using `cloud_client.py`, which connects to the cloud broker and subscribes to the `face_detection_topic`. Upon receiving messages, the cloud client will extract and save the images to IBM Object Storage (bucket `hw3-faces2`) via the mounted folder. The container, where the cloud client runs from, is created from an image from the Dockerfile `Dockerfile.cloud_client` with the lightweight Alpine Linux distro environment.

```
docker build -t cloud_client_image -f Dockerfile.cloud .
docker run --name cloud_client -v /mnt/mybucket:/my_faces -ti cloud_client_image sh
```

Once inside the container, run the cloud client: 

`python cloud_client.py`

As the client connects to the broker and receives messages, the output should be:
```
connected to cloud broker with rc: 0
subscribed to topic: face_detection_topic
message received!
image saved to /my_faces/img_0.png
```

To allow http access to the bucket, public access will need to be enabled in Buckets -> Access Policies -> Public Access. The link to the Object Storage is: `http://s3.us-south.cloud-object-storage.appdomain.cloud/hw3-faces2/` 

Here is a sample image:

![sample_image](/IoT_101/img_99.png)