# Your API KEYS (you need to use your own keys - very long random characters)
import urllib.parse
import urllib.request
from config import MAPBOX_TOKEN, MBTA_API_KEY
import json
from pprint import pprint

# Useful URLs (you need to add the appropriate parameters for your requests)
MAPBOX_BASE_URL = "https://api.mapbox.com/geocoding/v5/mapbox.places"
MBTA_BASE_URL = "https://api-v3.mbta.com/stops"


# A little bit of scaffolding if you want to use it


def get_json(url: str) -> dict:
    """
    Given a properly formatted URL for a JSON web API request, return a Python JSON object containing the response to that request.

    Both get_lat_long() and get_nearest_station() might need to use this function.
    """
    with urllib.request.urlopen(url) as f:
        response_text = f.read().decode('utf-8')
        response_data = json.loads(response_text)
        return response_data



def get_lat_long(place_name: str) -> tuple[str, str]:
    """
    Given a place name or address, return a (latitude, longitude) tuple with the coordinates of the given place.

    See https://docs.mapbox.com/api/search/geocoding/ for Mapbox Geocoding API URL formatting requirements.
    """
    #urllib.parse converts the user string input into url form 
    query = urllib.parse.quote_plus(place_name, safe='', encoding=None, errors=None)
    url=f'{MAPBOX_BASE_URL}/{query}.json?access_token={MAPBOX_TOKEN}&types=poi'

    #call the function get_json to return json object
    json_output = get_json(url)

    #this function will return a tuple of the geometric coordinates of the user's location
    #IMPORTANT!!! the output returns [Longitude, Latitude] <- we need to switch this over to get the nearest station!!!
    if(json_output['features']):
        return json_output['features'][0]['geometry']['coordinates']
    else:
        raise Exception("Address entered does not exist")


def get_nearest_station(latitude: str, longitude: str) -> tuple[str, bool]:
    """
    Given latitude and longitude strings, return a (station_name, wheelchair_accessible) tuple for the nearest MBTA station to the given coordinates.

    See https://api-v3.mbta.com/docs/swagger/index.html#/Stop/ApiWeb_StopController_index for URL formatting requirements for the 'GET /stops' API.
    """
    URL = f'https://api-v3.mbta.com/stops?api_key={MBTA_API_KEY}&sort=distance&filter%5Blatitude%5D={latitude}&filter%5Blongitude%5D={longitude}'
    json_output = get_json(URL)

    #check if the user's input has a MBTA nearby, then check if it is wheelchair accessible - checks whether wheelchair_boarding > 0
    have_stops = True
    if (len(json_output['data'])) == 0:
        have_stops == False
        return have_stops
    else:
        if (json_output['data'][0]['attributes']['wheelchair_boarding']) > 0:
            wheelchair_accessible = True
        else:
            wheelchair_accessible = False

        return((json_output['data'][0]['attributes']['name'], wheelchair_accessible))


def find_stop_near(place_name: str) -> tuple[str, bool]:
    """
    Given a place name or address, return the nearest MBTA stop and whether it is wheelchair accessible.

    This function might use all the functions above.
    """

    #call get_lat_long function to get the latitude and longitude first 
    #get the nearest station based on the lat and long values obtained, passing it into the nearest_stop function
    lat_long = get_lat_long(place_name)
    nearest_stop = get_nearest_station(lat_long[1], lat_long[0])

    #if the nearest stop is boolean shows that there is no stop nearby, ensure the returned message is dynamic. 
    if type(nearest_stop) is bool:
        return f"Unfortunately there are no MBTA stops close enough to {place_name} - you have to get out into the city!"

    else:
        if nearest_stop[1] == True:
            message = "Yes"
        else:
            message = "No"

        output = f"Nearest MBTA station: {nearest_stop[0]} | Wheelchair Accessible : {message} |"

        return output
    
# use openWeather API to obtain the weather at the user's input location ss
def get_weather(place_name):
    lat_long = get_lat_long(place_name)
    APIKEY = '2d7b5c8cba9bfa9036774e2462b3ddb4'
    url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat_long[1]}&lon={lat_long[0]}&appid={APIKEY}'

    f = urllib.request.urlopen(url)
    response_text = f.read().decode('utf-8')
    response_data = json.loads(response_text)
    # print(response_data)

    current_temp = response_data['main']['temp']
    return current_temp


def main(): 
    """
    You can test all the functions here
    """
    # print(get_lat_long('B'))
    #print(get_nearest_station(42.3737614375,-71.1181085))
    # print(find_stop_near("boston commons"))
    # print(get_weather('Harvard University'))


if __name__ == '__main__':
    main()
