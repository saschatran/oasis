import shutil
import os

# Specify the paths to your folders A and B
folder_a = '/usr/src/oasisabm'
folder_b = '/usr/local/lib/python3.8/site-packages/oasisabm'

# List all files in folder A
files_in_a = os.listdir(folder_a)

for file_name in files_in_a:
    # Construct the full file paths for the source and destination
    source_file = os.path.join(folder_a, file_name)
    destination_file = os.path.join(folder_b, file_name)

    # Check if it's a file and not a directory
    if os.path.isfile(source_file):
        # Copy the file from folder A to folder B, overwriting if exists
        shutil.copy2(source_file, destination_file)
        print(f"Copied {file_name} to {folder_b}")

print("All files from folder A have been copied to folder B.")
