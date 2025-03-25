import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Check if directory argument is provided
if len(sys.argv) != 2:
    print("Usage: python check_data.py <directory_path>")
    sys.exit(1)

data_dir = sys.argv[1]

# Read all CSV files from directory and combine into one dataframe
print(f"Loading data from {data_dir}...")
data_frames = []
time_column = 'Time'

for filename in os.listdir(data_dir):
    if filename.endswith(".csv"):
        file_path = os.path.join(data_dir, filename)
        df = pd.read_csv(file_path, parse_dates=[time_column], dayfirst=False)
        data_frames.append(df)

all_data = pd.concat(data_frames)

# Process time data
all_data = all_data.sort_values(by=time_column)
all_data[time_column] = pd.to_datetime(all_data[time_column])
all_data = all_data.set_index(time_column)

# Define a function to find minimum values
def find_min_value(cols):
    for col in cols:
        print(f'{col} min value is: {all_data[col].min()}')
        print(f"Index of minimum value: {all_data[col].idxmin()}")

# Calculate the power relationship metrics with tolerance for small errors
tolerance = 1

# Check S1 vs √(P1² + Q1²) relationship
all_data['diff_pqs'] = all_data['S1'] - np.sqrt(all_data['P1']**2 + all_data['Q1']**2)
all_data['check_pqs'] = np.where(all_data['diff_pqs'] <= tolerance, 1, 0)

# Calculate S from P and Q
all_data['Ssum_cal'] = np.sqrt(all_data['Psum_kW']**2 + all_data['Qsum_kvar']**2)

# Find minimum values for power difference
find_min_value(['diff_pqs'])

# Define a function to create dual-panel time series plots
def plot2_time_series(data, columns, title, ylabel, columns2, title2, ylabel2, colors=None):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 8), sharex=True)

    # Plot first panel
    for col in columns:
        ax1.plot(data.index, data[col], label=col, 
                color=colors[col] if colors and col in colors else None)
    ax1.set_title(title)
    ax1.set_xlabel('Time')
    ax1.set_ylabel(ylabel)
    ax1.grid(True)
    ax1.legend()

    # Plot second panel
    for col in columns2:
        ax2.plot(data.index, data[col], label=col,
                color=colors[col] if colors and col in colors else None)
    ax2.set_title(title2)
    ax2.set_xlabel('Time')
    ax2.set_ylabel(ylabel2)
    ax2.legend()
    ax2.grid(True)
    plt.tight_layout()

# Color map for consistent visualization
color_map = {
    # P and Q by phase
    'P1': 'blue',
    'Q1': 'cyan',
    'P2': 'green',
    'Q2': 'lime',
    'P3': 'red', 
    'Q3': 'lightcoral',
    # current by phase
    'I1': 'blue',
    'I2': 'green',
    'I3': 'red', 
    # Voltage angle by sequence
    'Ang_Vb': 'green',
    'Ang_Vc': 'red',
    # Current angle by sequence
    'Ang_Ia': 'cyan',
    'Ang_Ib': 'lime',
    'Ang_Ic': 'lightcoral',
    # THD
    'THD_Ia': 'blue',
    'THD_Ib': 'green',
    'THD_Ic': 'red',
    'THD_Va': 'cyan',
    'THD_Vb': 'lime',
    'THD_Vc': 'lightcoral',
    # Calculated values
    'diff_pqs': 'purple',
    'Ssum_kVA': 'orange',
    'Ssum_cal': 'brown'
}

# Create visualization plots
print("Creating plots...")

# Plot 1: Power difference and phase power values
plot2_time_series(
    data=all_data,
    columns=['diff_pqs'],
    title='Difference between S1 and √(P1² + Q1²)',
    ylabel='kVA',
    columns2=['P1', 'P2', 'P3', 'Q1', 'Q2', 'Q3'],
    title2='Phase Power Values (P1, P2, P3, Q1, Q2, Q3)',
    ylabel2='Power',
    colors=color_map
)

# Plot 2: Compare S measurements and THD values
plot2_time_series(
    data=all_data,
    columns=['Ssum_kVA', 'Ssum_cal'],
    title='Measured vs. Calculated S',
    ylabel='kVA',
    columns2=['THD_Vavg', 'THD_Iavg'],
    title2='THD Values',
    ylabel2='Percentage',
    colors=color_map
)

# Display plots
print("Displaying plots. Press Enter to close...")
plt.show(block=False)
input("Press Enter to close the figures...")
plt.close('all')