import paho.mqtt.client as mqtt
import tkinter as tk
from tkinter import scrolledtext
import time

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe("topic/stream")

def on_message(client, userdata, msg):
    message = msg.payload.decode('utf-8')
    print(f"Received message: {message}")
    update_gui(message)

def update_gui(message):
    label.config(state=tk.NORMAL)
    label.insert(tk.END, f"{message}\n")
    label.config(state=tk.DISABLED)
    label.yview(tk.END)  # Scroll to the bottom

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)

# Tkinter setup
root = tk.Tk()
root.title("MQTT Subscriber GUI")

label = scrolledtext.ScrolledText(root, state=tk.DISABLED)
label.pack(expand=True, fill='both')

client.loop_start()  # Start the loop in a separate thread

try:
    root.mainloop()
except KeyboardInterrupt:
    # Gracefully handle interruption (e.g., Ctrl+C)
    print("Received keyboard interrupt. Stopping the subscriber.")
    client.loop_stop()
    client.disconnect()
