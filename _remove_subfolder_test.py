import os
import shutil

# Replace with the path to your parent directory
parent_dir = './'

for subfolder in os.listdir(parent_dir):
    subfolder_path = os.path.join(parent_dir, subfolder)
    if os.path.isdir(subfolder_path):
        csv_file_name = subfolder + ".csv"  # Assuming the CSV file name matches the subfolder name
        csv_file_path = os.path.join(subfolder_path, csv_file_name)
        if os.path.isfile(csv_file_path):
            destination_path = os.path.join(parent_dir, csv_file_name)
            # Remove destination file if it exists to overwrite it
            if os.path.exists(destination_path):
                os.remove(destination_path)
                print(f"Removed existing file: {destination_path}")
            # Move the CSV file to the parent directory
            shutil.move(csv_file_path, destination_path)
            # Remove the now-empty subfolder
            os.rmdir(subfolder_path)
            print(f"Moved {csv_file_name} to {parent_dir} and deleted {subfolder}")
        else:
            print(f"No CSV file named {csv_file_name} in {subfolder}")