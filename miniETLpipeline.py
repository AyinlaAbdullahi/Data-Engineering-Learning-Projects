#to create the csv file

import csv
from pathlib import Path
from random import randint, choice
from faker import Faker
import json

fake = Faker()
csv_file = Path("workers.csv")
headers = ["id", "first_name", "last_name", "salary", "department"]
departments = ["Engineering", "Marketing", "HR", "Finance", "Sales", "Support"]

rows = []
for i in range(1, 1001):
    row = [
        i,
        fake.first_name(),
        fake.last_name(),
        round(randint(3000, 10000) + randint(0, 99)/100, 2),
        choice(departments)
    ]
    rows.append(row)

with open(csv_file, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(headers)
    writer.writerows(rows)

print(f"CSV file created: {csv_file}")


#mini ETL Pipepline
json_file = Path("workers.json")

def extract(csv_path):
    if not csv_path.exists():
        raise FileNotFoundError(f"{csv_path} not found")
    with open(csv_path, newline='') as f:
        reader = csv.DictReader(f)
        data = [row for row in reader]
    return data

def transform(data):
    for row in data:
        row['id'] = int(row['id'])
        row['salary'] = float(row['salary'])
    return data

def load(data, json_path):
    with open(json_path, 'w') as f:
        json.dump(data, f, indent=4)

def etl_pipeline(csv_path, json_path):
    data = extract(csv_path)
    data = transform(data)
    load(data, json_path)
    print("ETL pipeline completed successfully!")

etl_pipeline(csv_file, json_file)

