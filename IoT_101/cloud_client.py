import paho.mqtt.client as mqtt
import sys

CLOUD_MQTT_HOST="mosquitto"
CLOUD_MQTT_PORT=1883
CLOUD_MQTT_TOPIC = "face_detection_topic"
img_count = 0
output_dir = '/mnt/jy_w251_bucket'

def on_connect_cloud(client, userdata, flags, rc):
        print("connected to cloud broker with rc: " + str(rc))
        client.subscribe(CLOUD_MQTT_TOPIC)
	
def on_message(client,userdata, msg):
    global img_count
    try:
    print("message received!")	
    # Re-publish message to the cloud broker
    image = msg.payload
    with open(output_dir+str(img_count)+'.png', 'wb') as out:
        out.write(image)
    img_count+=1
  except:
    print("Unexpected error:", sys.exc_info()[0])

cloud_mqttclient = mqtt.Client()
cloud_mqttclient.on_connect = on_connect_cloud
cloud_mqttclient.connect(CLOUD_MQTT_HOST, CLOUD_MQTT_PORT, 60)
cloud_mqttclient.on_message = on_message

# go into a loop
cloud_mqttclient.loop_forever()
