import socket

# Server settings
host = '192.168.34.82'
port = 8081  # Choose an available port

# Set up server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen(1)
print(f"Server listening on {host}:{port}")

# Open CSV file for writing
csv_file = open('2st_test.csv', 'a')
header = 'time,millsec,voltage,reading,average_reading\n'
csv_file.write(header)

while True:
    client_socket, _ = server_socket.accept()
    data = client_socket.recv(1024).decode()

    if data:
        print(f"Received data: {data}")
        csv_file.write(data + '\n')
        csv_file.flush()
        client_socket.send('Data received'.encode())

    client_socket.close()

csv_file.close()
server_socket.close()
