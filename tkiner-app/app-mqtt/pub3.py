import paho.mqtt.client as mqtt
import time
import json
import pandas as pd

def on_publish(client, userdata, mid):
    print("Message Published")

# Read data from CSV file
csv_file_path = "./fligh-motortest.csv"  # Replace with the actual path to your CSV file
df = pd.read_csv(csv_file_path)

client = mqtt.Client()
client.connect("localhost", 1883, 60)
client.on_publish = on_publish

# Extract headers from the CSV file
headers = df.columns.tolist()

# Iterate through rows and publish messages
for index, row in df.iterrows():
    # Generate a dictionary with header-value pairs
    message_dict = {header: row[header] for header in headers}

    payload = json.dumps(message_dict)

    # Publish the message
    client.loop_start()
    client.publish("topic/stream", payload, qos=1, retain=False)
    client.loop_stop()
    print(f"Message {index + 1} sent: {payload}")

    time.sleep(1)  # Simulate some processing time

client.disconnect()
