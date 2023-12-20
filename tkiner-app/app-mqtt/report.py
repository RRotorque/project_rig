import pandas as pd

# Read data from CSV file
csv_file_path = 'fligh-motortest.csv'  # Replace with the actual path to your CSV file
df = pd.read_csv(csv_file_path)

# Calculate changes in voltage and reading
df['Voltage Change'] = df['voltage']
df['Reading Change'] = df['reading']

# Extracting key metrics for analysis
max_voltage_change = df['Voltage Change'].max()
min_voltage_change = df['Voltage Change'].min()

max_reading_change = df['Reading Change'].max()
min_reading_change = df['Reading Change'].min()

# Generate a brief report
report = f"""
## Voltage and Reading Change Analysis

### Key Metrics

- **Maximum Voltage:** {max_voltage_change}
- **Minimum Voltage:** {min_voltage_change}

- **Maximum Thrust:** {max_reading_change}
- **Minimum Thrust:** {min_reading_change}

### Comparison Analysis

The analysis focuses on changes in voltage and sensor readings over time:

### Reading vs Time Analysis

To find the time corresponding to specific values of the reading:

"""
# Save the report to a text file (optional)
with open('change_analysis_report.txt', 'w') as report_file:
    report_file.write(report)

# Print the report
print(report)
