from __future__ import print_function
from datetime import date, datetime, timedelta
from dateutil import parser, relativedelta
from time import mktime

from crispy_calendar import CrispyCalendar
from crispy_maps import CrispyMaps


def main():
    """
    Main loop
    """
    ccal = CrispyCalendar()
    cmaps = CrispyMaps()
    
    events = ccal.get_next_ten_events()

    for event in events:
        driving_time = None
        
        if not event['all_day'] and event['location']:
            cmaps.calculate_driving_times(event)
            
        print(event['start'])
        print("    {} - {}".format(event['summary'], event['location']))
        if event.get('duration_seconds', None):
            print("    Driving time: {}".format(event['duration_text']))
            print("    Departure Time: {}".format(str(event['departure_datetime'])))

               
if __name__ == '__main__':
    main()
