import paho.mqtt.client as mqtt
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation
import json
import tkinter as tk
from tkinter import scrolledtext, Entry, Button, messagebox, ttk
from PIL import Image, ImageTk
import socket
import pandas as pd
from datetime import datetime

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"Connected to {broker_entry.get()}:{port_combobox.get()}")
        connection_status_label.config(text="Connected successfully", fg="green")
        client.subscribe("topic/stream")
    else:
        print(f"Connection failed with result code {rc}")
        if rc == 5:  # Authentication error
            messagebox.showerror("Connection Error", "Authentication failed. Check username and password.")
        elif rc == 4:  # Connection refused - bad broker address
            connection_status_label.config(text="Invalid broker address", fg="red")
        else:
            connection_status_label.config(text=f"Connection failed (Code {rc})", fg="red")

# Variables for storing x, y data
x_data = []
y_data = []

def on_message(client, userdata, msg):
    message = msg.payload.decode('utf-8')
    print(f"Received message: {message}")
    update_gui(message)

    payload = msg.payload.decode('utf-8')
    data = json.loads(payload)
    
    x_point = data.get('x')
    y_point = data.get('y')

    x_data.append(x_point)
    y_data.append(y_point)
    

def update_plot(frame):
    if x_data:
        line1.set_xdata(x_data)
        line1.set_ydata(y_data)
        ax1.relim()
        ax1.autoscale_view()
        canvas1.draw()
    if x_data:
        line2.set_xdata(x_data)
        line2.set_ydata(y_data)
        ax2.relim()
        ax2.autoscale_view()
        canvas2.draw()
    if x_data:
        line3.set_xdata(x_data)
        line3.set_ydata(y_data)
        ax3.relim()
        ax3.autoscale_view()
        canvas3.draw()

def update_gui(message):
    label.config(state=tk.NORMAL)
    label.insert(tk.END, f"{message}\n")
    label.config(state=tk.DISABLED)
    label.yview(tk.END)  # Scroll to the bottom

def connect_to_broker():
    broker_address = broker_entry.get()
    port_number = int(port_combobox.get())

    try:
        client.connect(broker_address, port_number, 60)
        client.loop_start()  # Start the loop after connection
    except socket.gaierror:
        connection_status_label.config(text="Invalid broker address", fg="red")

def save_to_txt():
    save_file("txt")

def save_to_csv():
    save_file("csv")

def save_to_excel():
    save_file("xlsx")

def save_file(extension):
    file_name = file_entry.get()
    if not file_name:
        messagebox.showerror("Error", "Please enter a file name.")
        return

    messages = label.get("1.0", tk.END)
    if not messages.strip():
        messagebox.showinfo("Info", "No content to save.")
        return

    file_path = f"{file_name}.{extension}"
    if extension == "txt":
        with open(file_path, "w") as file:
            file.write(messages)
    elif extension == "csv":
        data = {"Messages": messages.splitlines()}
        df = pd.DataFrame(data)
        df.to_csv(file_path, index=False)
    elif extension == "xlsx":
        data = {"Messages": messages.splitlines()}
        df = pd.DataFrame(data)
        df.to_excel(file_path, index=False)

    messagebox.showinfo("Save Success", f"Messages saved to {file_path}")

# Tkinter setup
root = tk.Tk()
root.title("RIG-QUE")

# Create a header frame
header_frame = tk.Frame(root)
header_frame.pack(fill='x')

# Load and resize your logo image (replace 'your_logo.png' with the actual filename)
logo_image = Image.open('logo.png')
logo_image = logo_image.resize((50, 50))
logo_image = ImageTk.PhotoImage(logo_image)

# Create a label widget to display the resized logo in the header frame
logo_label = tk.Label(header_frame, image=logo_image)
logo_label.grid(row=0, column=0, padx=10, pady=10)

# Broker entry and label in the header frame
broker_label = tk.Label(header_frame, text="Broker:")
broker_label.grid(row=0, column=1)
broker_entry = Entry(header_frame)
broker_entry.grid(row=0, column=2)

# Port combobox in the header frame
port_label = tk.Label(header_frame, text="Port:")
port_label.grid(row=0, column=3)
port_combobox = ttk.Combobox(header_frame, values=["1883", "8883"])  # Add more port values as needed
port_combobox.set("1883")  # Set a default value
port_combobox.grid(row=0, column=4)

