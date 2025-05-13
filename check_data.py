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
    ax1.set_xlabel(time_column)
    ax1.set_ylabel(ylabel)
    ax1.grid(True)
    ax1.legend()

    # Plot second panel
    for col in columns2:
        ax2.plot(data.index, data[col], label=col,
                color=colors[col] if colors and col in colors else None)
    ax2.set_title(title2)
    ax2.set_xlabel(time_column)
    ax2.set_ylabel(ylabel2)
    ax2.legend()
    ax2.grid(True)
    plt.tight_layout()

def plot6_time_series(data, 
                     columns1, title1, ylabel1,
                     columns2, title2, ylabel2,
                     columns3, title3, ylabel3,
                     columns4, title4, ylabel4,
                     columns5, title5, ylabel5,
                     columns6, title6, ylabel6,
                     colors=None):
    """
    Plot six time series on six separate subplots sharing the same x-axis.
    
    Parameters:
    - data: DataFrame with time index
    - columnsN: List of column names to plot in subplot N
    - titleN: Title for subplot N
    - ylabelN: Y-axis label for subplot N
    - colors: Optional dictionary mapping column names to colors
    """
    fig, (ax1, ax2, ax3, ax4, ax5, ax6) = plt.subplots(6, 1, figsize=(14, 16), sharex=True)
    
    # Plot first panel
    for col in columns1:
        ax1.plot(data.index, data[col], label=col, 
                color=colors[col] if colors and col in colors else None)
    ax1.set_title(title1)
    ax1.set_ylabel(ylabel1)
    ax1.grid(True)
    ax1.legend()
    
    # Plot second panel
    for col in columns2:
        ax2.plot(data.index, data[col], label=col,
                color=colors[col] if colors and col in colors else None)
    ax2.set_title(title2)
    ax2.set_ylabel(ylabel2)
    ax2.grid(True)
    ax2.legend()
    
    # Plot third panel
    for col in columns3:
        ax3.plot(data.index, data[col], label=col,
                color=colors[col] if colors and col in colors else None)
    ax3.set_title(title3)
    ax3.set_ylabel(ylabel3)
    ax3.grid(True)
    ax3.legend()
    
    # Plot fourth panel
    for col in columns4:
        ax4.plot(data.index, data[col], label=col,
                color=colors[col] if colors and col in colors else None)
    ax4.set_title(title4)
    ax4.set_ylabel(ylabel4)
    ax4.grid(True)
    ax4.legend()
    
    # Plot fifth panel
    for col in columns5:
        ax5.plot(data.index, data[col], label=col,
                color=colors[col] if colors and col in colors else None)
    ax5.set_title(title5)
    ax5.set_ylabel(ylabel5)
    ax5.grid(True)
    ax5.legend()
    
    # Plot sixth panel
    for col in columns6:
        ax6.plot(data.index, data[col], label=col,
                color=colors[col] if colors and col in colors else None)
    ax6.set_title(title6)
    ax6.set_xlabel(time_column)
    ax6.set_ylabel(ylabel6)
    ax6.grid(True)
    ax6.legend()
    
    plt.tight_layout()
    return fig

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

# # Plot 1: Power difference and phase power values
# plot2_time_series(
#     data=all_data,
#     columns=['diff_pqs'],
#     title='Difference between S1 and √(P1² + Q1²)',
#     ylabel='kVA',
#     columns2=['P1', 'P2', 'P3', 'Q1', 'Q2', 'Q3'],
#     title2='Phase Power Values (P1, P2, P3, Q1, Q2, Q3)',
#     ylabel2='Power',
#     colors=color_map
# )

# Plot 2: Compare S measurements and THD values
# plot2_time_series(
#     data=all_data,
#     columns=['V1', 'V2', 'V3'],
#     title='Voltages in each phase',
#     ylabel='V',
#     columns2=['THD_Vavg', 'THD_Iavg'],
#     title2='THD Values',
#     ylabel2='Percentage',
#     colors=color_map
# )

# plot2_time_series(
#     data=all_data,
#     columns=['V1', 'V2', 'V3'],
#     title='Voltages in each phase',
#     ylabel='V',
#     columns2=['I1', 'I2', 'I3'],
#     title2='Currents in each phase',
#     ylabel2='A',
#     colors=color_map
# )

plot6_time_series(
    data=all_data,
    columns1=['P1', 'P2', 'P3', 'Q1', 'Q2', 'Q3'],
    title1='Phase Power Values',
    ylabel1='KVA',
    columns2=['I1', 'I2', 'I3'],
    title2='Currents by phase',
    ylabel2='A',
    columns3=['THD_Ia', 'THD_Ib', 'THD_Ic'],
    title3='Current THD by phase',
    ylabel3='Percentage',
    columns4=['V1', 'V2', 'V3'],
    title4='Voltages by phase',
    ylabel4='V',
    columns5=['THD_Va', 'THD_Vb', 'THD_Vc'],
    title5='Voltage THD by phase',
    ylabel5='Percentage',
    columns6=['PF1', 'PF2', 'PF3'],
    title6='Power Factor by phase',
    ylabel6='Percentage',
    colors=color_map
)

# Display plots
print("Displaying plots. Press Enter to close...")
plt.show(block=False)
input("Press Enter to close the figures...")
plt.close('all')