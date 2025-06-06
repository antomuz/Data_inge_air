import pandas as pd
import os

# Dossier des données nettoyées
clean_dir = os.path.join(os.getcwd(), "data_clean")

#####################################################################################
#                              ANALYSE N02
#####################################################################################
def analyse_NO2_200_3days():
    print("\n/////////////////////////////////////////////////////////////////////////////////////////////////////")
    print("//         Analyse NO2 - Seuil de recommandation 200 µg/m3 sur 3 jours glissants                    //")
    print("/////////////////////////////////////////////////////////////////////////////////////////////////////\n")

    # Charger le fichier NO2
    df_no2 = pd.read_csv(os.path.join(clean_dir, "NO2_data_TEST.csv"))

    # Forcer format date
    df_no2['date_local'] = pd.to_datetime(df_no2['date_local'])

    # Calculer moyenne journalière par commune, station, date
    df_journalier = df_no2.groupby(['commune', 'station', 'date_local'])['no2_value'].mean().reset_index()

    # Marquer les jours > 200
    seuil_recommandation = 200
    df_journalier['over_200'] = df_journalier['no2_value'] > seuil_recommandation

    # Trier par commune, station, date
    df_journalier = df_journalier.sort_values(by=['commune', 'station', 'date_local'])

    # Appliquer une rolling window de 3 jours (correction avec transform)
    df_journalier['over_200_rolling3'] = (
        df_journalier
        .groupby(['commune', 'station'])['over_200']
        .transform(lambda x: x.rolling(window=3, min_periods=3).sum())
    )

    # Identifier les séquences où les 3 jours sont > 200
    df_journalier_alert = df_journalier[df_journalier['over_200_rolling3'] >= 3]

    print(f"Nombre d'alertes NO2 (200 µg/m3 sur 3 jours glissants) : {len(df_journalier_alert)}\n")
    print("Communes concernées :")
    print(df_journalier_alert['commune'].value_counts())

    # Sauvegarder le résultat
    df_journalier_alert.to_csv(os.path.join(clean_dir, "NO2_alert_200_3days.csv"), index=False)
    print("\nNO2 200 µg/m3 3 jours alerts saved to data_clean/NO2_alert_200_3days.csv\n")



#####################################################################################
#                              ANALYSE PM10
#####################################################################################

##TO DO : A REFAIRE - 
def analyse_PM10():
    print("=== Analyse PM10 ===")
    df_pm10 = pd.read_csv(os.path.join(clean_dir, "PM10_data.csv"))

    # Lignes au-dessus du seuil
    seuil_pm10 = 80
    df_alert_pm10 = df_pm10[df_pm10['pm10_value'] > seuil_pm10]

    print(f"Nombre de dépassements PM10 : {len(df_alert_pm10)}")
    print("Communes concernées (PM10) :")
    print(df_alert_pm10['commune'].value_counts())

    # Sauvegarde éventuelle
    df_alert_pm10.to_csv(os.path.join(clean_dir, "PM10_alerts.csv"), index=False)
    print("PM10 alerts saved to data_clean/PM10_alerts.csv\n")



if __name__ == "__main__":
    analyse_NO2_200_3days()


