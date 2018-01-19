from __future__ import print_function
from datetime import date, datetime, timedelta
from dateutil import parser, relativedelta
from time import mktime

from crispy_calendar import CrispyCalendar
from crispy_maps import CrispyMaps
from crispy_event_service  import CrispyEventService


def main():
    """
    Main loop
    """
    c_events = CrispyEventService()

    events = c_events.get_next_ten_events()

    for event in events:
        driving_time = None

        if not event.data['all_day'] and event.data['location']:
            c_events.calculate_driving_times(event)

        print(event.data['start'])
        print("    {} - {}".format(event.data['summary'], event.data['location']))
        if event.data.get('duration_seconds', None):
            print("    Driving time: {}".format(event.data['duration_text']))
            print("    Departure Time: {}".format(str(event.data['departure_datetime'])))


if __name__ == '__main__':
    main()
