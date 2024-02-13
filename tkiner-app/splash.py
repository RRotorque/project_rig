import tkinter as tk
from PIL import Image, ImageTk

class SplashScreen(tk.Toplevel):
    def __init__(self, parent, logo_path):
        super().__init__(parent)
        self.overrideredirect(True)  # Remove outer window border
        self.geometry("+{}+{}".format(parent.winfo_screenwidth() // 2 - 150, parent.winfo_screenheight() // 2 - 100))
        
        # Load and display logo image
        logo_image = Image.open(logo_path)
        logo_photo = ImageTk.PhotoImage(logo_image)
        logo_label = tk.Label(self, image=logo_photo)
        logo_label.image = logo_photo
        logo_label.pack(pady=10)

    def close(self):
        self.destroy()

class MainApplication(tk.Tk):
    def __init__(self, logo_path):
        super().__init__()
        self.title("Main Application")
        self.geometry("500x300")

        # Show splash screen
        self.splash = SplashScreen(self, logo_path)
        self.after(2000, self.load_main_app)

    def load_main_app(self):
        # Close splash screen
        self.splash.close()

        # Add your main application widgets and logic here

if __name__ == "__main__":
    logo_path = "logo.png"
    app = MainApplication(logo_path)
    app.mainloop()
