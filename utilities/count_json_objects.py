import os
import json

def count_json_objects(folder_path):
    total_count = 0
    
    # Iterate through all files in the specified directory
    for filename in os.listdir(folder_path):
        if filename.endswith('.json'):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                try:
                    # Load the JSON data and count the number of objects
                    data = json.load(file)
                    total_count += len(data)
                except json.JSONDecodeError as e:
                    print(f"Error reading {filename}: {e}")
    
    return total_count

# Specify the folder path containing the JSON files
folder_path = 'weddingbazaar/photographers/json_loc_data'  # Change this to your folder path
total_objects = count_json_objects(folder_path)

print(f"Total number of objects in JSON files: {total_objects}")
