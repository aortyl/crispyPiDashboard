from __future__ import print_function

from crispy_calendar import CrispyCalendar

def main():
    """
    Main loop
    """
    ccal = CrispyCalendar()
    events = ccal.get_next_ten_events()

    for event in events:
        print(event['start'])
        print("    {} - {}".format(event['summary'], event['location']))


if __name__ == '__main__':
    main()
