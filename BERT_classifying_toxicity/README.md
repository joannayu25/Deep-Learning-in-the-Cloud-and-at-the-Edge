# Classifying Toxicity with BERT
## Joanna Yu
## Wendesday 4pm, Summer 2020

## Introduction
In this assignment, we will run BERT in pytorch on the Jigsaw Toxicity classification dataset. We will do so by running a Jupyter notebook in an IBM VM instance.

### Starting the VM
#### P100:
```
ibmcloud sl vs create --datacenter=lon06 --hostname=p100a --domain=w251_hw6.cloud --image=2263543 --billing=hourly  --network 1000 --key=1810104 --flavor AC1_8X60X100 --san
```
#### V100:
```
ibmcloud sl vs create --datacenter=lon06 --hostname=v100a --domain=w251_hw6.cloud --image=2263543 --billing=hourly  --network 1000 --key=1810104 --flavor AC2_8X60X100 --san
```

Once the VM is created, ssh into the new machine and start the container. 
```
nvidia-docker run --rm --name hw06 -p 8888:8888 -d w251/hw06:x86-64
```
   
The above will output a container ID on completion, like `959f320ffed2cce68ff19d171dcd959e33ebca30a818501677978957867d96fe`
We can get the URL of the notebook by running: 
```
docker logs <containerid>
```
  
After running this, we will get an output like this:
```
	root@p100:~# docker run --rm --runtime=nvidia -it -p 8888:8888 -v /root:/root w251/pytorch_gpu_hw06
	[I 18:46:45.371 NotebookApp] Serving notebooks from local directory: /workspace
	[I 18:46:45.371 NotebookApp] The Jupyter Notebook is running at:
	[I 18:46:45.371 NotebookApp] http://(bef46d014d15 or 127.0.0.1):8888/?token=c5d34fc988f452c4105c77a56924fe392d52991dde48478e
	[I 18:46:45.371 NotebookApp] Use Control-C to stop this server and shut down all kernels (twice to skip confirmation).

```
We can access the notebook by replacing the public IP in the brackets, such as `http://158.176.131.11:8888/?token=c5d34fc988f452c4105c77a56924fe392d52991dde48478e`