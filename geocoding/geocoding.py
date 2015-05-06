# Geocoding 

import geopy

from geopy.geocoders import Nominatim

geolocator = Nominatim()

location = geolocator.geocode("203 Finch Ave East Toronto")
print(location.address)

print((location.latitude, location.longitude))

    
    