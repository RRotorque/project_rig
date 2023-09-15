import socket
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Socket settings
HOST = '0.0.0.0'  # Listen on all available interfaces
PORT = 8080

# Create a socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)
print('Listening for incoming connections...')

# Accept a connection
client_socket, client_address = server_socket.accept()
print(f'Connected to {client_address}')

# Initialize lists to store data
time_data = []
voltage_data = []

# Initialize the plot
plt.style.use('ggplot')
fig, ax = plt.subplots()
line, = ax.plot([], [], label='Voltage (V)')

def update(frame):
    # Receive data from client
    data = client_socket.recv(1024).decode()
    if data:
        time_str, voltage_str = data.strip().split(",")  # Split time and voltage values
        voltage = float(voltage_str)
        time_data.append(len(voltage_data) + 1)  # Incremental time value
        voltage_data.append(voltage)
        line.set_data(time_data, voltage_data)
        ax.relim()  # Update the data limits
        ax.autoscale_view()  # Autoscale the view
    return line,


ani = FuncAnimation(fig, update, blit=True, interval=1000)

plt.tight_layout()
plt.show()

# Close the sockets
client_socket.close()
server_socket.close()
