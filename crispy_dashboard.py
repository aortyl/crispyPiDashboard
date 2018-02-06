import kivy
kivy.require('1.10.1')

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.listview import ListView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

from crispy_event_service  import CrispyEventService

from kivy.lang import Builder
from kivy.uix.recycleview import RecycleView


Builder.load_string('''
<RV>:
    viewclass: 'Label'
    RecycleBoxLayout:
        default_size: None, dp(56)
        default_size_hint: 1, None
        size_hint_y: None
        height: self.minimum_height
        orientation: 'vertical'
''')

class RV(RecycleView):
    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)
        self.crispy = CrispyEventService()

        # self.data = [{'text': str(x)} for x in range(100)]
        self.data = []

        for event in self.crispy.get_all_stored_events():
            self.data.append({'text': "{}: {} {}".format(event.start_time_display(),
                                                       event.data['summary'],
                                                       event.data['location'])})


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
        return RV()


if __name__ == '__main__':
    CrispyDashboard().run()
