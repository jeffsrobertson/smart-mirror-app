from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty,ListProperty,ObjectProperty,BooleanProperty,NumericProperty


# Custom imports
from widgets.basewidget import ScatterBase


class ToDoListWidget(ScatterBase):

    # Settings
    enable_title = BooleanProperty(True)
    title = StringProperty('To Do')
    to_do_list = ListProperty(['this','is'])
    to_do_list_completed = ListProperty([True,False])
    completed_style = StringProperty('checkbox')
    number_style = StringProperty('number')

    # No touchy
    to_do_layout = ObjectProperty()
    update_interval = NumericProperty(300)

    def initialize(self,*args):

        #1. Title settings
        if not self.enable_title:
            self.ids['title'].font_size = 0
            # Need to make title not the 'seed widget' before i can implement this

        #2. Dynamically build list
        for l in range(len(self.to_do_list)):

            new_list_item = ToDoListItem(checked=self.to_do_list_completed[l],
                                         number=int(l+1),
                                         description=self.to_do_list[l])
            self.to_do_layout.add_widget(new_list_item)

    def update(self,*args):
        pass

class ToDoListItem(BoxLayout):
    checked = BooleanProperty()
    number = NumericProperty()
    description = StringProperty()
