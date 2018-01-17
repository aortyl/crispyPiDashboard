import googlemaps
import json
import os

class CrispyMaps:
    
    ORIGIN_ADDR = '1010 Brookview Drive, Pennsburg, PA'

    def __init__(self):
        self.gmaps = googlemaps.Client(key=os.environ['GOOGLE_MAPS_API_KEY'])

    def get_driving_time(self, destination, arrival_time):
        matrix = self.gmaps.distance_matrix(self.ORIGIN_ADDR,
                                            destination,
                                            arrival_time= arrival_time,
                                            mode='driving')

        rows = matrix.get('rows', [])

        if rows:
            elements = rows[0].get('elements', [])

            if elements:
                duration_text = elements[0]['duration']['text']
                duration_seconds = elements[0]['duration']['value']

                return {'seconds': duration_seconds, 'text': duration_text }
        
        return None
