import os
import json

def combine_json_files(folder_path):
    combined_data = []
    
    # Iterate through all files in the specified directory
    for filename in os.listdir(folder_path):
        if filename.endswith('.json'):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                try:
                    # Load the JSON data and extend the combined_data list
                    data = json.load(file)
                    combined_data.extend(data)
                except json.JSONDecodeError as e:
                    print(f"Error reading {filename}: {e}")
    
    return combined_data

# Specify the folder path containing the JSON files
folder_path = 'weddingbazaar/venues/json_loc_data'  # Change this to your folder path
combined_list = combine_json_files(folder_path)

# Optionally, save the combined list to a new JSON file
output_file = 'weddingbazaar/venues/combined/combined_venues_data.json'
with open(output_file, 'w', encoding='utf-8') as outfile:
    json.dump(combined_list, outfile, ensure_ascii=False, indent=4)

print(f"Combined JSON data saved to {output_file}")
