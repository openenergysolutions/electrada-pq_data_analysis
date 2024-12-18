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

time_column2 = 'timestamp'
cms_df = pd.read_csv("./data/mth_meter_data_2024-11-27.csv", parse_dates=[time_column2], dayfirst=False)
cms_df = cms_df.sort_values(by=time_column2)
cms_df[time_column2] = pd.to_datetime(cms_df[time_column2])
cms_df[time_column2] = cms_df[time_column2].dt.tz_localize(None)


# cms_df = cms_df.set_index(time_column2)

revised_full_index = pd.date_range(
    start=max(cms_df[time_column2].min(), all_data.index.min()), 
    end=min(cms_df[time_column2].max(), all_data.index.max()), 
    freq='min')
print(revised_full_index)
print(cms_df.columns)
cms_df = cms_df.set_index(time_column2).reindex(revised_full_index)

all_data = all_data.reindex(revised_full_index)
# print(f'Available datas are {all_data.columns.values}')
print(f'Available chargers are {cms_df.columns.values}')


# calculate daily and weekly total P and Q values
def calculate_consumption(data, columns):
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

    print("Daily Consumption:")
    print(daily_consumption)

    print("\nWeekly Consumption:")
    print(weekly_consumption)


calculate_consumption(all_data, ['EP_TOTAL_kWh','EQ_TOTAL_kvarh'])



# Plot the data
def plot_time_series(data, columns, title, ylabel, colors=None):
    plt.figure(figsize=(14, 8))
    for col in columns:
        plt.plot(data.index, data[col], label=col)
    plt.title(title)
    plt.xlabel('Time')
    plt.ylabel(ylabel)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()


# Plot I1, I2, I3 in one figure
# plot_time_series(
#     data=all_data,
#     columns=['I1', 'I2', 'I3'],
#     title='Time Series Data for I1, I2, I3',
#     ylabel='Current'
# )

# Plot P1, P2, P3, Q1, Q2, Q3 in another figure
# plot_time_series(
#     data=all_data,
#     columns=['P1', 'P2', 'P3', 'Q1', 'Q2', 'Q3'],
#     title='Time Series Data for P1, P2, P3, Q1, Q2, Q3',
#     ylabel='Power'
# )

# plot_time_series(
#     data=all_data,
#     columns=['EP_TOTAL_kWh', 'EQ_TOTAL_kvarh'],
#     title='Time Series Data for EP_Total, EQ_Total',
#     ylabel='Power'
# )
chargers = [
        '3ELMTH01',
        'Alpitronic 50kW',
        'Lincoln Electric 150kW',
        'Liteon IC48A',
        'Zerova 01 - 48A',
        'Zerova 02 - 48A',
        'Zerova 03 - 80A',
        'Zerova 04 - 80A',
        'Zerova 5 (Amphenol)'
        # 'site_power'
        ]

plot_time_series(
    data=cms_df,
    columns=chargers,
    title='Time Series charger data',
    ylabel='kw'
)

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

def plot2_time_series_2data(data, columns, title, ylabel,data2, columns2, title2, ylabel2, colors=None):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 8), sharex=True)

    for col in columns:
        ax1.plot(data.index, data[col], label=col, color=colors[col] if colors and col in colors else None)
    # Hardcoded cms site data
    ax1.plot(data.index, data2['site_power'], label='site_power', color=colors[col] if colors and col in colors else None)
    ax1.set_title(title)
    ax1.set_xlabel('Time')
    ax1.set_ylabel(ylabel)
    ax1.grid(True)
    ax1.legend()

    for col in columns2:
        ax2.plot(data2.index, data2[col], label=col, color=colors[col] if colors and col in colors else None)

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

# plot2_time_series(
#     data=all_data,
#     columns=['Ang_Vb', 'Ang_Vc', 'Ang_Ia', 'Ang_Ib', 'Ang_Ic'],
#     title='Time Series Data for Ang_Vb, Ang_Vc, Ang_Ia, Ang_Ib, Ang_Ic',
#     ylabel='Degree',
#     columns2=['P1', 'P2', 'P3', 'Q1', 'Q2', 'Q3'],
#     title2='Time Series Data for P1, P2, P3, Q1, Q2, Q3',
#     ylabel2='Power',
#     colors=color_map
# )

# plot2_time_series(
#     data=all_data,
#     columns=['I1', 'I2', 'I3'],
#     title='Time Series Data for I1, I2, I3',
#     ylabel='Current',
#     columns2=['Ang_Vb', 'Ang_Vc', 'Ang_Ia', 'Ang_Ib', 'Ang_Ic'],
#     title2='Time Series Data for Ang_Vb, Ang_Vc, Ang_Ia, Ang_Ib, Ang_Ic',
#     ylabel2='Degree',
#     colors=color_map
# )

# plot2_time_series(
#     data=all_data,
#     columns=['I1', 'I2', 'I3'],
#     title='Time Series Data for I1, I2, I3',
#     ylabel='Current',
#     columns2=['THD_Ia', 'THD_Ib', 'THD_Ic', 'THD_Va', 'THD_Vb', 'THD_Vc'],
#     title2='Time Series Data for Ia, Ib, Ic THD',
#     ylabel2='Percentage',
#     colors=color_map
# )

# plot2_time_series(
#     data=all_data,
#     columns=['I1', 'I2', 'I3'],
#     title='Time Series Data for I1, I2, I3',
#     ylabel='Current',
#     columns2=['THD_Ia', 'THD_Ib', 'THD_Ic', 'THD_Va', 'THD_Vb', 'THD_Vc'],
#     title2='Time Series Data for Ia, Ib, Ic THD',
#     ylabel2='Percentage',
#     colors=color_map
# )

plot2_time_series_2data(
    data=all_data,
    columns=['Psum_kW', 'Ssum_kVA'],
    title='Time Series Data for Psum_kW & Ssum_kVA(meter) and site_power(CMS)',
    ylabel='kW',
    data2=cms_df,
    columns2=chargers,
    title2='Time Series Data for different chargers',
    ylabel2='kW',
    colors=color_map
)

# =======Below code has issues, not of the same dimension
# def plot_time_series_2data(data, data2, columns, columns2, title, ylabel, colors=None):
#     plt.figure(figsize=(14, 8))
#     for col in columns:
#         plt.plot(data.index, data[col], label=col)
#     for col in columns2:
#         plt.plot(data.index, data2[col], label=col)
#     plt.title(title)
#     plt.xlabel('Time')
#     plt.ylabel(ylabel)
#     plt.legend()
#     plt.grid(True)
#     plt.tight_layout()

# plot_time_series_2data(
#     data=all_data,
#     columns=['Psum_kW'],
#     data2=cms_df,
#     columns2=chargers,
#     title='Time Series charger data',
#     ylabel='kw'
# )


plt.show(block=False)
input("Press Enter to close the figure...")
plt.close('all')
