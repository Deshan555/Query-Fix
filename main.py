import pandas as pd
import json
from enum import Enum


# Define the Enum for IndoorOutdoor
class IndoorOutdoor(Enum):
    INDOOR = 1
    OUTDOOR = 2
    LAMP_POLE = 4
    NA = 3


# Text file to store the queries
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


# Function to generate and write SQL update queries
def generate_and_write_queries(data, indoor_outdoor_value, file_name):
    site_count = 0
    site_ids = []

    for index, row in data.iterrows():
        site_ids.append(row['Site ID'])
        site_count += 1
        if site_count == 300:
            query = f"UPDATE `site` SET `indoor_outdoor_type_id`={indoor_outdoor_value} WHERE `site_id` IN ({','.join(f'\'{site_id}\'' for site_id in site_ids)})"
            print(query)
            write_to_file(file_name, [query])
            site_count = 0
            site_ids = []

    # Write remaining records if they are less than 300
    if site_ids:
        query = f"UPDATE `site` SET `indoor_outdoor_type_id`={indoor_outdoor_value} WHERE `site_id` IN ({','.join(f'\'{site_id}\'' for site_id in site_ids)})"
        print(query)
        write_to_file(file_name, [query])


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

# Category sites with IndoorOutdoorEnum
category = data.groupby('IndoorOutdoorEnum').size()
print(category)

# Get the count of each category
category_count = category.to_dict()
print(category_count)

# Process Indoor data and generate queries
indoor_data = data[data['IndoorOutdoorEnum'] == IndoorOutdoor.INDOOR.value]
generate_and_write_queries(indoor_data, IndoorOutdoor.INDOOR.value, 'update_indoor_new.txt')

# Process Outdoor data and generate queries
outdoor_data = data[data['IndoorOutdoorEnum'] == IndoorOutdoor.OUTDOOR.value]
generate_and_write_queries(outdoor_data, IndoorOutdoor.OUTDOOR.value, 'update_outdoor_new.txt')

# Process Lamp Pole data and generate queries
lamp_pole_data = data[data['IndoorOutdoorEnum'] == IndoorOutdoor.LAMP_POLE.value]
generate_and_write_queries(lamp_pole_data, IndoorOutdoor.LAMP_POLE.value, 'update_lamp_pole_new.txt')

# Process NA data and generate queries
na_data = data[data['IndoorOutdoorEnum'] == IndoorOutdoor.NA.value]
generate_and_write_queries(na_data, IndoorOutdoor.NA.value, 'update_na_new.txt')
