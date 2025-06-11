# /// script
# dependencies = [
#   "pandas",
#   "openpyxl",
# ]
# ///

"""
This script calculates the number of plants that have thermal storage
in Spain using the cspguru/cspdata database.

This script should be run with:
`uv run scripts/csp_with_thermal_storage_spain.py`
"""

import pandas as pd
from pathlib import Path

data_path: Path = Path(__file__).parent / "csp_data.xlsx"
if not data_path.exists():
    raise FileNotFoundError(f"Data file not found: {data_path}")
# Load the data from the Excel file
df = pd.read_excel(data_path, sheet_name="csp-guru")

# Count the number of plants with a thermal storage larger than 2 hours. Return:
# - the percentage of plants with thermal storage larger than 2 hours.
# - the total number of plants with thermal storage larger than 2 hours.

plants_with_storage = df[df["Storage_capacity_hours"] > 2]
total_plants = len(df)
plants_with_storage_count = len(plants_with_storage)
percentage_with_storage = (plants_with_storage_count / total_plants) * 100
print(f"Total number of plants with thermal storage larger than 2 hours: {plants_with_storage_count} out of {total_plants}")
print(f"Percentage of plants with thermal storage larger than 2 hours: {percentage_with_storage:.2f}%")