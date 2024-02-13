import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np

# Function to update the graph
def update_graph(x_values, y_values, line, canvas, ax):
    # Update the data for the sine wave
    x_values += 0.1
    y_values = np.sin(x_values)

    # Update the plot data
    line.set_xdata(x_values)
    line.set_ydata(y_values)

    # Redraw the canvas
    canvas.draw()

    # Call the update_graph function after 100 milliseconds
    root.after(100, update_graph, x_values, y_values, line, canvas, ax)

# Main Tkinter window
root = tk.Tk()
root.title("Live Graph")

# Create a Matplotlib figure and Tkinter canvas
fig, ax = plt.subplots()
canvas = FigureCanvasTkAgg(fig, master=root)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

# Initial data for the sine wave
x_values = np.linspace(0, 2*np.pi, 100)
y_values = np.sin(x_values)

# Plot the initial sine wave
line, = ax.plot(x_values, y_values, label='Sine Wave')
ax.legend()

# Start the update_graph function
update_graph(x_values, y_values, line, canvas, ax)

# Start the Tkinter main loop
root.mainloop()
