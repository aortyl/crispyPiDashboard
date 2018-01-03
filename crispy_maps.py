import googlemaps
import json
import os

gmaps = googlemaps.Client(key=os.environ['GOOGLE_MAPS_API_KEY'])

ORIGIN_ADDR = 'Pennsburg, PA'
DEST_ADDR = 'New York City,NY'

matrix = gmaps.distance_matrix(ORIGIN_ADDR, DEST_ADDR, mode='driving')

rows = matrix.get('rows', [])

if rows:
    elements = rows[0].get('elements', [])

    if elements:
        duration_text = elements[0]['duration']['text']
        duration_seconds = elements[0]['duration']['value']

        print("Travel time from {} to {} is {}".format(ORIGIN_ADDR, DEST_ADDR, duration_text))

