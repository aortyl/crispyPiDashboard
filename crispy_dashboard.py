import kivy
kivy.require('1.10.1')

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.listview import ListView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

from crispy_event_service  import CrispyEventService

from kivy.lang import Builder
from kivy.uix.recycleview import RecycleView


Builder.load_string('''
<CustButton@Button>:
    font_size: 16

<EventScreen>:
    id: eventscreen
    events: events

    BoxLayout:
        spacing: 10
        padding: 10

        CustButton:
            text: "Refresh"
            on_press: eventscreen.button_refresh_events()

    RecycleView:
        id: events
        viewclass: 'Label'
        RecycleBoxLayout:
            default_size: None, dp(56)
            default_size_hint: 1, None
            size_hint_y: None
            height: self.minimum_height
            orientation: 'vertical'


''')


class EventScreen(BoxLayout):

    def __init__(self, **kwargs):
        super(EventScreen, self).__init__(**kwargs)
        self.crispy = CrispyEventService()

        self.build_events(self.crispy.get_all_stored_time_series_events)

        for date, events in self.crispy.get_all_stored_time_series_events().items():
            print("{}:".format(date))
            for event in events:
                print("    {}".format(event.data['summary']))


    def button_refresh_events(self):
        self.build_events(self.crispy.refresh_10_days_of_events)


    def build_events(self, event_yielding_method):
        self.events.data = []
        for date, events in event_yielding_method().items():
            self.events.data.append({'text': date})
            for event in events:
                self.events.data.append({'text': event.get_display_description()})

class CrispyDashboard(App):

    def build(self):
        return EventScreen()


if __name__ == '__main__':
    CrispyDashboard().run()
