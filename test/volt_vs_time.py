import csv
import matplotlib.pyplot as plt
from datetime import datetime

# Initialize empty lists to store data
timestamps = []
voltages = []
name='2st_test'
test_g='1000g'
# Read data from the CSV file
with open('{}.csv'.format(name), 'r') as csvfile:
    csvreader = csv.DictReader(csvfile)
    for row in csvreader:
        timestamps.append(row['time'])
        voltages.append(float(row['voltage']))

# Convert timestamps to datetime objects
time_objects = [datetime.strptime(ts, "%H:%M:%S") for ts in timestamps]

# Extract minutes and seconds from the datetime objects
minutes_and_seconds = [time_obj.strftime("%M:%S") for time_obj in time_objects]

# Create the plot
plt.figure(figsize=(12, 6))  # Adjust figure size as needed
plt.plot(minutes_and_seconds, voltages, marker='o', linestyle='-')
plt.title('Voltage vs. Time')
plt.xlabel('Time (MM:SS)')
plt.ylabel('Voltage')
plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
plt.grid(True)

# Show the plot
plt.tight_layout()
plt.savefig('image/{}.png'.format(name+'_'+test_g+'_vol_vs_ti'))  # Change 'image/' to your desired folder path
plt.show()

