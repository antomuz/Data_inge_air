# main.py
from datetime import datetime, timedelta
import extract_data
import process_data
import export_excel

end_date = datetime.now()
start_date = end_date - timedelta(days=1080)

start_date_str = start_date.strftime("%Y-%m-%d")
end_date_str = end_date.strftime("%Y-%m-%d")
print(f"Fetching data from {start_date_str} to {end_date_str}")


#####################################################################################
#                              
#                                    RUN SCRIPT
#
#####################################################################################

# =========  EXTRACT DATAS ========= #
print("Fetching pollution data...")
extract_data.fetch_pollution_data(start_date, end_date)

print("Fetching population data...")
extract_data.fetch_population_data()

print("Fetching enterprise data...")
extract_data.fetch_enterprise_data()

# =========  PROCESSING DATAS ========= #

print("Processing N02 data...")
process_data.process_NO2_data()

print("Processing PM10 data...")
process_data.process_PM10_data()

print("Processing population data...")
process_data.process_population_data()

print("Processing enterprise data...")
process_data.process_enterprise_data()

print("Extraction and processing completed successfully.")

# =========  ANALYSE ========= #

import analyse
analyse.analyse_NO2_200_3days()
analyse.analyse_PM10()

# =========  EXPORT EXCEL ========= #
print("Generating Excel report with graphs...")
export_excel.run_export()
print("Excel export completed.")
