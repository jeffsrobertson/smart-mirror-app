from kivy.lang import Builder
from kivy.app import App
from kivy.uix.modalview import ModalView
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.properties import BooleanProperty,NumericProperty,DictProperty,ObjectProperty,AliasProperty
from kivy.logger import Logger

import json
from time import time
from functools import partial

Builder.load_string('''
<CityFinderDialog>:
    size_hint: (.9,.67)
    pos_hint: {'center_x':.5,'center_x':.5}
    rv: rv
    layout: layout
    textinput: textinput
    BoxLayout:
        spacing: dp(5)
        padding: dp(5)
        orientation: 'vertical'
        TextInput:
            id: textinput
            readonly: True
            font_size: .5*self.height
            hint_text: 'Type the name of a city'
            multiline: False
            focus: True
            size_hint: (1,.1)
            pos_hint: {'center_x':.5,'top':1}
            on_text: 
                layout.selected_city_info = {}
                layout.selected_index = None
                root.populate_list()
        RecycleView:
            id: rv
            viewclass: 'CityFinderRow'
            size_hint: (1,.75)
            pos_hint: {'center_x':.5}
            CityFinderLayout:
                id: layout
                default_size_hint: 1,None
                default_size: None,.15*rv.height
                size_hint_y: None
                height: self.minimum_height
                orientation: 'vertical'
        BoxLayout:
            size_hint: (1,.15)
            orientation: 'horizontal'
            spacing: dp(5)
            padding: dp(2)
            Button:
                disabled: True if layout.selected_index==None else False
                text: 'Select'
                on_release: 
                    root.dispatch('on_select')
            Button:
                text: 'Cancel'
                on_release: root.dismiss()
         
<CityFinderRow>:
    canvas.before:
        Color:
            rgba: (.0, .1, .9, .3) if self.selected else (0, 0, 0, 1)
        Rectangle:
            pos: self.pos
            size: self.size
    text: ''

''')


class CityFinderLayout(LayoutSelectionBehavior, RecycleBoxLayout):
    selected_city_info = {}
    selected_index = NumericProperty(None,allownone=True)

    # Triggered when a row is clicked
    def select_with_touch(self, city_info, node, touch=None):

        # Catch city id and index
        self.selected_city_info = city_info
        self.selected_index = node
        super(CityFinderLayout,self).select_with_touch(node,touch)
        # Goes to self.apply_selection() after this

    # Runs any time a row is clicked OR when a row appears/disappears from view
    def apply_selection(self, index, view, is_selected):

        # If this row is the selected one, load it as such
        if index == self.selected_index:
            super(CityFinderLayout, self).apply_selection(index, view, True)
        else:
            super(CityFinderLayout, self).apply_selection(index, view, False)
        # runs CityFinderRow().apply_selection() after this


class CityFinderRow(RecycleDataViewBehavior, Label):
    selected = BooleanProperty(False)

    # Triggered when rows are loaded initially, or when rows appear/disappear from view
    def refresh_view_attrs(self, rv, index, data):
        self.index = index
        super(CityFinderRow, self).refresh_view_attrs(rv, index, data)

    # If row is clicked
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            return self.parent.select_with_touch(self.city_info,self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        if is_selected:
            self.selected = True
        else:
            self.selected = False


class CityFinderDialog(ModalView):

    __events__ = ('on_select',)

    def on_open(self):

        # Load json into memory if not there
        self.load_json_into_memory()
        self.textinput.readonly = False

    def load_json_into_memory(self):
        with open('dialogs/city_list.json') as f:
            ts = time()
            self.city_list = json.load(f)
            Logger.info('Loaded json in {:.3f} seconds.'.format(time()-ts))

    def populate_list(self):

        # 1. Only create list if search is 2 or more chars
        search = self.textinput.text.lower()
        if len(search) < 2:
            self.rv.data = []
            return

        # 2. Create list
        list_of_cities = []
        for city in self.city_list:
            if (city["name"].lower()).startswith(search):
                list_of_cities.append(city)

        # 3. Alphabetize
        list_of_cities.sort(key=lambda k: k['name'])

        # 4. Make list of city names and their dict of info
        self.rv.data = [{'text': city['name'], 'city_info':city} for city in list_of_cities]

    def get_city_info(self, *args):
        return self.layout.selected_city_info
    selected_city_info = AliasProperty(get_city_info, None)

    def on_select(self, *args):
        self.dismiss()


if __name__ == '__main__':
    from kivy.app import App
    from kivy.uix.floatlayout import FloatLayout

    class MainApp(App):
        c = ObjectProperty()

        def build(self):
            r = FloatLayout()
            b = Button(size_hint=(.5, .1), pos_hint={'center_x': .5, 'y': .1}, text='Press to open popup')
            self.c = CityFinderDialog()
            self.c.bind(on_select=self.save_city_info)
            b.bind(on_release=self.c.open)
            r.add_widget(b)
            return r

        def save_city_info(self, *args):
            city_info = self.c.selected_city_info
            print('selected city: ', city_info)
    MainApp().run()
