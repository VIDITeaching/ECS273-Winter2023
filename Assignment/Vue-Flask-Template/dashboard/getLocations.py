import json
import requests

# Load JSON object from file
with open('cities.json', 'r') as infile:
    data = json.load(infile)

# Your API key
api_key = "AIzaSyCQhfWWEQHvRRXIBtceMnS9RIyymNb2Rog"
# print(data)
# Iterate over the cities in the JSON object
for city in data["cities"]:
    try:
    # print(city["name"])
        # Form the request url
        url = f"https://maps.googleapis.com/maps/api/geocode/json?address={city['name']}&key={api_key}"
        # Send the request to the API
        response = requests.get(url)
        # Parse the response
        response_json = response.json()
        # Get the latitude and longitude from the response
        city["latitude"] = response_json["results"][0]["geometry"]["location"]["lat"]
        city["longitude"] = response_json["results"][0]["geometry"]["location"]["lng"]
    except:
        print(city["name"])
# Save the updated JSON object to file
with open('citiesWithCoords.json', 'w') as outfile:
    json.dump(data, outfile)