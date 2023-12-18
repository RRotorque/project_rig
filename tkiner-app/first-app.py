import tkinter as tk
from tkinter import scrolledtext
import paho.mqtt.client as mqtt

class MqttApp:
    def __init__(self, master):
        self.master = master
        master.title("Thrust Rig")
        master.configure(bg='#e6e6e6')  # Set background color for the window

        # Variables for user input
        self.broker_address_var = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        # Entry widget for broker address
        self.broker_label = tk.Label(self.master, text="Broker Address:", bg='#e6e6e6')
        self.broker_label.pack(pady=(10, 0))

        self.broker_entry = tk.Entry(self.master, textvariable=self.broker_address_var, width=30)
        self.broker_entry.pack(pady=5)

        # Button to connect
        self.connect_button = tk.Button(self.master, text="Connect", command=self.connect_to_broker)
        self.connect_button.pack(pady=10)

        # Scrolled text area for displaying messages
        self.text_area = scrolledtext.ScrolledText(self.master, wrap=tk.WORD, width=40, height=10,
                                                   bg='#ffffff', fg='#000000')  # Set colors for the text area
        self.text_area.pack(padx=10, pady=10)

    def connect_to_broker(self):
        # Get the broker address from the entry widget
        self.broker_address = self.broker_address_var.get()

        # MQTT setup
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        try:
            # Connect to the MQTT broker
            self.client.connect(self.broker_address, 1883, 60)

            # Start the MQTT loop in a separate thread
            self.client.loop_start()
        except Exception as e:
            print(f"Error connecting to the broker: {e}")

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT broker")
            # Subscribe to a default topic or any specific topic you want
            client.subscribe("example_topic")
        else:
            print(f"Connection failed with code {rc}")

    def on_message(self, client, userdata, msg):
        # Display the received message in the Tkinter window
        message = f"Topic: {msg.topic}\nMessage: {msg.payload.decode()}\n\n"
        self.text_area.insert(tk.END, message)

# Create the Tkinter root window
root = tk.Tk()
app = MqttApp(root)

# Run the Tkinter event loop
root.mainloop()
