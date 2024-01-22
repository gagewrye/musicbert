import os
import json

# Path to the directory containing composer folders
base_dir = '/Users/gage/Desktop/musicbert/composers'
# Dictionary to hold file ID to composer mappings
file_composer_map = {}

# Loop through each composer's folder
for composer in os.listdir(base_dir):
    composer_path = os.path.join(base_dir, composer)

    # Ensure it's a directory
    if os.path.isdir(composer_path):
        for midi_file in os.listdir(composer_path):
            if midi_file.lower().endswith(('.mid', '.midi')):
                # Extract file ID
                file_id = os.path.splitext(midi_file)[0]
                file_composer_map[file_id] = composer

# Write the mappings to a JSON file
with open('midi_composer_map.json', 'w') as json_file:
    json.dump(file_composer_map, json_file, indent=4)

print("JSON file created with {} mappings.".format(len(file_composer_map)))
