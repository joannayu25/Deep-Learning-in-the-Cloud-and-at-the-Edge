# Setup cloud training

## Setup server
1. Install pip
```apt install python3-pip```
2. Install related packages
```
apt-get install -y libsm6 libxext6 libxrender-dev
```
3. Install related python packages
```
pip3 install mtcnn==0.1.0
pip3 install Pillow
pip3 install matplotlib
pip3 install opencv-python
pip3 install tensorflow
pip3 install --upgrade tensorflow-gpu
pip3 install --upgrade tensorboard
pip3 install keras==2.3.1
pip3 install --upgrade tensorflow-gpu==1.14.0
pip3 install numpy==1.16.1
pip3 install scipy==1.1.0
pip3 install tensorboard==2.2.2
```

## Clone the repo
```
git clone https://github.com/davidsandberg/facenet.git
```

## Screen Session
Create a screen session in case the SSH connection broke. 
```
screen
```
To see all the screen sessions:
```
screen -ls
```

## Face Alignment
### Set the python path 
```
export PYTHONPATH=~/facenet/src
```

### Run the alignment
```
for N in {1..4}; do \
python3 src/align/align_dataset_mtcnn.py \
/data/CASIA-WebFace/ \
/data/CASIA-WebFace_mtcnnpy_182/ \
--image_size 182 \
--margin 44 \
--random_order \
--gpu_memory_fraction 0.25  \
& done
```

## Validate on LFW
### Download LFW for validation
```
curl -o lfw.tgz http://vis-www.cs.umass.edu/lfw/lfw.tgz
```

### Extract the unaligned LFW images to local storage
```
cd /data
mkdir -p lfw/raw
tar xvf ~/Downloads/lfw.tgz -C lfw/raw --strip-components=1
```

### Align the LFW Dataset
```
for N in {1..4}; do \
python3 src/align/align_dataset_mtcnn.py \
/data/lfw/raw/ \
/data/lfw/lfw_mtcnnpy_160/ \
--image_size 160 \
--margin 32 \
--random_order \
--gpu_memory_fraction 0.25  \
& done
```

### Classifier Training
```
python3 src/train_softmax.py \
--logs_base_dir ~/logs/facenet/ \
--models_base_dir ~/models/facenet/ \
--data_dir /data/CASIA-WebFace_mtcnnpy_182/ \
--image_size 160 \
--model_def models.inception_resnet_v1 \
--lfw_dir /data/lfw/lfw_mtcnnpy_160/ \
--optimizer ADAM \
--learning_rate -1 \
--max_nrof_epochs 150 \
--keep_probability 0.8 \
--random_crop \
--random_flip \
--use_fixed_image_standardization \
--learning_rate_schedule_file data/learning_rate_schedule_classifier_casia.txt \
--weight_decay 5e-4 \
--embedding_size 512 \
--lfw_distance_metric 1 \
--lfw_use_flipped_images \
--lfw_subtract_mean \
--validation_set_split_ratio 0.05 \
--validate_every_n_epochs 5 \
--prelogits_norm_loss_factor 5e-4

```

## Setup TensorBoard
```
screen 
tensorboard --logdir=~/logs/facenet --bind_all --port 6006
```
