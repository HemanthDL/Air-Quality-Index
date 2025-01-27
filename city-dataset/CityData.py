import requests


url = "http://api.openweathermap.org/data/2.5/air_pollution/history"

#api parameters
params = {
    "lat": 12.9141,
    "lon": 74.8560,
    "start": 1514764800,  # Start timestamp in Unix format
    "end": 1681838166,      # End timestamp in Unix format
    "appid": "d824318da122bd110425cba0029fa108"      # Your API key from OpenWeatherMap
}

#api call
response = requests.get(url, params=params)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # extract json data from response
    data = response.json()
    with open("Mangaluru.txt", "w") as file:
        file.write(str(data))
else:
    print("Error:", response.status_code)
