from __future__ import print_function
from datetime import date, datetime, timedelta
from dateutil import parser, relativedelta
from time import mktime

from crispy_calendar import CrispyCalendar
from crispy_maps import CrispyMaps


def epoch_to_datetime(epoch_timestamp):
    return datetime.fromtimestamp(epoch_timestamp, tz=settings.TIMEZONE) if epoch_timestamp else None


def datetime_to_epoch(dt):
    """
    :param dt: Can be a datetime or datetime.date object
    :return: Integer representing the unix epoch timestamp
    """
    return int(mktime(dt.timetuple()))


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
            start_datetime = parser.parse(event['start'])
            driving_time = cmaps.get_driving_time(event['location'],
                                                 datetime_to_epoch(start_datetime))
            departure_datetime = start_datetime + relativedelta.relativedelta(seconds=-driving_time['seconds'])
            alert_datetime = departure_datetime + relativedelta.relativedelta(minutes=-15)
           
        print(event['start'])
        print("    {} - {}".format(event['summary'], event['location']))
        if driving_time:
            print("    Driving time: {}".format(driving_time['text']))
            print("    Departure Time: {}".format(str(departure_datetime)))

               
if __name__ == '__main__':
    main()
