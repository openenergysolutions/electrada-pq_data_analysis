# Meter Data Analysis Tools

This repository contains a collection of Python scripts for analyzing meter data.

## Installation

No installation is required. Simply ensure you have Python 3.x installed with the following dependencies:
- pandas
- matplotlib
- numpy

## Data Preparation
1. Download the logger data from the meter's online portal, it will be a list of `.gz` files, create a folder under `./data` and move them there
2.Extract compressed data files:

```bash
# Extract .gz files in a specific directory
python prepare_data.py /path/to/gz/files

# If no directory is specified, current directory is used
python prepare_data.py
```


## Analysis Scripts

### Individual Analysis Tools
#### 1. Consumption Analysis and Visualization

Use `process.py` to calculate and visualize energy consumption metrics:

```bash
python process.py /path/to/data/directory
```

This script:
- Loads data from CSV files
- Calculates daily and weekly energy consumption
- Generates time series plots


#### 2. CMS Data Comparison

Use `cms_data.py` to compare meter measurements with CMS (Charger Management System) data:

```bash
python cms_data.py /path/to/data/directory
```

This script:
- Loads meter data and aligns it with CMS data(reading CMS data is hardcoded now)
- Visualizes power meter readings vs. CMS site power
- Shows individual charger power consumption
- Displays percentage differences between measurements

#### 3. Power Relationship Analysis

Use `check_data.py` to analyze power relationships, THD values, and phase metrics:

```bash
python check_data.py /path/to/data/directory
```

This script loads CSV files, analyzes power relationship metrics (S vs P/Q), and generates visualizations showing:
- Differences between S1 and √(P1² + Q1²)
- Phase power values (P1, P2, P3, Q1, Q2, Q3)
- Measured vs calculated apparent power (S)
- THD values

