import paho.mqtt.client as mqtt
import time

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe("topic/stream")

def on_message(client, userdata, msg):
    print(f"Received message: {msg.payload.decode('utf-8')}")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)

client.loop_start()  # Start the loop in a separate thread

try:
    while True:
        # Keep the main thread alive
        time.sleep(1)
except KeyboardInterrupt:
    # Gracefully handle interruption (e.g., Ctrl+C)
    print("Received keyboard interrupt. Stopping the subscriber.")
    client.loop_stop()
    client.disconnect()
