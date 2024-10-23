# DB QUERY GENERATOR

This project processes site data from a CSV file, categorizes the data based on the indoor/outdoor/lamp pole/NA classification, and generates SQL queries to update a database. The generated queries update the `indoor_outdoor_type_id` field in the `site` table in batches of 300.

## Table of Contents
- [Project Overview](#project-overview)
- [Technologies Used](#technologies-used)
- [File Structure](#file-structure)
- [How to Use](#how-to-use)
  - [Pre-requisites](#pre-requisites)
  - [Running the Script](#running-the-script)
- [Configuration](#configuration)
- [Output](#output)

## Project Overview

This script reads a CSV file containing information about different sites, particularly their classification into categories: `Indoor`, `Outdoor`, `Lamp Pole`, or `NA`. It maps these categories to corresponding enumerations, then groups the data based on this classification. Finally, it generates SQL `UPDATE` queries in batches of 300 to modify the `indoor_outdoor_type_id` for the respective sites in the database.

## Technologies Used

- **Python 3**
  - `pandas`: For reading and manipulating CSV data.
  - `Enum`: To manage site classifications (Indoor, Outdoor, Lamp Pole, NA).
  - File I/O: To generate and store SQL queries in text files.

## How to Use
### Pre-requisites

- **Python 3** installed on your system.
- Install the required Python packages using `pip`:
  ```bash
  pip install pandas
  ```

### Running the Script

1. **Prepare the CSV file**: Ensure the input CSV file (`import.csv`) is placed in the same directory as the script. The CSV file must contain the following columns:
   - `Site ID`: Unique identifier for each site.
   - `Indoor/Outdoor`: Specifies whether the site is "Indoor", "Outdoor", "Lamp Pole", or `NA`.

2. **Run the script**:
   ```bash
   python generate_queries.py
   ```

3. The script will:
   - Map each `Indoor/Outdoor` value to its corresponding enumeration.
   - Group the data by category (Indoor, Outdoor, Lamp Pole, NA).
   - Generate SQL `UPDATE` queries in batches of 300 for each category.
   - Write the generated queries into text files:
     - `update_indoor_new.txt`
     - `update_outdoor_new.txt`
     - `update_lamp_pole_new.txt`
     - `update_na_new.txt`

## Configuration

- **CSV file format**: The input CSV must contain `Site ID` and `Indoor/Outdoor` columns.
- **Site Categories**:
  - **Indoor**: Mapped to `indoor_outdoor_type_id = 1`
  - **Outdoor**: Mapped to `indoor_outdoor_type_id = 2`
  - **Lamp Pole**: Mapped to `indoor_outdoor_type_id = 4`
  - **NA**: Mapped to `indoor_outdoor_type_id = 3`

## Output

- The generated SQL queries are written to the following text files:
  - `update_indoor_new.txt`: Contains SQL queries for Indoor sites.
  - `update_outdoor_new.txt`: Contains SQL queries for Outdoor sites.
  - `update_lamp_pole_new.txt`: Contains SQL queries for Lamp Pole sites.
  - `update_na_new.txt`: Contains SQL queries for NA sites.

Each query updates the `indoor_outdoor_type_id` for up to 300 sites at a time.

## Example

**Sample SQL query generated for Indoor sites**:

```sql
UPDATE `site` SET `indoor_outdoor_type_id`=1 WHERE `site_id` IN ('SiteID1','SiteID2','SiteID3', ..., 'SiteID300')
```

**Sample SQL query for remaining Indoor sites (if fewer than 300)**:

```sql
UPDATE `site` SET `indoor_outdoor_type_id`=1 WHERE `site_id` IN ('SiteID301', 'SiteID302', ..., 'SiteID350')
```

## License

This project is open-source and available for modification and distribution under the MIT License.
```

### Instructions:

1. Replace `import.csv` with the actual CSV filename if it differs.
2. Update the project name and details as needed.
3. The "License" section assumes an MIT License; modify this according to your project's license if needed.

This `README.md` will guide any user through the setup and execution of your script!
