import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file into a pandas DataFrame
name='2st_test'
test_g='1000g'
df = pd.read_csv('{}.csv'.format(name))

# Extract voltage and reading columns
voltage = df['voltage']
reading = df['reading']

# Create a line chart
plt.plot(voltage, reading, marker='o', linestyle='-', markersize=5, label='Voltage vs. Reading')

# Add labels to data points
for i, txt in enumerate(df.index):
    plt.annotate(txt, (voltage[i], reading[i]), fontsize=8, ha='right')

# Set labels and title
plt.xlabel('Voltage')
plt.ylabel('Reading')
plt.title('Voltage vs. Reading')

# Reverse the x-axis
plt.gca().invert_xaxis()

# Show the legend
plt.legend()

# Show the plot
plt.grid()
plt.savefig('image/{}.png'.format(name+'_'+test_g+'_vol_vs_th'))  # Change 'image/' to your desired folder path
plt.show()
