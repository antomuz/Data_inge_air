import os
import requests
import json
from datetime import datetime

# Prompt user for start and end dates
start_date = input("Enter the start date (YYYY-MM-DD): ")
end_date = input("Enter the end date (YYYY-MM-DD): ")

# Optional: Validate the date format
# This will raise a ValueError if the format is incorrect
try:
    datetime.fromisoformat(start_date)  # e.g. "2024-01-31"
    datetime.fromisoformat(end_date)
except ValueError:
    print("Invalid date format! Please use YYYY-MM-DD.")
    exit(1)
    
# Build the date range string
date_range = f"{start_date},{end_date}"
    
# Base endpoint
url = "https://data.airpl.org/api/v1/mesure/journaliere/"

# Define your query parameters in a dict
params_PM10 = {
    "code_configuration_de_mesure__code_point_de_prelevement__code_polluant": "24",
    "code_configuration_de_mesure__code_point_de_prelevement__code_station__code_commune__code_departement__in": "44,49,53,72,85,",
    "date_heure_tu__range": date_range,
    "export": "json",
    "format": "json",
}

# Define your query parameters in a dict
params_NO2 = {
    "code_configuration_de_mesure__code_point_de_prelevement__code_polluant": "03",
    "code_configuration_de_mesure__code_point_de_prelevement__code_station__code_commune__code_departement__in": "44,49,53,72,85,",
    "date_heure_tu__range": date_range,
    "export": "json",
    "format": "json",
}

try:
    # Make the GET requests
    response_PM10 = requests.get(url, params=params_PM10)
    response_PM10.raise_for_status()  # Raises HTTPError if the request returned an unsuccessful status code
    
    response_NO2 = requests.get(url, params=params_PM10)
    response_NO2.raise_for_status()  # Raises HTTPError if the request returned an unsuccessful status code
    
    # Parse the JSON data
    data_PM10 = response_PM10.json()
    data_NO2 = response_NO2.json()
    
    # Specify the file path
    script_dir = os.path.dirname(os.path.abspath(__file__))  
    file_path_PM10 = os.path.join(script_dir,"PM10_Data.json")
    file_path_NO2 = os.path.join(script_dir,"NO2_Data.json")
    
    # Save data to a JSON file
    with open(file_path_PM10, "w", encoding="utf-8") as f:
        json.dump(data_PM10, f, ensure_ascii=False, indent=4)
    
    print(f"Data successfully saved to {file_path_PM10}")
    
    with open(file_path_NO2, "w", encoding="utf-8") as f:
        json.dump(data_NO2, f, ensure_ascii=False, indent=4)
    
    print(f"Data successfully saved to {file_path_NO2}")

except requests.exceptions.RequestException as e:
    print("An error occurred while making the request:", e)
except ValueError as e:
    print("Error decoding JSON:", e)

