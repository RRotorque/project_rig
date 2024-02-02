import paho.mqtt.client as mqtt

# MQTT broker details
broker_address = "192.168.151.110"
broker_port = 1883
topic = "sensorData"

# Callback when the client connects to the broker
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe(topic)

# Callback when a message is received from the broker
def on_message(client, userdata, msg):
    print(f"Received message on topic {msg.topic}: {msg.payload.decode()}")

# Create an MQTT client instance
client = mqtt.Client()

# Set the callback functions
client.on_connect = on_connect
client.on_message = on_message

# Connect to the broker
client.connect(broker_address, broker_port, 60)

# Start the loop to listen for messages
client.loop_forever()
