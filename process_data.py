# process_data.py
import os
import json
import pandas as pd

#####################################################################################
#                               GLOBAL VARIABLE
#####################################################################################
script_dir = os.path.dirname(os.path.abspath(__file__))
datas_dir = os.path.join(script_dir, "datas")
clean_dir = os.path.join(script_dir, "data_clean")
os.makedirs(clean_dir, exist_ok=True)  # ensure data_clean exists



#####################################################################################
#                               PROCESSING PM10
#####################################################################################

def process_PM10_data():
    print("Processing PM10 data...")

    # Load JSON
    with open(os.path.join(datas_dir, "PM10_Data.json"), "r", encoding="utf-8") as f:
        data_PM10 = json.load(f)

    # Les données sont sous "results"
    records = data_PM10.get('results', [])

    # Transformer en DataFrame
    df_PM10 = pd.json_normalize(records)

    # === DEBUG : pour mes tests ===
    print("Colonnes PM10 disponibles :")
    print(df_PM10.columns.tolist())

    # Garder uniquement les colonnes utiles
    columns_to_keep = [
        'nom_commune',
        'nom_station',
        'valeur',
        'date_heure_local'
    ]
    df_PM10 = df_PM10[columns_to_keep]

    # === Nettoyage ===
    # Renommer les colonnes pour être plus clair pour Power BI
    df_PM10 = df_PM10.rename(columns={
        'nom_commune': 'commune',
        'nom_station': 'station',
        'valeur': 'pm10_value',
        'date_heure_local': 'date_local'
    })

    # Forcer les types :
    df_PM10['date_local'] = pd.to_datetime(df_PM10['date_local']).dt.date
    df_PM10['pm10_value'] = pd.to_numeric(df_PM10['pm10_value'], errors='coerce')

    df_PM10 = df_PM10.dropna(subset=['pm10_value'])
    # Supprimer les valeurs négatives ou aberrantes
    df_PM10 = df_PM10[df_PM10["pm10_value"] >= 0]
    df_PM10 = df_PM10[df_PM10["pm10_value"] < 1000]


    # === Ajouter la colonne de seuil pour info ===
    df_PM10['seuil_info_recommandation'] = 50  # µg/m³
    df_PM10['seuil_alerte'] = 80  # µg/m³

    # === Sauvegarder le CSV ===
    df_PM10.to_csv(os.path.join(clean_dir, "PM10_data.csv"), index=False)
    print("PM10 data saved to data_clean/PM10_data.csv")



#####################################################################################
#                               PROCESSING N02
#####################################################################################

def process_NO2_data():
    print("Processing NO2 data...")

    # Load JSON
    with open(os.path.join(datas_dir, "NO2_Data.json"), "r", encoding="utf-8") as f:
        data_NO2 = json.load(f)

    # Les données sont sous "results"
    records = data_NO2.get('results', [])

    # Transformer en DataFrame
    df_NO2 = pd.json_normalize(records)

    # === DEBUG : pour mes tests ===
    print("Colonnes NO2 disponibles :")
    print(df_NO2.columns.tolist())

    # Garder uniquement les colonnes utiles
    columns_to_keep = [
        'nom_commune',
        'nom_station',
        'valeur',
        'date_heure_local'
    ]
    df_NO2 = df_NO2[columns_to_keep]

    # Renommer les colonnes
    df_NO2 = df_NO2.rename(columns={
        'nom_commune': 'commune',
        'nom_station': 'station',
        'valeur': 'no2_value',
        'date_heure_local': 'date_local'
    })

    # Forcer les types
    df_NO2['date_local'] = pd.to_datetime(df_NO2['date_local']).dt.date
    df_NO2['no2_value'] = pd.to_numeric(df_NO2['no2_value'], errors='coerce')

    # === SUPPRIMER les lignes où la valeur est null ===
    df_NO2 = df_NO2.dropna(subset=['no2_value'])
    # Supprimer les valeurs négatives ou aberrantes
    df_NO2 = df_NO2[df_NO2["no2_value"] >= 0]
    df_NO2 = df_NO2[df_NO2["no2_value"] < 1000]


    # === Ajouter les seuils réglementaires NO2 ===
    # (source : ton PDF :contentReference[oaicite:0]{index=0})
    df_NO2['seuil_info_recommandation'] = 200  # µg/m³ en moyenne horaire
    df_NO2['seuil_alerte'] = 400  # µg/m³ en moyenne horaire

    # Sauvegarder le CSV
    df_NO2.to_csv(os.path.join(clean_dir, "NO2_data.csv"), index=False)
    print("NO2 data saved to data_clean/NO2_data.csv")


