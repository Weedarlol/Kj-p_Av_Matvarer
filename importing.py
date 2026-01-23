import requests
import googlemaps
from datetime import datetime

def fetch_nearby_stores(address, API_KEY_CLOUD, API_KEY_KASSAL):
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

    headers = {
        "Authorization": f"Bearer {API_KEY_KASSAL}"
    }

    params = {
        "lat": lat,
        "lng": lng,
        "km": 10
    }

    try:
        response = requests.get(kassal_url, headers=headers, params=params)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        data = response.json()
        unique_stores = []
        for store in data["data"]:
            # Extract specific fields
            if store.get("name", "N/A") not in unique_stores:
                unique_stores.append(store.get("name", "N/A"))
        return unique_stores
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None


def find_distance(unique_stores, address, API_KEY_CLOUD):
    # Replace with your API key
    gmaps = googlemaps.Client(key=API_KEY_CLOUD)

    stores = []

    for i in unique_stores:
        destination = i
        
        # Request walking directions
        directions_result = gmaps.directions(
            address,
            destination,
            mode="walking",  # Specify walking mode
            avoid="ferries", # Optional: avoid ferries if needed
            units="metric"   # Use 'imperial' for miles
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



if __name__ == "__main__":
    address = "Kråkstadveien 7A, Norway"

    API_KEY_CLOUD = 'AIzaSyC65V2O-yb2SUoxx_FxEyoZ2fSTMcHGN7U'
    API_KEY_KASSAL = 'J7pwxRQLc1n3CrqpLFjObxciLEeXlrdSNef6cm6p'

    unique_stores = fetch_nearby_stores(address, API_KEY_CLOUD, API_KEY_KASSAL)
    
    stores = find_distance(unique_stores, address, API_KEY_CLOUD)

    for i in stores:
        print(i)

    

