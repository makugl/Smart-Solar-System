import paho.mqtt.client as mqtt
import time


mqtt_host = "test.mosquitto.org"
mqtt_client = mqtt.Client("SolarEdge123")


def on_connect(client, userdata, flags, rc):  # The callback for when the client connects to the broker
    print("Connected with result code {0}".format(str(rc)))  # Print result of connection attempt
    client.subscribe("haus4711/solaredge/production", qos=1)  # Subscribe to the topic “digitest/test1”, receive any messages published on it

def on_message(client, userdata, msg):  # The callback for when a PUBLISH message is received from the server.
    print("Message received-> " + msg.topic + " " + str(msg.payload))  # Print a received msg


mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

mqtt_client.connect(mqtt_host)
mqtt_client.loop_start()
time.sleep(0.05)
mqtt_client.loop_stop()
