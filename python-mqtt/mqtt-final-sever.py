import paho.mqtt.client as mqtt
import csv
import time

# MQTT broker configuration
broker_address = "192.168.128.110"
broker_port = 1883

filename = "fligh-motortest"

# CSV file configuration
csv_file_path = "./python-mqtt/{}.csv".format(filename)

# Data storage
data = {"voltage": "", "reading": "", "average_reading": ""}

# Callback when the client connects to the broker
def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker with result code " + str(rc))
    # Subscribe to the topics
    client.subscribe("voltage")
    client.subscribe("loadCellReading")
    client.subscribe("averageReading")

# Callback when a message is received from the broker
def on_message(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload.decode()

    # Add values to the data dictionary
    if topic == "voltage":
        data["voltage"] = payload
    elif topic == "loadCellReading":
        data["reading"] = payload
    elif topic == "averageReading":
        data["average_reading"] = payload

    print(f"Received message on topic {topic}: {payload}")

    try:
        # Check if all values are present, then write to CSV
        if all(data.values()):
            current_time = time.strftime("%H:%M:%S", time.localtime())
            millis = int(time.time() * 1000)
            print(f"Writing to CSV: {current_time}, {millis}, {data['voltage']}, {data['reading']}, {data['average_reading']}")
            write_to_csv(current_time, millis, data['voltage'], data['reading'], data['average_reading'])
            # Clear the data after writing to CSV
            data.clear()
    except KeyError:
        print("KeyError: Not all values present, waiting for the next set of data.")

def write_to_csv(current_time, millis, voltage, reading, average_reading):
    with open(csv_file_path, mode="a", newline="") as csv_file:
        csv_writer = csv.writer(csv_file)
        if csv_file.tell() == 0:
            csv_writer.writerow(["time", "millsec", "voltage", "reading", "average_reading"])
        csv_writer.writerow([current_time, millis, voltage, reading, average_reading])

# Create an MQTT client instance
client = mqtt.Client()

# Set callback functions
client.on_connect = on_connect
client.on_message = on_message

# Connect to the MQTT broker
client.connect(broker_address, broker_port, 60)

# Start the MQTT loop
client.loop_forever()
