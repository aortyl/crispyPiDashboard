import googlemaps
import json
import os
import httplib2

from datetime import date, datetime, timedelta
from dateutil import parser, relativedelta
from time import mktime
from pytz import timezone

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

from google.cloud import firestore

def epoch_to_datetime(epoch_timestamp):
    return datetime.fromtimestamp(epoch_timestamp, tz=timezone('US/Eastern')) if epoch_timestamp else None


def datetime_to_epoch(dt):
    """
    :param dt: Can be a datetime or datetime.date object
    :return: Integer representing the unix epoch timestamp
    """
    return int(mktime(dt.timetuple()))


class CrispyEvent:

    def __init__(self, data):
        self.db = firestore.Client()
        self.data = data


    def save(self):
        doc_ref = self.db.collection('events').document(self.data['id'])
        doc_ref.set(self.data)
        return self


    def delete(self):
        self.db.collection('events').document(self.data['id']).delete()


    def start_time_display(self):
        return epoch_to_datetime(self.data['start']).isoformat()


class CrispyEventService:
    ORIGIN_ADDR = '1010 Brookview Drive, Pennsburg, PA'
    # If modifying these scopes, delete your previously saved credentials
    # at ~/.credentials/calendar-python-quickstart.json
    SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
    CLIENT_SECRET_FILE = 'client_secret.json'
    APPLICATION_NAME = 'Crispy Calendar'

    def __init__(self):
        self.gmaps = googlemaps.Client(key=os.environ['GOOGLE_MAPS_API_KEY'])
        self.db = firestore.Client()

        credentials = self.get_calendar_credentials()
        http = credentials.authorize(httplib2.Http())
        self.service = discovery.build('calendar', 'v3', http=http)


    def get_calendar_credentials(self):
        """Gets valid user credentials from storage.

        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.

        Returns:
            Credentials, the obtained credential.
        """
        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir,
                                       'calendar-python-quickstart.json')

        store = Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(self.CLIENT_SECRET_FILE, self.SCOPES)
            flow.user_agent = self.APPLICATION_NAME
            if flags:
                credentials = tools.run_flow(flow, store, flags)
            else: # Needed only for compatibility with Python 2.6
                credentials = tools.run(flow, store)
            print('Storing credentials to ' + credential_path)
        return credentials

    def get_past_stored_events(self):
        docs = self.db.collection('events') \
            .where('start', '<', datetime_to_epoch(datetime.now())) \
            .get()

        for doc in docs:
            yield CrispyEvent(doc.to_dict())


    def delete_all_past_events(self):
        for event in self.get_past_stored_events():
            event.delete()

    def get_next_x_days_of_events(self, days):
        now = datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
        now_plus_days = (datetime.utcnow() + relativedelta.relativedelta(days=days)).isoformat() + 'Z'
        print("Getting events for the next {} days".format(days))
        event_results = self.service.events().list(
            calendarId='primary',
            timeMin=now,
            timeMax=now_plus_days,
            singleEvents=True,
            orderBy='startTime').execute()

        return self.__process_google_calendar_event_results(event_results)


    def get_next_x_events(self, count):
        """
        Gets the next X events from the calendar.
        """
        now = datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
        print("Getting the upcoming {} events".format(count))
        events_result = self.service.events().list(
            calendarId='primary',
            timeMin=now,
            maxResults=count,
            singleEvents=True,
            orderBy='startTime').execute()

        return self.__process_google_calendar_event_results(event_results)


    def __process_google_calendar_event_results(self, g_event_results):
        events = g_event_results.get('items', [])

        formatted_events = []

        for event in events:
            c_event = CrispyEvent({'id':event['id'],
                                  'start':datetime_to_epoch(parser.parse(event['start'].get('dateTime', event['start'].get('date')))),
                                  'all_day':True if 'date' in event['start'] else False,
                                  'summary':event['summary'],
                                  'location':event.get('location', '')}).save()

            formatted_events.append(c_event)

        return formatted_events


    def calculate_driving_times(self, crispy_event):

        rows = self.gmaps.distance_matrix(self.ORIGIN_ADDR,
                                          crispy_event.data['location'],
                                          arrival_time= crispy_event.data['start'],
                                          mode='driving').get('rows', [])

        if rows:
            elements = rows[0].get('elements', [])

            if elements:
                crispy_event.data['duration_text'] = elements[0]['duration']['text']
                crispy_event.data['duration_seconds'] = elements[0]['duration']['value']
                crispy_event.data['departure_datetime'] = epoch_to_datetime(crispy_event.data['start']) + relativedelta.relativedelta(seconds= -crispy_event.data['duration_seconds'])
                crispy_event.data['alert_datetime'] = crispy_event.data['departure_datetime'] + relativedelta.relativedelta(minutes=-15)

                crispy_event.save()

        return crispy_event
