import os
import sys
import pandas as pd
import matplotlib.pyplot as plt

# Check command line arguments
if len(sys.argv) != 2:
    print("Usage: python process.py <directory_path>")
    sys.exit(1)

data_dir = sys.argv[1]

# Load data from CSV files
print(f"Loading data from {data_dir}...")
data_frames = []
time_column = 'Time'

data_for_plot = {
    'column1': ['I1', 'I2', 'I3'],
    'title1': 'Current Magnitude Per Phase',
    'ylabel1': 'Amps',
    'column2': ['Ang_Ia', 'Ang_Ib', 'Ang_Ic','Ang_Vb', 'Ang_Vc'],
    'title2': 'Current Phase Angle Per Phase',
    'ylabel2': 'Degrees',
}

data_for_plot2 = {
    'column1': ['P1', 'P2', 'P3', 'Q1', 'Q2', 'Q3'],
    'title1': 'P, Q Per Phase',
    'ylabel1': 'Kw',
    'column2': ['PF'],
    'title2': 'Power Factor',
    'ylabel2': 'p.u.',
}

for filename in os.listdir(data_dir):
    if filename.endswith(".csv"):
        file_path = os.path.join(data_dir, filename)
        df = pd.read_csv(file_path, parse_dates=[time_column], dayfirst=False)
        data_frames.append(df)

if not data_frames:
    print(f"No CSV files found in {data_dir}")
    sys.exit(1)

# Combine data and sort by time
all_data = pd.concat(data_frames)
all_data = all_data.sort_values(by=time_column)
all_data[time_column] = pd.to_datetime(all_data[time_column])
all_data = all_data.set_index(time_column)

# Calculate consumption metrics if energy columns exist
energy_columns = [col for col in all_data.columns if 'EP_TOTAL' in col or 'EQ_TOTAL' in col]
if energy_columns:
    print("Calculating energy consumption...")
    
    # Define consumption calculation function
    def calculate_consumption(data, columns):
        """Calculate daily and weekly consumption for given energy columns."""
        daily_consumption = pd.DataFrame()
        weekly_consumption = pd.DataFrame()

        for column in columns:
            # Calculate daily consumption
            daily_start = data[column].resample('D').first()
            daily_end = data[column].resample('D').last()
            daily_diff = daily_end - daily_start
            daily_consumption[column] = daily_diff

            # Calculate weekly consumption
            weekly_start = data[column].resample('W').first()
            weekly_end = data[column].resample('W').last()
            weekly_diff = weekly_end - weekly_start
            weekly_consumption[column] = weekly_diff

        daily_consumption = daily_consumption.reset_index()
        weekly_consumption = weekly_consumption.reset_index()
        daily_consumption.columns = ['Date'] + [f'Daily_{col}_Consumption' for col in columns]
        weekly_consumption.columns = ['Week'] + [f'Weekly_{col}_Consumption' for col in columns]

        print("\nDaily Consumption:")
        print(daily_consumption)

        print("\nWeekly Consumption:")
        print(weekly_consumption)
        
        return daily_consumption, weekly_consumption

    # Color map for consistent visualization
    color_map = {
        # Active and reactive energy
        'EP_TOTAL_kWh': 'blue',
        'EQ_TOTAL_kvarh': 'green',
        # Derived consumption values
        'Daily_EP_TOTAL_kWh_Consumption': 'blue',
        'Daily_EQ_TOTAL_kvarh_Consumption': 'green',
        'Weekly_EP_TOTAL_kWh_Consumption': 'blue',
        'Weekly_EQ_TOTAL_kvarh_Consumption': 'green'
    }

    # Calculate and display consumption
    daily_data, weekly_data = calculate_consumption(all_data, energy_columns)

    # Plot energy data
    def plot_dual_time_series(data1, columns1, title1, ylabel1, 
                             data2, columns2, title2, ylabel2, 
                             colors=None):
        """Create a figure with two vertically stacked time series plots."""
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 8), sharex=True)

        # Plot first panel
        for col in columns1:
            ax1.plot(data1.index, data1[col], label=col, 
                    color=colors[col] if colors and col in colors else None)
        ax1.set_title(title1)
        ax1.set_ylabel(ylabel1)
        ax1.grid(True)
        ax1.legend()

        # Plot second panel
        for col in columns2:
            ax2.plot(data2.index, data2[col], label=col, 
                    color=colors[col] if colors and col in colors else None)
        ax2.set_title(title2)
        ax2.set_xlabel('Time')
        ax2.set_ylabel(ylabel2)
        ax2.grid(True)
        ax2.legend()
        
        plt.tight_layout()

    # Create plots
    print("Creating plots...")
    
    # Plot time series of interest
    plot_dual_time_series(
        data1=all_data,
        columns1=data_for_plot['column1'],
        title1=data_for_plot['title1'],
        ylabel1=data_for_plot['ylabel1'],
        data2=all_data,
        columns2=data_for_plot['column2'],
        title2=data_for_plot['title2'],
        ylabel2=data_for_plot['ylabel2'],
        colors=color_map
    )
    plot_dual_time_series(
        data1=all_data,
        columns1=data_for_plot2['column1'],
        title1=data_for_plot2['title1'],
        ylabel1=data_for_plot2['ylabel1'],
        data2=all_data,
        columns2=data_for_plot2['column2'],
        title2=data_for_plot2['title2'],
        ylabel2=data_for_plot2['ylabel2'],
        colors=color_map
    )

else:
    print("No energy data (EP_TOTAL or EQ_TOTAL) found in the dataset.")

# Display plots if they were created
if energy_columns:
    print("Displaying plots. Press Enter to close...")
    plt.show(block=False)
    input("Press Enter to close the figures...")
    plt.close('all')
