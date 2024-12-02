import os
import gzip
import shutil

# Get a list of all .gz files in the current directory
gz_files = [f for f in os.listdir('.') if f.endswith('.gz')]

for gz_file in gz_files:
    # Determine the output file name
    output_file = gz_file[:-3]  # Remove the .gz extension
    print(f"Unzipping {gz_file} to {output_file}...")
    
    # Unzip the file
    with gzip.open(gz_file, 'rb') as f_in:
        with open(output_file, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

print("All files have been unzipped.")