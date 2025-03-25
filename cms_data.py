import os
import sys
import pandas as pd
import matplotlib.pyplot as plt

# Check command line arguments
if len(sys.argv) != 2:
    print("Usage: python cms_data.py <directory_path>")
    sys.exit(1)

data_dir = sys.argv[1]

# Load power quality data from files
print(f"Loading power quality data from {data_dir}...")
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

# Load CMS data
print("Loading CMS data...")
time_column2 = 'timestamp'
cms_data_dir = "./data/mth_meter_data_2024-12-09.csv"  # alternative: "./data/mth_meter_data_2024-11-27.csv"
cms_df = pd.read_csv(cms_data_dir, parse_dates=[time_column2], dayfirst=False)
cms_df = cms_df.sort_values(by=time_column2)
cms_df[time_column2] = pd.to_datetime(cms_df[time_column2])
cms_df[time_column2] = cms_df[time_column2].dt.tz_localize(None)  # Remove timezone info if present

# Create common time index for both datasets
print("Aligning datasets...")
revised_full_index = pd.date_range(
    start=max(cms_df[time_column2].min(), all_data.index.min()), 
    end=min(cms_df[time_column2].max(), all_data.index.max()), 
    freq='min')

# Reindex both datasets to common time index
cms_df = cms_df.set_index(time_column2).reindex(revised_full_index)
all_data = all_data.reindex(revised_full_index)

# Calculate differences between measurements
print("Calculating differences...")
all_data['diff'] = all_data['Psum_kW'] - cms_df['site_power']
all_data['diff_site_power_percentage'] = (all_data['diff'] / cms_df['site_power']) * 100
all_data['diff_site_power_percentage'] = all_data['diff_site_power_percentage'].clip(lower=0, upper=100)
cms_df['diff_site_power_percentage'] = all_data['diff_site_power_percentage']

# Get list of charger columns (excluding the percentage difference column)
chargers = set(cms_df.columns.values)
chargers.remove('diff_site_power_percentage')

# Define plotting functions
def plot2_time_series(data, columns, title, ylabel, columns2, title2, ylabel2, colors=None):
    """Create a figure with two vertically stacked time series plots."""
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

def plot2_time_series_2data(data, columns, title, ylabel, data2, columns2, title2, ylabel2, colors=None):
    """Create a figure with two vertically stacked time series plots from different datasets."""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 8), sharex=True)

    # Plot first panel with data1 and site_power from data2
    for col in columns:
        ax1.plot(data.index, data[col], label=col, 
                color=colors[col] if colors and col in colors else None)
    # Add site_power from data2
    ax1.plot(data.index, data2['site_power'], label='site_power', 
            color=colors['site_power'] if colors and 'site_power' in colors else None)
    ax1.set_title(title)
    ax1.set_xlabel('Time')
    ax1.set_ylabel(ylabel)
    ax1.grid(True)
    ax1.legend()

    # Plot second panel with data2 (excluding site_power)
    for col in columns2:
        if col == 'site_power':  # Skip site_power as it's in the top panel
            continue
        ax2.plot(data2.index, data2[col], label=col,
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
    # Current by phase
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
    # THD values
    'THD_Ia': 'blue',
    'THD_Ib': 'green',
    'THD_Ic': 'red',
    'THD_Va': 'cyan',
    'THD_Vb': 'lime',
    'THD_Vc': 'lightcoral',
    # CMS comparison values
    'site_power': 'green',
    'Psum_kW': 'blue',
    'diff': 'red'
}

# Create visualization plots
print("Creating plots...")

# Plot 1: Compare power measurements and charger data
plot2_time_series_2data(
    data=all_data,
    columns=['Psum_kW', 'diff'],  # Meter power and difference
    title='Power Meter vs. CMS Site Power',
    ylabel='kW',
    data2=cms_df,
    columns2=chargers,  # All charger columns
    title2='Individual Charger Power',
    ylabel2='kW',
    colors=color_map
)

# Plot 2: Percentage difference between power measurements
plot2_time_series_2data(
    data=all_data,
    columns=['Psum_kW', 'diff'],  # Meter power and difference
    title='Power Meter vs. CMS Site Power',
    ylabel='kW',
    data2=cms_df,
    columns2=['diff_site_power_percentage'],  # Percentage difference
    title2='Percentage Difference',
    ylabel2='%',
    colors=color_map
)

# Display plots
print("Displaying plots. Press Enter to close...")
plt.show(block=False)
input("Press Enter to close the figures...")
plt.close('all')
