import kivy
kivy.require('1.10.1')

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.listview import ListView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

from crispy_event_service  import CrispyEventService


class EventScreen(GridLayout):

    def __init__(self, **kwargs):
        self.crispy = CrispyEventService()

        kwargs['cols'] = 2
        super(EventScreen, self).__init__(**kwargs)

        refresh_events_button = Button(text='Refresh Events')
        refresh_events_button.bind(on_press=self.button_refresh_events)
        self.add_widget(refresh_events_button)

        events = []

        for event in self.crispy.get_all_stored_events():
            events.append("""{}: {} {}""".format(event.start_time_display(),
                                                       event.data['summary'],
                                                       event.data['location']))

        self.event_list_view = ListView(item_strings=events)
        self.add_widget(self.event_list_view)


    def button_refresh_events(self, instance):
        events = []
        for event in self.crispy.refresh_10_days_of_events():
            events.append("""{}: {} {}""".format(event.start_time_display(),
                                                       event.data['summary'],
                                                       event.data['location']))
        self.event_list_view.item_strings = events

class CrispyDashboard(App):

    def build(self):
        return EventScreen()


if __name__ == '__main__':
    CrispyDashboard().run()
