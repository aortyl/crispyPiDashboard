import kivy
kivy.require('1.10.1')

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.listview import ListView
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

from crispy_event_service  import CrispyEventService


class EventScreen(GridLayout):

    def __init__(self, **kwargs):
        crispy = CrispyEventService()
        kwargs['cols'] = 2
        super(EventScreen, self).__init__(**kwargs)

        events_display = []
        for event in crispy.get_all_stored_events():
            events_display.append("""{}: {} {}""".format(event.start_time_display(),
                                                       event.data['summary'],
                                                       event.data['location']))

        list_view = ListView(item_strings=events_display)

        self.add_widget(list_view)


class CrispyDashboard(App):

    def build(self):
        return EventScreen()


if __name__ == '__main__':
    CrispyDashboard().run()
