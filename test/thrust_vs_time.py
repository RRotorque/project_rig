import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Read the CSV file into a DataFrame
name='2st_test'
test_g='1000g'
data = pd.read_csv('{}.csv'.format(name))

# Convert the 'time' column to datetime objects
data['time'] = pd.to_datetime(data['time'], format='%H:%M:%S')

# Plotting
plt.figure(figsize=(12, 6))
plt.plot(data['time'], data['reading'], marker='o', linestyle='-', color='b')
plt.title('Thrust vs Time')
plt.xlabel('Time (Minutes:Seconds)')
plt.ylabel('Thrust')
plt.grid(True)

# Customize the x-axis labels to display minutes and seconds
time_labels = [time.strftime('%M:%S') for time in data['time']]
plt.xticks(data['time'], time_labels, rotation=45)

# Display the plot
plt.tight_layout()
plt.savefig('image/{}.png'.format(name+'_'+test_g+'_th_vs_ti'))  # Change 'image/' to your desired folder path
plt.show()
