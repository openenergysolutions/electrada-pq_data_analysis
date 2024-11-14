import os
import sys
import pandas as pd
import matplotlib.pyplot as plt

# Check if directory argument is provided
if len(sys.argv) != 2:
    print("Usage: python script_name.py <directory_path>")
    sys.exit(1)

data_dir = sys.argv[1]


# Read csv files and concatenate into one dataframe
data_frames = []

for filename in os.listdir(data_dir):
    if filename.endswith(".csv"):
        file_path = os.path.join(data_dir, filename)
        df = pd.read_csv(file_path, parse_dates=['Time'], dayfirst=False)
        data_frames.append(df)

all_data = pd.concat(data_frames)
all_data = all_data.sort_values(by='Time')

# Plot the data
def plot_time_series(data, columns, title, ylabel):
    plt.figure(figsize=(14, 8))
    for col in columns:
        plt.plot(data['Time'], data[col], label=col)
    plt.title(title)
    plt.xlabel('Time')
    plt.ylabel(ylabel)
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()


# Plot I1, I2, I3 in one figure
plot_time_series(
    data=all_data,
    columns=['I1', 'I2', 'I3'],
    title='Time Series Data for I1, I2, I3',
    ylabel='Current'
)

# Plot P1, P2, P3, Q1, Q2, Q3 in another figure
plot_time_series(
    data=all_data,
    columns=['P1', 'P2', 'P3', 'Q1', 'Q2', 'Q3'],
    title='Time Series Data for P1, P2, P3, Q1, Q2, Q3',
    ylabel='Power'
)
plt.show()