#####################################################################################
#                               PROCESSING POPULATION
#####################################################################################


def process_population_data():
    print("Processing population data...")

    # Load JSON
    with open(os.path.join(datas_dir, "population_data.json"), "r", encoding="utf-8") as f:
        data_population = json.load(f)

    # Les données sont dans 'records' → et les colonnes sont dans 'fields'
    records = data_population.get('records', [])
    # Extraire directement la liste des 'fields'
    fields_list = [record['fields'] for record in records]
    
    # Transformer en DataFrame
    df_population = pd.DataFrame(fields_list)


    # === DEBUG : pour mes tests ===
    print("Colonnes population disponibles :")
    print(df_population.columns.tolist())

    # Garder les colonnes utiles
    columns_to_keep = [
        'nom_de_la_commune',
        'population_totale',
        'tranche_population'
    ]
    df_population = df_population[columns_to_keep]

    # Renommer pour plus de clarté
    df_population = df_population.rename(columns={
        'nom_de_la_commune': 'commune',
        'population_totale': 'population_totale',
        'tranche_population': 'tranche_population'
    })

    # Forcer les types
    df_population['population_totale'] = pd.to_numeric(df_population['population_totale'], errors='coerce')

    # Supprimer les lignes où population_totale est null
    df_population = df_population.dropna(subset=['population_totale'])

    # Sauvegarder le CSV
    df_population.to_csv(os.path.join(clean_dir, "population_data.csv"), index=False)
    print("Population data saved to data_clean/population_data.csv")

#####################################################################################
#                               PROCESSING ENTERPRISE
#####################################################################################


def process_enterprise_data():
    print("Processing enterprise data...")

    # Load JSON
    with open(os.path.join(datas_dir, "enterprise_data.json"), "r", encoding="utf-8") as f:
        data_enterprises = json.load(f)

    # Les données sont dans 'records'
    records = data_enterprises.get('records', [])

    # Extraire directement la liste des 'fields'
    fields_list = [record['fields'] for record in records]

    # Transformer en DataFrame
    df_enterprises = pd.DataFrame(fields_list)

   

    # Garder les colonnes utiles
    columns_to_keep = [
        'libellecommuneetablissement',
        'etatadministratifetablissement',
        'activiteprincipaleetablissement',
        'soussectionetablissement',
        'sectionetablissement',
        'datecreationetablissement',
        'datefermetureetablissement'
    ]
    df_enterprises = df_enterprises[columns_to_keep]

    # Renommer pour plus de clarté
    df_enterprises = df_enterprises.rename(columns={
        'libellecommuneetablissement': 'commune',
        'etatadministratifetablissement': 'etat',
        'activiteprincipaleetablissement': 'activite_principale',
        'soussectionetablissement': 'soussection',
        'sectionetablissement': 'section',
        'datecreationetablissement' : 'date_creation',
        'datefermetureetablissement': 'date_fermeture'
    })

    # === DEBUG : afficher les colonnes ===
    print("Colonnes entreprises disponibles :")
    print(df_enterprises.columns.tolist())

    # Forcer le type date
    df_enterprises['date_fermeture'] = pd.to_datetime(df_enterprises['date_fermeture'], errors='coerce')

    # Sauvegarder le CSV
    df_enterprises.to_csv(os.path.join(clean_dir, "enterprise_data.csv"), index=False)
    print("Enterprise data saved to data_clean/enterprise_data.csv")


#process_PM10_data()
#process_NO2_data()
#process_population_data()
#process_enterprise_data()