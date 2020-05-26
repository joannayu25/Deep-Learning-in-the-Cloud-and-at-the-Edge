# This Python file uses the following encoding: utf-8
import paho.mqtt.client as mqtt
import sys

CLOUD_MQTT_HOST='169.44.179.123'
CLOUD_MQTT_PORT=1883
CLOUD_MQTT_TOPIC = "face_detection_topic"
img_count = 0

def on_connect_cloud(client, userdata, flags, rc):
    	print('connected to cloud broker with rc: ' + str(rc))
    	client.subscribe(CLOUD_MQTT_TOPIC)
	print('subscribed to topic: '+ CLOUD_MQTT_TOPIC)

def on_message(client,userdata, msg):
	global img_count
	try:
		print("message received!")
		# Extract the image from the message and save
		# as a .png file to object storage via the mounted
		# folder. 
		image = msg.payload
		file_path = '/my_faces/img_'+str(img_count)+'.png'
		save_image = open(file_path, 'w+') 
		save_image.write(image)
		img_count+=1
		print('image saved to '+file_path)
	except:
		print("Unexpected error:", sys.exc_info()[0])

cloud_mqttclient = mqtt.Client()
cloud_mqttclient.on_connect = on_connect_cloud
cloud_mqttclient.connect(CLOUD_MQTT_HOST, CLOUD_MQTT_PORT, 60)
cloud_mqttclient.on_message = on_message

# go into a loop
cloud_mqttclient.loop_forever()
