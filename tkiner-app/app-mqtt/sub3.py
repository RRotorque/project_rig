import paho.mqtt.client as mqtt
import tkinter as tk
from tkinter import scrolledtext, Entry, Button, messagebox
import time

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"Connected to {broker_entry.get()}:{port_entry.get()}")
        client.subscribe("topic/stream")
    else:
        print(f"Connection failed with result code {rc}")
        messagebox.showerror("Connection Error", f"Connection failed with result code {rc}")

def on_message(client, userdata, msg):
    message = msg.payload.decode('utf-8')
    print(f"Received message: {message}")
    update_gui(message)

def update_gui(message):
    label.config(state=tk.NORMAL)
    label.insert(tk.END, f"{message}\n")
    label.config(state=tk.DISABLED)
    label.yview(tk.END)  # Scroll to the bottom

def connect_to_broker():
    broker_address = broker_entry.get()
    port_number = int(port_entry.get())

    client.connect(broker_address, port_number, 60)
    client.loop_start()  # Start the loop after connection

# Tkinter setup
root = tk.Tk()
root.title("MQTT Subscriber GUI")

broker_label = tk.Label(root, text="Broker:")
broker_label.pack()
broker_entry = Entry(root)
broker_entry.pack()

port_label = tk.Label(root, text="Port:")
port_label.pack()
port_entry = Entry(root)
port_entry.pack()

connect_button = Button(root, text="Connect", command=connect_to_broker)
connect_button.pack()

label = scrolledtext.ScrolledText(root, state=tk.DISABLED)
label.pack(expand=True, fill='both')

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

try:
    root.mainloop()
except KeyboardInterrupt:
    # Gracefully handle interruption (e.g., Ctrl+C)
    print("Received keyboard interrupt. Stopping the subscriber.")
    client.loop_stop()
    client.disconnect()
