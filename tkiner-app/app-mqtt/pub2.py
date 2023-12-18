import paho.mqtt.client as mqtt
import time
import json
import random

def on_publish(client, userdata, mid):
    print("Message Published")

client = mqtt.Client()
client.connect("localhost", 1883, 60)

message_count = 50

for i in range(message_count):
    # Generate random x, y points for demonstration
    x_point = i + 1
    y_point = random.uniform(0, 10)

    # Create a JSON payload
    payload = json.dumps({'x': x_point, 'y': y_point})

    # Publish the message
    client.loop_start()
    client.publish("topic/stream", payload, qos=1, retain=False)
    client.loop_stop()
    print(f"Message {i + 1} sent: {payload}")

    time.sleep(1)  # Simulate some processing time

client.disconnect()
