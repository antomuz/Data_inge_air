# extract_data.py
import os
import requests
import json


#####################################################################################
#                               GLOBAL VARIABLE
#####################################################################################

# define datas directory
script_dir = os.path.dirname(os.path.abspath(__file__))
datas_dir = os.path.join(script_dir, "datas")

# create it if it does not exist
os.makedirs(datas_dir, exist_ok=True)


#####################################################################################
#
#                               EXTRACT POLLUTION
#
#####################################################################################
def fetch_pollution_data(start_date, end_date):
    date_range = f"{start_date},{end_date}"
    url = "https://data.airpl.org/api/v1/mesure/journaliere/"

    params_PM10 = {
        "code_configuration_de_mesure__code_point_de_prelevement__code_polluant": "24",
        "code_configuration_de_mesure__code_point_de_prelevement__code_station__code_commune__code_departement__in": "44,49,53,72,85,",
        "date_heure_tu__range": date_range,
        "export": "json",
        "format": "json",
    }

    params_NO2 = {
        "code_configuration_de_mesure__code_point_de_prelevement__code_polluant": "03",
        "code_configuration_de_mesure__code_point_de_prelevement__code_station__code_commune__code_departement__in": "44,49,53,72,85,",
        "date_heure_tu__range": date_range,
        "export": "json",
        "format": "json",
    }

    try:
        # Fetch PM10
        response_PM10 = requests.get(url, params=params_PM10)
        response_PM10.raise_for_status()
        data_PM10 = response_PM10.json()

        # Fetch NO2
        response_NO2 = requests.get(url, params=params_NO2)
        response_NO2.raise_for_status()
        data_NO2 = response_NO2.json()

        # Save to JSON      
        with open(os.path.join(datas_dir, "PM10_Data.json"), "w", encoding="utf-8") as f:
            json.dump(data_PM10, f, ensure_ascii=False, indent=4)
        print("PM10 data saved successfully.")

        with open(os.path.join(datas_dir, "NO2_Data.json"), "w", encoding="utf-8") as f:
            json.dump(data_NO2, f, ensure_ascii=False, indent=4)
        print("NO2 data saved successfully.")

    except requests.exceptions.RequestException as e:
        print("An error occurred while fetching pollution data:", e)
    except ValueError as e:
        print("Error decoding JSON:", e)



#####################################################################################
#
#                               EXTRACT POPULATION
#
#####################################################################################


def fetch_population_data():
    url = "https://data.paysdelaloire.fr/api/records/1.0/search/"
    params = {
        "dataset": "12002701600563_population_pays_de_la_loire_2019_communes_epci",
        "rows": 10000,  # limité à max 10000 par le site
        "format": "json"
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data_population = response.json()

        # Save to JSON        
        with open(os.path.join(datas_dir, "population_data.json"), "w", encoding="utf-8") as f:
            json.dump(data_population, f, ensure_ascii=False, indent=4)
        print("Population data saved successfully.")

    except requests.exceptions.RequestException as e:
        print("An error occurred while fetching population data:", e)
    except ValueError as e:
        print("Error decoding JSON:", e)



#####################################################################################
#
#                               EXTRACT ENTERPRISE
#
#####################################################################################



def fetch_enterprise_data():
    url = "https://data.paysdelaloire.fr/api/records/1.0/search/"
    params = {
        "dataset": "120027016_base-sirene-v3-ss",
        "rows": 10000,  # limité à max 10000 par le site
        "format": "json",
        "where": 'datecreationetablissement > "2024-01-01"',
        }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data_enterprises = response.json()

        # Save to JSON
        with open(os.path.join(datas_dir, "enterprise_data.json"), "w", encoding="utf-8") as f:
            json.dump(data_enterprises, f, ensure_ascii=False, indent=4)
        print("Enterprise data saved successfully.")

    except requests.exceptions.RequestException as e:
        print("An error occurred while fetching enterprise data:", e)
    except ValueError as e:
        print("Error decoding JSON:", e)


