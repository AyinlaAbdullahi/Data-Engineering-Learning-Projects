import csv
import json
from pathlib import Path

csv_file = Path("employees.csv")
json_file = Path("employees.json")


data = []

with csv_file.open(newline="", encoding="utf-8") as csvFile:
    reader = csv.DictReader(csvFile)
    for row in reader:
        data.append(row)
        
with json_file.open("w", encoding="utf-8") as jsonFile:
    json.dump(data,jsonFile, indent=4 )





import csv
import json
from pathlib import Path
from datetime import datetime

csv_file = Path("employees.csv")
json_file = Path("employees.json")

if not csv_file.exists():
    raise FileNotFoundError("CSV file does not exist")

SCHEMA = {
    "id": int,
    "first_name": str,
    "last_name": str,
    "email": str,
    "age": int,
    "department": str,
    "role": str,
    "country": str,
    "salary": int,
    "hire_date": lambda v: datetime.strptime(v, "%Y-%m-%d").date().isoformat()
}

def apply_schema(row, schema):
    clean_row = {}
    for field, converter in schema.items():
        value = row.get(field)
        if value in (None, ""):
            clean_row[field] = None
        else:
            clean_row[field] = converter(value)
    return clean_row

converted_rows = []

with csv_file.open(newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        converted_rows.append(apply_schema(row, SCHEMA))

with json_file.open("w", encoding="utf-8") as f:
    json.dump(converted_rows, f, indent=4)

print("Done")
