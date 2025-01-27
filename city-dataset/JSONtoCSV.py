import json
import csv


with open('Mangaluru.txt', 'r') as txt_file:
    json_data = txt_file.read()


json_data = json_data.replace("'", '"')

#parsing json data to python dir
data = json.loads(json_data)


with open('Mangaluru.csv', 'w', newline='') as csvfile:
    fieldnames = ['date', 'aqi', 'co', 'no', 'no2', 'o3', 'so2', 'pm2_5', 'pm10', 'nh3']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()

    for item in data['list']:
        writer.writerow({
            'date': item['dt'],
            'aqi': item['main']['aqi'],
            'co': item['components']['co'],
            'no': item['components']['no'],
            'no2': item['components']['no2'],
            'o3': item['components']['o3'],
            'so2': item['components']['so2'],
            'pm2_5': item['components']['pm2_5'],
            'pm10': item['components']['pm10'],
            'nh3': item['components']['nh3']
        })

print("Data written successfully.")
