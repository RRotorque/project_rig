import paho.mqtt.client as mqtt
import time

def on_publish(client, userdata, mid):
    print("Message Published")

client = mqtt.Client()
client.connect("localhost", 1883, 60)
message_count = 5

for i in range(message_count):
    message = f"Message {i + 1}"
    client.publish("topic/stream", message, qos=1, retain=False)
    print(f"Message {i + 1} sent")

    time.sleep(1)  # Simulate some processing time

client.disconnect()
