import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Step 2: Read the CSV file
data = pd.read_csv('2st_test.csv')

# Step 3: Extract required columns
time_str = data['time']
voltage = data['voltage']
average_reading = data['average_reading']
reading = data['reading']

# Convert the time string to a datetime object for plotting
time = [datetime.strptime(t, '%H:%M:%S') for t in time_str]

# Create two separate plots
plt.figure(figsize=(10, 6))

# Plot voltage vs. reading
plt.subplot(2, 1, 1)
plt.plot(voltage, reading, marker='o', linestyle='-', color='r')
plt.xlabel('Voltage')
plt.ylabel('Reading')
plt.title('Voltage vs Reading')
plt.grid()

# Plot voltage vs. time
plt.subplot(2, 1, 2)
plt.plot(time, reading, marker='o', linestyle='-', color='b')
plt.xlabel('Time')
plt.ylabel('Thrust')
plt.title('Thrust vs Time')
plt.xticks(rotation=45)
plt.grid()

# Adjust the layout to prevent overlap
plt.tight_layout()

# Show the plots
plt.show()
