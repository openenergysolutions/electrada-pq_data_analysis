#!/usr/bin/env python3
"""
Simple GZ File Extraction Script

This script finds and extracts all .gz files in the specified directory.

Usage:
    python prepare_data.py /path/to/gz/files

"""

import os
import sys
import gzip
import shutil
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def unzip_gz_files(directory='.'):
    """Unzip all .gz files in the specified directory."""
    if not os.path.isdir(directory):
        logger.error(f"Directory not found: {directory}")
        return False
        
    # Get a list of all .gz files in the directory
    gz_files = [f for f in os.listdir(directory) if f.endswith('.gz')]
    
    if not gz_files:
        logger.info(f"No .gz files found in {directory}")
        return False
        
    for gz_file in gz_files:
        try:
            # Determine the output file name
            output_file = gz_file[:-3]  # Remove the .gz extension
            gz_path = os.path.join(directory, gz_file)
            output_path = os.path.join(directory, output_file)
            
            logger.info(f"Unzipping {gz_file} to {output_file}...")
            
            # Unzip the file
            with gzip.open(gz_path, 'rb') as f_in:
                with open(output_path, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
                    
        except Exception as e:
            logger.error(f"Error processing {gz_file}: {str(e)}")
            continue
    
    logger.info(f"Finished unzipping files in {directory}")
    return True

if __name__ == "__main__":
    # Check if directory argument is provided
    if len(sys.argv) > 1:
        target_dir = sys.argv[1]
        logger.info(f"Processing .gz files in directory: {target_dir}")
        unzip_gz_files(target_dir)
    else:
        logger.info("No directory specified, using current directory")
        unzip_gz_files('.')
    
    logger.info("All .gz files have been processed") 