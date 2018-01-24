from __future__ import print_function
from datetime import date, datetime, timedelta
from dateutil import parser, relativedelta
from time import mktime, sleep

from crispy_event_service  import CrispyEventService


def main():
    """
    Main loop
    """
    c_events = CrispyEventService()

    while True:
        events = c_events.get_next_x_days_of_events(10)

        for event in events:
            driving_time = None

            if not event.data['all_day'] and event.data['location']:
                c_events.calculate_driving_times(event)

            print(event.start_time_display())
            print("    {} - {}".format(event.data['summary'], event.data['location']))
            if event.data.get('duration_seconds', None):
                print("    Driving time: {}".format(event.data['duration_text']))
                print("    Departure Time: {}".format(str(event.data['departure_datetime'])))

        print('*************************')
        print('Displaying all Old Events')

        for event in c_events.get_past_stored_events():
            print("{} - {}".format(event.start_time_display(), event.data['id']))

        print('*************************')
        print('Deleting all Old Events')
        c_events.delete_all_past_events()

        sleep(60) # delay for 1 minute

if __name__ == '__main__':
    main()
