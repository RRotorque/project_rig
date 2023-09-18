import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import csv

def plot_thrust_vs_time(name, test_g):
    data = pd.read_csv('{}.csv'.format(name))
    data['time'] = pd.to_datetime(data['time'], format='%H:%M:%S')

    plt.figure(figsize=(12, 6))
    plt.plot(data['time'], data['reading'], marker='o', linestyle='-', color='b')
    plt.title('Thrust vs Time')
    plt.xlabel('Time (Minutes:Seconds)')
    plt.ylabel('Thrust')
    plt.grid(True)

    time_labels = [time.strftime('%M') for time in data['time']]
    plt.xticks(data['time'], time_labels, rotation=45)

    plt.tight_layout()
    plt.savefig('image/{}_th_vs_ti.png'.format(name + '_' + test_g))
    plt.show()

def plot_voltage_vs_reading(name, test_g):
    df = pd.read_csv('{}.csv'.format(name))
    voltage = df['voltage']
    reading = df['reading']

    plt.plot(voltage, reading, marker='o', linestyle='-', markersize=5, label='Voltage vs. Reading')

    for i, txt in enumerate(df.index):
        plt.annotate(txt, (voltage[i], reading[i]), fontsize=8, ha='right')

    plt.xlabel('Voltage')
    plt.ylabel('Reading')
    plt.title('Voltage vs. Reading')

    plt.gca().invert_xaxis()
    plt.legend()
    plt.grid()
    plt.savefig('image/{}_vol_vs_th.png'.format(name + '_' + test_g))
    plt.show()

def plot_voltage_vs_time(name, test_g):
    timestamps = []
    voltages = []

    with open('{}.csv'.format(name), 'r') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            timestamps.append(row['time'])
            voltages.append(float(row['voltage']))

    time_objects = [datetime.strptime(ts, "%H:%M:%S") for ts in timestamps]
    minutes_and_seconds = [time_obj.strftime("%M") for time_obj in time_objects]

    plt.figure(figsize=(12, 6))
    plt.plot(minutes_and_seconds, voltages, marker='o', linestyle='-')
    plt.title('Voltage vs. Time')
    plt.xlabel('Time (MM:SS)')
    plt.ylabel('Voltage')
    plt.xticks(rotation=45)
    plt.grid(True)

    plt.tight_layout()
    plt.savefig('image/{}_vol_vs_ti.png'.format(name + '_' + test_g))
    plt.show()

# Call the functions with the appropriate file name and test name
name = 'Official_test_3a'
test_g = '1200'

plot_thrust_vs_time(name, test_g)
plot_voltage_vs_reading(name, test_g)
plot_voltage_vs_time(name, test_g)

print('check the images in the image folder,graph successful')
