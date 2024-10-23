import pandas as pd
import json
from enum import Enum

# Define the Enum for IndoorOutdoor
class IndoorOutdoor(Enum):
    INDOOR = 1
    OUTDOOR = 2
    LAMP_POLE = 4
    NA = 3

# text file to store the queries
def write_to_file(file_name, data):
    with open(file_name, 'a') as f:
        for item in data:
            f.write(f"{item}\n")

# Function to map Indoor/Outdoor values to the Enum
def map_enum(value):
    if pd.isna(value):  # Check for NaN values
        return IndoorOutdoor.NA.value
    elif value == "Indoor":
        return IndoorOutdoor.INDOOR.value
    elif value == "Outdoor":
        return IndoorOutdoor.OUTDOOR.value
    elif value == "Lamp Pole":
        return IndoorOutdoor.LAMP_POLE.value
    else:
        return IndoorOutdoor.NA.value

# Read the CSV file
try:
    data = pd.read_csv('import.csv')
except FileNotFoundError:
    print("Error: 'import.csv' file not found.")
    exit()

# Check if required columns exist
required_columns = ['Site ID', 'Indoor/Outdoor']
if not all(col in data.columns for col in required_columns):
    print(f"Error: CSV file does not contain the required columns: {required_columns}")
    exit()

# Map the Indoor/Outdoor column to the Enum
data['IndoorOutdoorEnum'] = data['Indoor/Outdoor'].apply(map_enum)

# Convert the DataFrame to JSON format
json_data = data[['Site ID', 'IndoorOutdoorEnum']].to_json(orient='records')

# Print the resulting JSON
# print(json_data)

# category sites with IndoorOutdoorEnum
category = data.groupby('IndoorOutdoorEnum').size()
print(category)

# get the count of each category
category_count = category.to_dict()
print(category_count)

# generate sql query for NA data to update the database, max site count: 300
na_data = data[data['IndoorOutdoorEnum'] == 3]
print(na_data)

site_count = 0
site_ids = []
for index, row in na_data.iterrows():
    site_ids.append(row['Site ID'])
    site_count += 1
    if site_count == 300:
        query = f"UPDATE `site` SET `indoor_outdoor_type_id`=3 WHERE `site_id` IN ({','.join(f'\'{site_id}\'' for site_id in site_ids)})"
        print(query)
        write_to_file('update_na_new.txt', [query])
        site_count = 0
        site_ids = []

# Check for remaining sites after the loop
if site_ids:
    query = f"UPDATE `site` SET `indoor_outdoor_type_id`=3 WHERE `site_id` IN ({','.join(f'\'{site_id}\'' for site_id in site_ids)})"
    print(query)
    write_to_file('update_na_new.txt', [query])
