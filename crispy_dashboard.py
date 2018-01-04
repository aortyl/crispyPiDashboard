from __future__ import print_function

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
        driving_time = cmaps.get_driving_time(event['location']) if event['location'] else None
           
        print(event['start'])
        print("    {} - {}".format(event['summary'], event['location']))
        if driving_time:
            print("    Driving time: {}".format(driving_time['text']))


if __name__ == '__main__':
    main()
