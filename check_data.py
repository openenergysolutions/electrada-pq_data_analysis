import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
# Check if directory argument is provided
if len(sys.argv) != 2:
    print("Usage: python script_name.py <directory_path>")
    sys.exit(1)

data_dir = sys.argv[1]


# Read csv files and concatenate into one dataframe
data_frames = []

time_column = 'Time'
for filename in os.listdir(data_dir):
    if filename.endswith(".csv"):
        file_path = os.path.join(data_dir, filename)
        df = pd.read_csv(file_path, parse_dates=[time_column], dayfirst=False)
        data_frames.append(df)

all_data = pd.concat(data_frames)

all_data = all_data.sort_values(by=time_column)
all_data[time_column] = pd.to_datetime(all_data[time_column])
all_data = all_data.set_index(time_column)


### Find min _value
columns=['I1', 'I2', 'I3', 'P1', 'P2', 'P3']

def find_min_value(cols):
    for col in cols:
        print(f'{col} min value is: {all_data[col].min()}')
        print("Index of minimum value:", all_data[col].idxmin())

# find_min_value(columns)

### Check the relationship among PQS and plot
# Define a tolerance for small errors
tolerance = 1

# Calculate the new column
all_data['diff_pqs'] = all_data['S1'] - np.sqrt(all_data['P1']**2 + all_data['Q1']**2)
all_data['check_pqs'] = np.where(all_data['diff_pqs'] <= tolerance, 1, 0)

all_data['Ssum_cal'] = np.sqrt(all_data['Psum_kW']**2 + all_data['Qsum_kvar']**2)

find_min_value(['diff_pqs'])
def plot2_time_series(data, columns, title, ylabel, columns2, title2, ylabel2, colors=None):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 8), sharex=True)

    for col in columns:
        ax1.plot(data.index, data[col], label=col, color=colors[col] if colors and col in colors else None)
    ax1.set_title(title)
    ax1.set_xlabel('Time')
    ax1.set_ylabel(ylabel)
    ax1.grid(True)
    ax1.legend()

    for col in columns2:
        ax2.plot(data.index, data[col], label=col, color=colors[col] if colors and col in colors else None)

    ax2.set_title(title2)
    ax2.set_xlabel('Time')
    ax2.set_ylabel(ylabel2)
    ax2.legend()
    ax2.grid(True)
    plt.tight_layout()

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
    'THD_Vc': 'lightcoral'
}

plot2_time_series(
    data=all_data,
    columns=['diff_pqs'],
    title='Diff',
    ylabel='KVA',
    columns2=['P1', 'P2', 'P3', 'Q1', 'Q2', 'Q3'],
    title2='Time Series Data for P1, P2, P3, Q1, Q2, Q3',
    ylabel2='Power',
    colors=color_map
)

plot2_time_series(
    data=all_data,
    columns=['Ssum_kVA', 'Ssum_cal'],
    title='compare S',
    ylabel='KVA',
    columns2=['THD_Vavg', 'THD_Iavg'],
    title2='Time Series Data for THDs ',
    ylabel2='Power',
    colors=color_map
)


plt.show(block=False)
input("Press Enter to close the figure...")
plt.close('all')