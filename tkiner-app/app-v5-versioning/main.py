# main.py
import tkinter as tk

class MyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("My Tkinter App")
        self.label = tk.Label(root, text="Hello, Tkinter!")
        self.label.pack(padx=20, pady=20)

if __name__ == "__main__":
    root = tk.Tk()
    app = MyApp(root)
    root.mainloop()
