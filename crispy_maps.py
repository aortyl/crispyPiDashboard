import googlemaps
import json
import os

from datetime import date, datetime, timedelta
from dateutil import parser, relativedelta
from time import mktime

from google.cloud import firestore

class CrispyMaps:
    
    ORIGIN_ADDR = '1010 Brookview Drive, Pennsburg, PA'

    def __init__(self):
        self.gmaps = googlemaps.Client(key=os.environ['GOOGLE_MAPS_API_KEY'])
        self.db = firestore.Client()


    def calculate_driving_times(self, crispy_event):
        rows = self.gmaps.distance_matrix(self.ORIGIN_ADDR,
                                          crispy_event['location'],
                                          arrival_time= crispy_event['start'],
                                          mode='driving').get('rows', [])
        
        if rows:
            elements = rows[0].get('elements', [])

            if elements:
                crispy_event['duration_text'] = elements[0]['duration']['text']
                crispy_event['duration_seconds'] = elements[0]['duration']['value']

                #TODO - Should I be modifying crispy_event here or doc_ref?
                doc_ref = self.db.collection('events').document(crispy_event['id'])

                crispy_event['departure_datetime'] = parser.parse(crispy_event['start']) + relativedelta.relativedelta(seconds=-crispy_event['duration_seconds'])
                crispy_event['alert_datetime'] = crispy_event['departure_datetime'] + relativedelta.relativedelta(minutes=-15)
                
                doc_ref.set(crispy_event)

        return crispy_event


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


    def epoch_to_datetime(epoch_timestamp):
        return datetime.fromtimestamp(epoch_timestamp, tz=settings.TIMEZONE) if epoch_timestamp else None


    def datetime_to_epoch(dt):
        """
        :param dt: Can be a datetime or datetime.date object
        :return: Integer representing the unix epoch timestamp
        """
        return int(mktime(dt.timetuple()))
