import paho.mqtt.client as mqtt

# MQTT broker configuration
broker_address = "192.168.128.110"
broker_port = 1883

# Callback when the client connects to the broker
def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker with result code "+str(rc))
    # Subscribe to the topics
    client.subscribe("voltage")
    client.subscribe("loadCellReading")
    client.subscribe("averageReading")

# Callback when a message is received from the broker
def on_message(client, userdata, msg):
    print(f"Received message on topic {msg.topic}: {msg.payload.decode()}")

# Create an MQTT client instance
client = mqtt.Client()

# Set callback functions
client.on_connect = on_connect
client.on_message = on_message

# Connect to the MQTT broker
client.connect(broker_address, broker_port, 60)

# Start the MQTT loop
client.loop_forever()
