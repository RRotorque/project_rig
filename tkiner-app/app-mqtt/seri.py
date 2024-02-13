import tkinter as tk
from tkinter import ttk, messagebox
import serial
import threading
import serial.tools.list_ports

class TinkerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Arduino Serial Monitor Reader")

        # Variables
        self.com_ports = self.get_available_com_ports()
        self.com_port_var = tk.StringVar()
        self.com_port_var.set(self.com_ports[0] if self.com_ports else "")

        self.baud_rate_var = tk.StringVar()
        self.baud_rate_var.set("9600")

        # GUI Elements
        ttk.Label(root, text="COM Port:").grid(row=0, column=0, padx=10, pady=10)
        self.com_port_combobox = ttk.Combobox(root, textvariable=self.com_port_var, values=self.com_ports)
        self.com_port_combobox.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(root, text="Baud Rate:").grid(row=0, column=2, padx=10, pady=10)
        self.baud_rate_combobox = ttk.Combobox(root, textvariable=self.baud_rate_var, values=["9600", "115200"])
        self.baud_rate_combobox.grid(row=0, column=3, padx=10, pady=10)

        self.connect_button = ttk.Button(root, text="Connect", command=self.connect)
        self.connect_button.grid(row=1, column=0, columnspan=2, pady=10)

        self.disconnect_button = ttk.Button(root, text="Disconnect", command=self.disconnect)
        self.disconnect_button.grid(row=1, column=2, columnspan=2, pady=10)

        ttk.Label(root, text="Messages:").grid(row=2, column=0, padx=10, pady=10)
        self.message_text = tk.Text(root, height=10, width=50)
        self.message_text.grid(row=3, column=0, columnspan=4, padx=10, pady=10)

        # Serial Communication
        self.serial_port = None
        self.serial_thread = None
        self.is_connected = False

    def get_available_com_ports(self):
        com_ports = [port.device for port in serial.tools.list_ports.comports()]
        return com_ports

    def connect(self):
        if not self.is_connected:
            try:
                port = self.com_port_var.get()
                baud_rate = int(self.baud_rate_var.get())
                self.serial_port = serial.Serial(port=port, baudrate=baud_rate, timeout=1)
                self.is_connected = True

                self.serial_thread = threading.Thread(target=self.read_sensor_value)
                self.serial_thread.start()

                self.message_text.insert(tk.END, "Connected to {} with baud rate {}\n".format(port, baud_rate))
            except serial.SerialException as e:
                messagebox.showerror("Error", str(e))
        else:
            messagebox.showinfo("Info", "Already connected!")

    def read_sensor_value(self):
        while self.is_connected:
            try:
                data = self.serial_port.readline().decode('utf-8', errors='replace').strip()
                self.message_text.insert(tk.END, data + '\n')
            except serial.SerialException:
                self.disconnect()
                self.message_text.insert(tk.END, "Connection closed.\n")
                break

    def disconnect(self):
        if self.is_connected:
            self.is_connected = False
            self.serial_port.close()
            self.message_text.insert(tk.END, "Disconnected\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = TinkerApp(root)

    root.mainloop()
