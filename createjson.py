import json
import os


def create_json_file():
    # Define the name of the JSON file
    json_filename = "editor_config.json"

    # Check if the file already exists
    if os.path.exists(json_filename):
        print(f"JSON file '{json_filename}' already exists. No new file created.")
        return

    # Define the data you want to store in the JSON file
    data = {
        "language": "en_us",
        "theme": "dark"
    }

    # Create the JSON file
    with open(json_filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)

    print(f"JSON file '{json_filename}' created successfully.")


# Run the function to create the JSON file
create_json_file()
