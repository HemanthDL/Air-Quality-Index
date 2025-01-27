import csv
import os

# Function to read data from a city CSV file and append the city name
def read_city_data(city_file, city_name):
    data = []
    with open(city_file, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            row['city'] = city_name
            data.append(row)
    return data

# List of city CSV files and their corresponding city names
city_files = [
    {'file': 'Mysuru.csv', 'name': 'Mysuru'},
    {'file': 'Bengaluru.csv', 'name': 'Bengaluru'},
    {'file': 'Chikkamagaluru.csv', 'name': 'Chikkamagaluru'},
    {'file': 'Mangaluru.csv', 'name': 'Mangaluru'},
    {'file': 'Hassan.csv', 'name': 'Hassan'},
    {'file': 'Kolar.csv', 'name': 'Kolar'},
]


combined_data = []
for city in city_files:
    city_data = read_city_data(city['file'], city['name'])
    combined_data.extend(city_data)


output_file = 'KACities.csv'
with open(output_file, 'w', newline='') as csvfile:
    fieldnames = ['date', 'aqi', 'co', 'no', 'no2', 'o3', 'so2', 'pm2_5', 'pm10', 'nh3', 'city']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(combined_data)

print(f"Combined data written to {output_file} successfully.")
