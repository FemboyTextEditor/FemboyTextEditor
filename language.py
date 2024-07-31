import json
import os

def apply_language_settings():
    # Define the name of the JSON file
    json_filename = "editor_config.json"

    # Check if the JSON file exists
    if not os.path.exists(json_filename):
        print(f"JSON file '{json_filename}' does not exist. Language settings cannot be applied.")
        return {}

    # Load the JSON data
    with open(json_filename, 'r') as json_file:
        data = json.load(json_file)

    # Retrieve the language setting
    language = data.get("language", "en_us")

    # Determine the language settings
    if language == "de_ge":
        return {"save_text": "Speichern", "open_text": "Öffnen"}
    elif language == "ru_ru":
        return {"save_text": "Сохранять", "open_text": "Открыть"}
    else:
        return {"save_text": "Save", "open_text": "Open"}

# Get the language settings
language_settings = apply_language_settings()

# Output the settings as JSON to stdout
print(json.dumps(language_settings))
