import tkinter as tk
from tkinter import ttk
import serial
import threading
import serial.tools.list_ports

class TinkerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Serial Communication App")

        # Variables
        self.com_ports = self.get_available_com_ports()
        self.com_port_var = tk.StringVar()
        self.com_port_var.set(self.com_ports[0] if self.com_ports else "")

        self.data_var = tk.StringVar()

        # GUI Elements
        ttk.Label(root, text="COM Port:").grid(row=0, column=0, padx=10, pady=10)
        self.com_port_combobox = ttk.Combobox(root, textvariable=self.com_port_var, values=self.com_ports)
        self.com_port_combobox.grid(row=0, column=1, padx=10, pady=10)

        self.refresh_button = ttk.Button(root, text="Refresh", command=self.refresh_ports)
        self.refresh_button.grid(row=0, column=2, padx=10, pady=10)

        self.connect_button = ttk.Button(root, text="Connect", command=self.connect)
        self.connect_button.grid(row=0, column=3, padx=10, pady=10)

        ttk.Label(root, text="Received Data:").grid(row=1, column=0, padx=10, pady=10)
        self.data_text = tk.Text(root, height=10, width=40)
        self.data_text.grid(row=1, column=1, columnspan=3, padx=10, pady=10)

        self.disconnect_button = ttk.Button(root, text="Disconnect", command=self.disconnect)
        self.disconnect_button.grid(row=2, column=1, columnspan=2, pady=10)

        # Serial Communication
        self.serial_port = None
        self.serial_thread = None
        self.is_connected = False

    def get_available_com_ports(self):
        com_ports = [port.device for port in serial.tools.list_ports.comports()]
        return com_ports

    def refresh_ports(self):
        self.com_ports = self.get_available_com_ports()
        self.com_port_combobox['values'] = self.com_ports

    def connect(self):
        if not self.is_connected:
            try:
                self.serial_port = serial.Serial(port=self.com_port_var.get(), baudrate=9600, timeout=1)
                self.is_connected = True

                self.serial_thread = threading.Thread(target=self.read_data)
                self.serial_thread.start()

                self.connect_button.configure(text="Disconnect")
                self.refresh_button.configure(state="disabled")
                self.com_port_combobox.configure(state="disabled")
            except serial.SerialException as e:
                tk.messagebox.showerror("Error", str(e))
        else:
            self.disconnect()

    def disconnect(self):
        if self.is_connected:
            self.is_connected = False
            self.serial_port.close()

            self.connect_button.configure(text="Connect")
            self.refresh_button.configure(state="normal")
            self.com_port_combobox.configure(state="readonly")

    def read_data(self):
        while self.is_connected:
            try:
                data = self.serial_port.readline()
                decoded_data = data.decode('utf-8', errors='replace').strip()
                self.data_text.insert(tk.END, decoded_data + '\n')
            except serial.SerialException:
                self.disconnect()
                tk.messagebox.showinfo("Info", "Connection closed.")
                break

if __name__ == "__main__":
    root = tk.Tk()
    app = TinkerApp(root)
    root.mainloop()