# Connect button in the header frame
connect_button = Button(header_frame, text="Connect", command=connect_to_broker)
connect_button.grid(row=0, column=5, padx=10, pady=10)

# Connection status label in the header frame
connection_status_label = tk.Label(header_frame, text="", fg="black")
connection_status_label.grid(row=0, column=6, padx=10, pady=10)

# Main content frame
content_frame = tk.Frame(root)
content_frame.pack(expand=True, fill='both')

# Main content area (scrolled text)
label = scrolledtext.ScrolledText(content_frame, state=tk.DISABLED)
label.pack(expand=True, fill='both')

# Create a subframe for file entry, label, and save button
file_frame = tk.Frame(content_frame)
file_frame.pack(pady=10)

# File entry in the subframe
file_label = tk.Label(file_frame, text="File Name:")
file_label.pack(side=tk.LEFT, padx=5)
file_entry = Entry(file_frame)
file_entry.pack(side=tk.LEFT, padx=5)

# Combobox for selecting file extension
extension_var = tk.StringVar()
extension_combobox = ttk.Combobox(file_frame, textvariable=extension_var, values=["txt", "csv", "xlsx"])
extension_combobox.set("txt")  # Set default value
extension_combobox.pack(side=tk.LEFT, padx=5)

# Save button in the subframe
save_button = Button(file_frame, text="Save", command=lambda: save_file(extension_var.get()))
save_button.pack(side=tk.LEFT, padx=5)

# Create a frame for the first graph
frame1 = tk.Frame(root)
frame1.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

# Create a Matplotlib figure for the first real-time graph
fig1, ax1 = plt.subplots()
line1, = ax1.plot([], [], label='Graph 1',color='red', marker='o')
ax1.set_xlabel('X1')
ax1.set_ylabel('Y1')
ax1.legend()

# Embed Matplotlib plot in Tkinter window
canvas1 = FigureCanvasTkAgg(fig1, master=frame1)
canvas_widget1 = canvas1.get_tk_widget()
canvas_widget1.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

# Use Matplotlib animation to update the first plot
ani1 = FuncAnimation(fig1, update_plot, interval=1000)  # 1000 milliseconds (1 second) update interval

# Create a frame for the second graph
frame2 = tk.Frame(root)
frame2.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

# Create a Matplotlib figure for the second real-time graph
fig2, ax2 = plt.subplots()
line2, = ax2.plot([], [], label='Graph 2',color='blue', marker='o')
ax2.set_xlabel('X2')
ax2.set_ylabel('Y2')
ax2.legend()

# Embed Matplotlib plot in Tkinter window
canvas2 = FigureCanvasTkAgg(fig2, master=frame2)
canvas_widget2 = canvas2.get_tk_widget()
canvas_widget2.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

# Use Matplotlib animation to update the second plot
ani2 = FuncAnimation(fig2, update_plot, interval=1000)  # 1000 milliseconds (1 second) update interval

# Create a frame for the third graph
frame3 = tk.Frame(root)
frame3.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

# Create a Matplotlib figure for the third real-time graph
fig3, ax3 = plt.subplots()
line3, = ax3.plot([], [], label='Graph 3',color='green', marker='o')
ax3.set_xlabel('X3')
ax3.set_ylabel('Y3')
ax3.legend()

# Embed Matplotlib plot in Tkinter window
canvas3 = FigureCanvasTkAgg(fig3, master=frame3)
canvas_widget3 = canvas3.get_tk_widget()
canvas_widget3.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

# Use Matplotlib animation to update the third plot
ani3 = FuncAnimation(fig3, update_plot, interval=1000)  # 1000 milliseconds (1 second) update interval

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

def on_closing():
    # Stop the MQTT client loop and disconnect
    print("Closing the application.")
    client.loop_stop()
    client.disconnect()
    print("Disconnected from MQTT broker.")
    root.destroy()
    print("Tkinter window destroyed.")

# Handle window close events
root.protocol("WM_DELETE_WINDOW", on_closing)

# Start the Tkinter main loop
try:
    root.mainloop()
except KeyboardInterrupt:
    # Gracefully handle interruption (e.g., Ctrl+C)
    print("Received keyboard interrupt. Stopping the subscriber.")
    client.loop_stop()
    client.disconnect()
    print("Disconnected from MQTT broker.")
