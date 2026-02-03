import requests
import googlemaps
from datetime import datetime

def fetch_nearby_stores(address, API_KEY_CLOUD, kassal_header):
    kassal_url = "https://kassal.app/api/v1/physical-stores"
    gmaps = googlemaps.Client(key=API_KEY_CLOUD)
    
    # Geocode the address
    geocode_result = gmaps.geocode(address)
    
    if geocode_result:
        location = geocode_result[0]['geometry']['location']
        lat = location['lat']
        lng = location['lng']
    else:
        print("Location not found")
        return None, None

    params = {
        "lat": lat,
        "lng": lng,
        "km": 10
    }

    try:
        response = requests.get(kassal_url, headers=kassal_header, params=params)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        data = response.json()
        unique_stores = []
        for store in data["data"]:
            if store.get("name", "N/A") not in unique_stores:
                unique_stores.append(store.get("name", "N/A"))
        return unique_stores
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

def find_distance(unique_stores, address, API_KEY_CLOUD):
    gmaps = googlemaps.Client(key=API_KEY_CLOUD)

    stores = []

    for i in unique_stores:
        destination = i
        
        # Request walking directions
        directions_result = gmaps.directions(
            address,
            destination,
            mode="walking",  # We want to walk
            units="metric"   # Type of mesurement
        )

        # Extract distance and duration
        if directions_result:
            route = directions_result[0]
            #print(route)
            leg = route['legs'][0]
            distance = leg['distance']['value']
            duration = leg['duration']['text']
            stores.append([destination, distance, duration])

    
    
    return stores

def fetch_ingridients(dinner):
    with open("Oppskrifter.txt", "r") as file:
        lines = file.readlines()
    
    ingridients = []
    found_recepie = False
    print(lines)

def find_ingridients(kassal_header):
    kassal_url = " https://kassal.app/api/v1/products"

    params = {
        "search": "chicken",
        "sort": "price_asc"
    }

    try:
        response = requests.get(kassal_url, headers=kassal_header, params=params)
        response.raise_for_status()  # Raises an HTTPError for bad responses
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None


if __name__ == "__main__":
    address = "Kråkstadveien 7A, Norway"

    with open('../keys/CLOUD_KEY.txt', 'r') as file:
        API_KEY_CLOUD = file.read().strip()

    with open('../keys/KASSAL_KEY.txt', 'r') as file:
        API_KEY_KASSAL = file.read().strip()

    kassal_header = {
        "Authorization": f"Bearer {API_KEY_KASSAL}"
    }

    unique_stores = fetch_nearby_stores(address, API_KEY_CLOUD, kassal_header)

    find_ingridients(API_KEY_KASSAL)
    
    #stores = find_distance(unique_stores, address, API_KEY_CLOUD)

    #dinner = "Marry_Me_Chicken"

    #ingridients = fetch_ingridients(dinner)

    #for i in stores:
    #    print(i)

    

