# Kivy imports
from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.screenmanager import Screen,ScreenManager
from kivy.properties import *
from kivy.core.window import Window
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.button import Button
from kivy.uix.modalview import ModalView
from kivy.storage.dictstore import DictStore
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.animation import Animation
from kivy.uix.scatter import Scatter
from kivy.uix.togglebutton import ToggleButton
from kivy.graphics import Color, Line
from kivy.core.text import LabelBase
from kivy.logger import Logger
from kivy.uix.widget import Widget


# Python packages
import pickle
import socket
import struct
import threading
import time
import json
from copy import deepcopy
from functools import partial

# Custom mirror widgets
from widgets import *
from dialogs import *


LabelBase.register(name="RobotoCondensed",
                    fn_regular="fonts/RobotoCondensed-Regular.ttf",
                    fn_bold="fonts/RobotoCondensed-Bold.ttf",
                    fn_italic="fonts/RobotoCondensed-LightItalic.ttf",
                    fn_bolditalic="fonts/RobotoCondensed-BoldItalic.ttf")
LabelBase.register(name="BebasNeue",
                   fn_regular="fonts/BebasNeue-Regular.ttf")

MAX_CONFIGS = 10
LIST_OF_WIDGETS = ['Time','Weather','ToDoList','Clock']
#,'Clock','News','Quotes''Calendar','Greeting','Compliments','Canvas','Texts','Picture Album','Commute']

TIME_WIDGET = {'type':'Time',
               'name':'Time',
               'position':(0,0),
               'magnitude':1.0,
               'tilt':0,
               'autotime':False,
               'city_id':5128638,
               'alignment':'left',
               'enable_military':False,
               'enable_seconds':True,
               'date_format':1,
               'enable_location':False}
WEATHER_WIDGET = {'type':'Weather',
                  'name':'Weather',
                  'position':(0,0),
                  'magnitude':1.0,
                  'tilt':0,
                  'autolocation':False,
                  'city_id':5128638,
                  'city_name':'New York',
                  'metric_units':True,
                  'display_units':False,
                  'display_location':True,
                  'display_forecast':True,
                  'forecast_days':1}
TODOLIST_WIDGET = None #TODO
CLOCK_WIDGET = {'type':'Clock',
                'name':'Clock',
                'enable_seconds':True}
WIDGET_SETTINGS = {'Time':TIME_WIDGET,'Weather':WEATHER_WIDGET,'ToDoList':TODOLIST_WIDGET,'Clock':CLOCK_WIDGET}

MIRROR_SETTINGS = {'enable_portrait':False,
                   'brightness':50}

WIDGET_FONT = 'RobotoCondensed'
APP_FONT = 'BebasNeue'

SWITCH_OFF = 'images/switch_off.png'
SWITCH_ON = 'images/switch_on.png'


Builder.load_string('''
#: import Factory kivy.factory.Factory

#: import APP_FONT __main__.APP_FONT
#: import SWITCH_OFF __main__.SWITCH_OFF
#: import SWITCH_ON __main__.SWITCH_ON

<RootLayout>:
    header: header
    manager: screen_manager
    nav_bar: nav_bar
    Header:
        id: header
        back_button: back_button
        wifi: wifi
        canvas:
            Color:
                rgba: .67,.816,.95,1
            Rectangle:
                size: self.size
                pos: (0,0)
        size_hint: (1,.075)
        pos_hint: {'top': 1}
        Label:
            pos_hint: {'center_x':.5,'center_y':.5}
            text: header.title
            bold: True
            size_hint: (None,None)
            size: self.texture_size
            font_size: .7*header.height
        Button:
            id: back_button
            background_normal: 'images/back_button.png'
            background_down: 'images/back_button_pressed.png'
            border: [0,0,0,0]
            size_hint: (None,1)
            width: self.height
            on_release: 
                app.root.manager.transition.direction = 'right'
                app.root.manager.change_screen(header.previous_screen)
        IconWithCaption:
            id: wifi
            source: 'images/wifi_off.png'
            caption: 'Offline'
            font_color: [.75,.75,.75,1]
            pos_hint: {'right':.95,'top':.95}
            size_hint: (None,None)
            width: .65*header.height
    Manager:
        id: screen_manager
        size_hint: (1,None)
        height: root.height-header.height
        mirror_select_screen: mirror_select_screen
        config_screen: config_screen
        layout_screen: layout_screen
        widgets_screen: widgets_screen
        mirror_settings_screen: mirror_settings_screen
        misc_screen: misc_screen
        time_widget_screen: time_widget_screen
        weather_widget_screen: weather_widget_screen
        clock_widget_screen: clock_widget_screen
        MirrorSelectScreen:
            id: mirror_select_screen
            name: 'mirror_select_screen'
            manager: screen_manager        
        ConfigScreen:
            id: config_screen
            name: 'config_screen'
            manager: screen_manager
        LayoutScreen:
            id: layout_screen
            name: 'layout_screen'
            manager: screen_manager
        WidgetsScreen:
            id: widgets_screen
            name: 'widgets_screen'
            manager: screen_manager
        MirrorSettingsScreen:
            id: mirror_settings_screen
            name: 'mirror_settings_screen'
            manager: screen_manager
        MiscScreen:
            id: misc_screen
            name: 'misc_screen'
            manager: screen_manager
        TimeWidgetScreen:
            id: time_widget_screen
            name: 'time_widget_screen'
            manager: screen_manager
        WeatherWidgetScreen:
            id: weather_widget_screen
            name: 'weather_widget_screen'
            manager: screen_manager
        ClockWidgetScreen:
            id: clock_widget_screen
            name: 'clock_widget_screen'
            manager: screen_manager
    NavBar:
        id: nav_bar
        pos_hint: {'center_x':.5,'top':0}

<MirrorSelectButton>:
    size_hint: (1,None)
    height: .1*app.root.height
    pos_hint: {'center_x':.5}
    background_normal: 'images/mirrorbuttonup.png'
    background_down: 'images/mirrorbuttondown.png'
    background_held: 'images/mirrorbuttondown.png'
    IconWithCaption:
        id: wifi_icon
        source: 'images/wifi_on.png' if root.online else 'images/wifi_off.png'
        caption: 'Online' if root.online else 'Offline'
        font_color: [71/256,149/256,236/256,1] if root.online else [.75,.75,.75,1]
        pos_hint: {'right':.9,'center_y':.55}
        size_hint: (None,None)
        width: .6*root.height
    Label:
        id: name
        text: root.mirror_name
        font_size: .5*root.height
        font_name: APP_FONT
        color: [.67,.816,.95,1] if root.online else [.75,.75,.75,1]
        pos_hint: {'center_x':.4,'center_y':.5}
        size_hint: (None,None)
        size: self.texture_size
        outline_width: 1
        outline_color: [0,0,0]


<ConfigButton>:
    size_hint: (1,None)
    height: .1*app.root.height
    pos_hint: {'center_x':.5}
    font_size: .5*self.height
    font_name: APP_FONT
    bold: True
    background_normal: 'images/mirrorbuttonup.png'
    background_down: 'images/mirrorbuttondown.png'
    background_held: 'images/mirrorbuttondown.png'
    CheckBox:
        id: active_checkbox
        size_hint: (None,.9)
        width: self.height
        pos_hint: {'right': 1,'center_y':.5}
        background_radio_normal: 'images/config_checkbox_norm.png'
        background_radio_down: 'images/config_checkbox_active.png'
        group: 'config_buttons'
        state: 'down' if root.active_config else 'normal'
        on_active: root.update_active_config()    
    Label:
        id: name
        text: root.config_name
        font_size: .5*root.height
        font_name: APP_FONT
        size_hint: (None,None)
        height: root.height
        width: root.width-active_checkbox.width
        pos_hint: {'center_y':.5}
        center_x: (root.width-active_checkbox.width)/2
        outline_width: 1
        outline_color: [0,0,0]
        
<WidgetButton>:
    size_hint: (1,None)
    height: .1*app.root.height
    pos_hint: {'center_x':.5}
    font_size: .5*self.height
    font_name: APP_FONT
    bold: True
    background_normal: 'images/mirrorbuttonup.png'
    background_down: 'images/mirrorbuttondown.png'
    background_held: 'images/mirrorbuttondown.png'
    Label:
        id: name
        text: root.widget_name
        font_size: .5*root.height
        font_name: APP_FONT
        size_hint: (None,None)
        height: root.height
        width: root.width
        pos_hint: {'center_x':.5,'center_y':.5}
        outline_width: 1
        outline_color: [0,0,0]

<NewButton>:
    size_hint: (1,None)
    height: .1*app.root.height
    pos_hint: {'center_x':.5}
    font_size: .5*self.height
    background_normal: 'images/new_button_normal.png'
    background_down: 'images/new_button_pressed.png'
    font_name: APP_FONT
    
<RefreshButton>:
    Image:
        id: refresh_icon
        source: 'images/refresh.png'
        pos_hint: {'right':.9,'center_y': .55}
        size_hint: (.1,None)

<CustomPopup>:
    background: 'images/popupbg.png'
    border: [30,30,30,30]
    font_color: [.67,.816,.95,1]

<WarningDialog>:
    size_hint: (.9,None)
    height: .6*self.width
    pos_hint: {'center_x':.5,'center_y':.5}
    fill_color: [.67,.816,.95,1]
    outline_color: [1,1,1,1]
    outline_width: .005*app.root.height
    button_height: .08*app.root.height
    title_height: .05*app.root.height
    background_color: 0,0,0,.7
    background: 'images/transparent.png'
    auto_dismiss: False
    RelativeLayout:
        canvas:
            Color:
                rgba: [1,1,1,1]
            RoundedRectangle:
                size: self.size
                radius: [(30,30),(30,30),(30,10),(30,30)]
            Color:
                rgba: root.outline_color
            RoundedRectangle:
                size: self.size
                radius: [(30,30),(30,30),(30,10),(30,30)]
            Color:
                rgba: root.fill_color
            RoundedRectangle:
                size: (self.width-2*root.outline_width,self.height-2*root.outline_width)
                pos: (root.outline_width,root.outline_width)
                radius: [(30,30),(30,30),(30,10),(30,30)]        
            Color:
                rgba: root.outline_color
            Line:
                points: [0,root.button_height,self.width,root.button_height]
                width: .5*root.outline_width
                cap: 'none'
            Line:
                points: [.5*self.width,root.button_height,.5*self.width,0]
                width: .5*root.outline_width
                cap: 'none'
        Label:
            id: title
            pos_hint:{'center_x':.5,'center_y':.75}
            size_hint: (None,None)
            text_size: (.9*root.width,root.title_height)
            font_size: .8*self.text_size[1]
            size: self.text_size
            text: root.title
            bold: True
            valign: 'center'
            halign: 'center'
        Label:
            id: body
            pos_hint: {'center_x':.5}
            y: title.y-self.height
            size_hint: (None,None)
            text_size: (.9*root.width,title.y-yes_button.top)
            font_size: .1*root.height
            size: self.text_size
            text: root.body
            valign: 'top'
            halign: 'center'
        Button:
            id: yes_button
            size_hint: (.5,None)
            height: root.button_height
            pos_hint: {'x':0,'y':0}
            text: root.yes_text
            color: root.outline_color if self.state=='normal' else root.fill_color
            font_size: .5*self.height
            background_color: [1,1,1,0]
            on_release: root.dispatch('on_yes')
        Button:
            id: no_button
            size_hint: (.5,None)
            height: root.button_height
            pos_hint: {'x':.5,'y':0}
            text: root.no_text
            color: root.outline_color if self.state=='normal' else root.fill_color
            font_size: .5*self.height
            background_color: [1,1,1,0]
            on_release: root.dispatch('on_no')

<InputDialog>:
    size_hint: (.9,None)
    height: .8*self.width
    pos_hint: {'center_x':.5,'center_y':.5}
    fill_color: [.67,.816,.95,1]
    outline_color: [1,1,1,1]
    outline_width: .005*app.root.height
    button_height: .08*app.root.height
    title_height: .05*app.root.height
    body_height: .1*app.root.height
    background_color: 0,0,0,.7
    background: 'images/transparent.png'
    auto_dismiss: True
    text_input: text_input.text
    RelativeLayout:
        canvas:
            Color:
                rgba: [1,1,1,1]
            RoundedRectangle:
                size: self.size
                radius: [(30,30),(30,30),(30,10),(30,30)]
            Color:
                rgba: root.outline_color
            RoundedRectangle:
                size: self.size
                radius: [(30,30),(30,30),(30,10),(30,30)]
            Color:
                rgba: root.fill_color
            RoundedRectangle:
                size: (self.width-2*root.outline_width,self.height-2*root.outline_width)
                pos: (root.outline_width,root.outline_width)
                radius: [(30,30),(30,30),(30,10),(30,30)]        
            Color:
                rgba: root.outline_color
            Line:
                points: [0,root.button_height,self.width,root.button_height]
                width: .5*root.outline_width
                cap: 'none'
            Line:
                points: [.5*self.width,root.button_height,.5*self.width,0]
                width: .5*root.outline_width
                cap: 'none'
        Label:
            id: title
            pos_hint:{'center_x':.5,'top':.95}
            size_hint: (None,None)
            text_size: (.9*root.width,root.title_height)
            font_size: .8*self.text_size[1]
            size: self.text_size
            text: root.title
            bold: True
            valign: 'center'
            halign: 'center'
        Label:
            id: body
            pos_hint: {'center_x':.5}
            y: title.y-self.height
            size_hint: (None,None)
            text_size: (.9*root.width,root.body_height)
            font_size: .3*root.body_height
            size: self.text_size
            text: root.body
            valign: 'top'
            halign: 'center'
        TextInput:
            id: text_input
            on_text: if len(self.text) > root.max_characters: self.text = self.text[:root.max_characters]
            text: root.default_name
            font_size: .7*self.height
            size_hint: (.9,.2)
            pos_hint: {'center_x':.5}
            y: body.y-self.height
            multiline: False
        Button:
            id: yes_button
            size_hint: (.5,None)
            height: root.button_height
            pos_hint: {'x':0,'y':0}
            text: root.yes_text
            color: root.outline_color if self.state=='normal' else root.fill_color
            font_size: .5*self.height
            background_color: [1,1,1,0]
            on_release: root.dispatch('on_yes')
        Button:
            id: no_button
            size_hint: (.5,None)
            height: root.button_height
            pos_hint: {'x':.5,'y':0}
            text: root.no_text
            color: root.outline_color if self.state=='normal' else root.fill_color
            font_size: .5*self.height
            background_color: [1,1,1,0]
            on_release: root.dispatch('on_no')
            
<InputWithCheckboxDialog>:
    size_hint: (.9,None)
    height: .8*self.width
    pos_hint: {'center_x':.5,'center_y':.5}
    fill_color: [.67,.816,.95,1]
    outline_color: [1,1,1,1]
    outline_width: .005*app.root.height
    button_height: .08*app.root.height
    title_height: .05*app.root.height
    body_height: .1*app.root.height
    background_color: 0,0,0,.7
    background: 'images/transparent.png'
    auto_dismiss: True
    text_input: text_input.text
    check_state: checkbox.active
    RelativeLayout:
        canvas:
            Color:
                rgba: [1,1,1,1]
            RoundedRectangle:
                size: self.size
                radius: [(30,30),(30,30),(30,10),(30,30)]
            Color:
                rgba: root.outline_color
            RoundedRectangle:
                size: self.size
                radius: [(30,30),(30,30),(30,10),(30,30)]
            Color:
                rgba: root.fill_color
            RoundedRectangle:
                size: (self.width-2*root.outline_width,self.height-2*root.outline_width)
                pos: (root.outline_width,root.outline_width)
                radius: [(30,30),(30,30),(30,10),(30,30)]        
            Color:
                rgba: root.outline_color
            Line:
                points: [0,root.button_height,self.width,root.button_height]
                width: .5*root.outline_width
                cap: 'none'
            Line:
                points: [.5*self.width,root.button_height,.5*self.width,0]
                width: .5*root.outline_width
                cap: 'none'
        Label:
            id: title
            pos_hint:{'center_x':.5,'top':.95}
            size_hint: (None,None)
            text_size: (.9*root.width,root.title_height)
            font_size: .8*self.text_size[1]
            size: self.text_size
            text: root.title
            bold: True
            valign: 'center'
            halign: 'center'
        Label:
            id: body
            pos_hint: {'center_x':.5}
            y: title.y-self.height
            size_hint: (None,None)
            text_size: (.9*root.width,root.body_height)
            font_size: .3*root.body_height
            size: self.text_size
            text: root.body
            valign: 'top'
            halign: 'center'
        TextInput:
            id: text_input
            on_text: if len(self.text) > root.max_characters: self.text = self.text[:root.max_characters]
            text: root.default_name
            font_size: .7*self.height
            size_hint: (.9,.2)
            pos_hint: {'center_x':.5}
            y: body.y-self.height
            multiline: False
        CheckBox:
            id: checkbox
            active: True
            x: text_input.x
            top: text_input.y
            size_hint: (.12,None)
            height: self.width
        Label:
            id: checkbox_text
            x: checkbox.right
            top: text_input.y
            size_hint: (None,None)
            width: text_input.width - checkbox.width
            height: checkbox.height
            text: '' if root.checkbox_text==None else root.checkbox_text
            font_size: .5*checkbox.height
            valign: 'center'
            halign: 'left'
        Button:
            id: yes_button
            size_hint: (.5,None)
            height: root.button_height
            pos_hint: {'x':0,'y':0}
            text: root.yes_text
            color: root.outline_color if self.state=='normal' else root.fill_color
            font_size: .5*self.height
            background_color: [1,1,1,0]
            on_release: root.dispatch('on_yes')
        Button:
            id: no_button
            size_hint: (.5,None)
            height: root.button_height
            pos_hint: {'x':.5,'y':0}
            text: root.no_text
            color: root.outline_color if self.state=='normal' else root.fill_color
            font_size: .5*self.height
            background_color: [1,1,1,0]
            on_release: root.dispatch('on_no')

<ListDialog>:
    size_hint: (.9,None)
    height: .67*app.root.height
    pos_hint: {'center_x':.5,'center_y':.5}
    fill_color: [.67,.816,.95,1]
    outline_color: [1,1,1,1]
    outline_width: .005*app.root.height
    title_height: .05*app.root.height
    background_color: 0,0,0,.7
    background: 'images/transparent.png'
    auto_dismiss: True
    button_layout: button_layout
    button_height: .05*app.root.height
    RelativeLayout:
        canvas:
            Color:
                rgba: [1,1,1,1]
            RoundedRectangle:
                size: self.size
                radius: [(30,30),(30,30),(30,10),(30,30)]
            Color:
                rgba: root.outline_color
            RoundedRectangle:
                size: self.size
                radius: [(30,30),(30,30),(30,10),(30,30)]
            Color:
                rgba: root.fill_color
            RoundedRectangle:
                size: (self.width-2*root.outline_width,self.height-2*root.outline_width)
                pos: (root.outline_width,root.outline_width)
                radius: [(30,30),(30,30),(30,10),(30,30)]
        Label:
            id: title
            pos_hint:{'center_x':.5,'top':.98}
            size_hint: (None,None)
            font_size: root.title_height
            size: self.texture_size
            text: root.title
            bold: True
            underline: True
            valign: 'center'
            halign: 'center'
        ScrollView:
            pos_hint: {'center_x':.5}
            y: .05*root.height
            size_hint: (1,None)
            height: title.y - self.y
            do_scroll_x: False
            StackLayout:
                id: button_layout
                orientation: 'lr-tb'
                height: self.minimum_height
                padding: (0,0)
                spacing: 0
                size_hint: (1,None)

<ListDialogButton>:
    padding: [0,0]
    size_hint: (1,None)
    height: layout.height+2*self.padding[1]
    button_height: .05*app.root.height
    canvas:
        Color:
            rgba: 0,0,0,.1
        Line:
            points: [.1*self.width,self.y,.9*self.width,self.y]
            width: 1.5
    RelativeLayout:
        id: layout
        size_hint: (1,None)
        height: title.height
        Label:
            id: title
            text: root.title
            size_hint: (None,None)
            size: self.texture_size
            pos_hint: {'x':.05,'center_y':.5}
            bold: True
            font_size: root.button_height
            halign: 'left'
            valign: 'center'
        Button:
            background_normal: 'images/forward_button.png'
            background_down: 'images/forward_button_pressed.png'
            pos_hint: {'right':1,'center_y':.5}
            size_hint: (None,None)
            height: root.button_height
            width: self.height

<NewConfigDialog>:
    title: 'Create New Config'
    body: 'Choose a name for your new config.'
    yes_text: 'Submit'
    no_text: 'Cancel'
    on_yes:
        root.check_config_name(self.text_input)
    on_no:
        root.dismiss()

<RenameConfigDialog>:
    title: 'Rename Config'
    body: 'Choose a new name for your mirror configuration.'
    yes_text: 'Submit'
    no_text: 'Cancel'
    on_yes:
        root.check_config_name(self.text_input)
    on_no:
        root.dismiss()

<DeleteConfigDialog>:
    title: "Delete Config?"
    body: "Are you sure you want to delete the config '"+root.selected_config_name+"'?"
    yes_text: 'Yes'
    no_text: 'Cancel'
    on_yes:
        root.dismiss()
        app.root.manager.config_screen.delete_selected_config()
    on_no:
        root.dismiss()

<ForgetMirrorDialog>:
    title: 'Forget Mirror?'
    body: 'Forget mirror '+root.selected_mirror_name+'? This will delete all saved data of mirror from this phone.'
    yes_text: 'Yes'
    no_text: 'Cancel'
    on_yes:
        root.dismiss()
        app.root.manager.mirror_select_screen.forget_selected_mirror()
    on_no:
        root.dismiss()
        
<RenameMirrorDialog>:
    title: 'Rename Mirror'
    body: 'Choose a new name for your mirror.'
    yes_text: 'Submit'
    no_text: 'Cancel'
    on_yes:
        root.dismiss()
        app.root.manager.mirror_select_screen.rename_selected_mirror(self.text_input)
    on_no:
        root.dismiss()

<DeleteWidgetDialog>:
    title: "Delete Widget?"
    body: "Are you sure you want to delete the widget '"+root.selected_widget_name+"'?"
    yes_text: 'Yes'
    no_text: 'Cancel'
    on_yes:
        root.dismiss()
        app.root.manager.widgets_screen.delete_selected_widget()
    on_no:
        root.dismiss()
        
<RenameWidgetDialog>:
    title: 'Rename Widget'
    body: 'Choose a new name for this widget.'
    yes_text: 'Submit'
    no_text: 'Cancel'
    on_yes:
        root.check_widget_name(self.text_input)
    on_no:
        root.dismiss()

<MirrorOfflineDialog>:
    title: self.mirror_name+" is Offline"
    body: "Any changes made here will be applied next time mirror is online. Continue in offline mode?"
    yes_text: 'Yes'
    no_text: 'No'
    on_yes:
        root.dismiss()
        app.root.manager.mirror_select_screen.go_to_config_screen(self.mirror_id)
    on_no:
        root.dismiss()
        
<NotActiveConfigDialog>:
    title: 'Not Active Layout'
    body: "This is not the currently displayed layout on the mirror. Set as active layout?"
    yes_text: 'Yes'
    no_text: 'No'
    on_yes:
        root.dismiss()
        app.selected_mirror['sys']['active_config'] = self.config_name
        app.root.manager.config_screen.go_to_layout_screen(self.config_name)
    on_no:
        root.dismiss()
        app.root.manager.config_screen.go_to_layout_screen(self.config_name)

<ConfigToolBar>:
    id: configtoolbar
    on_dismiss: app.root.manager.config_screen.update_config_list()
    background_color: 0,0,0,.3
    canvas:
        Color:
            rgba: .67,.816,.95,1
        Rectangle:
            size: self.size
            pos: (0,0)
    size_hint: (1,.15)
    pos_hint: {'x':0,'y':0}
    RelativeLayout:
        IconWithCaption:
            source: 'images/trashbin.png'
            caption: 'Delete Layout'
            size_hint: (None,None)
            width: .55*root.height
            pos_hint: {'center_x':.3,'center_y':.5}
            on_release: app.root.manager.config_screen.delete_config_popup()
        IconWithCaption:
            source: 'images/rename.png'
            caption: 'Rename Layout'
            size_hint: (None,None)
            width: .55*root.height
            pos_hint: {'center_x':.7,'center_y':.5}
            on_release: app.root.manager.config_screen.rename_config_popup()

<IconWithCaption>:
    size_hint_y: None
    height: img.height + cp.height
    Image:
        id: img
        source: root.source
        pos_hint: {'center_x':.5,'top':1}
        size_hint: (1,None)
        height: self.width
    Label:
        id: cp
        size_hint: (None,None)
        text_size: (root.width,None)
        size: self.texture_size
        pos_hint: {'center_x':.5}
        top: img.y
        font_size: .25*img.height
        color: root.font_color
        valign: 'top'
        halign: 'center'
        text: root.caption
        bold: True
        line_height: .9

<MirrorToolBar>:
    on_dismiss: app.root.manager.mirror_select_screen.load_buttons()
    background_color: 0,0,0,.3
    canvas:
        Color:
            rgba: .67,.816,.95,1
        Rectangle:
            size: self.size
            pos: (0,0)
    size_hint: (1,.15)
    pos_hint: {'x':0,'y':0}
    RelativeLayout:
        IconWithCaption:
            source: 'images/trashbin.png'
            caption: 'Forget Mirror'
            size_hint: (None,None)
            width: .55*root.height
            pos_hint: {'center_x':.3,'center_y':.5}
            on_release: app.root.manager.mirror_select_screen.forget_mirror_popup()
        IconWithCaption:
            source: 'images/rename.png'
            caption: 'Rename Mirror'
            size_hint: (None,None)
            width: .55*root.height
            pos_hint: {'center_x':.7,'center_y':.5}
            on_release: app.root.manager.mirror_select_screen.rename_mirror_popup()

<WidgetToolBar>:
    on_dismiss: app.root.manager.widgets_screen.load_widget_list()
    background_color: 0,0,0,.3
    canvas:
        Color:
            rgba: .67,.816,.95,1
        Rectangle:
            size: self.size
            pos: (0,0)
    size_hint: (1,.15)
    pos_hint: {'x':0,'y':0}
    RelativeLayout:
        IconWithCaption:
            source: 'images/trashbin.png'
            caption: 'Delete Widget'
            size_hint: (None,None)
            width: .55*root.height
            pos_hint: {'center_x':.3,'center_y':.5}
            on_release: app.root.manager.widgets_screen.delete_widget_popup()
        IconWithCaption:
            source: 'images/rename.png'
            caption: 'Rename Widget'
            size_hint: (None,None)
            width: .55*root.height
            pos_hint: {'center_x':.7,'center_y':.5}
            on_release: app.root.manager.widgets_screen.rename_widget_popup()

<ConfigScreen>:
    button_layout: button_layout
    ScrollView:
        size_hint: (.9,1)
        pos_hint: {'center_x':.5,'y':0}
        do_scroll_x: False
        StackLayout:
            id: button_layout
            height: self.minimum_height
            orientation: 'lr-tb'
            padding: (0,75)
            spacing: 50
            size_hint: (1,None)
            
<MirrorSelectScreen>:
    button_layout: button_layout
    searching_label: search_label
    ScrollView:
        id: scrollview
        size_hint: (.9,1)
        pos_hint: {'center_x':.5,'y':0}
        do_scroll_x: False
        StackLayout:
            id: button_layout
            orientation: 'lr-tb'
            height: self.minimum_height
            padding: (0,75)
            spacing: 50
            size_hint: (1,None)
    Label:
        id: search_label
        size_hint: (None,None)
        text_size: (root.width,None)
        size: self.texture_size
        pos_hint: {'center_x':.5,'center_y':.6}
        halign: 'center'
        valign: 'center'
        font_size: .05*root.height
        text: 'Searching for connected devices...'
            
<WidgetsScreen>:
    button_layout: button_layout
    ScrollView:
        size_hint: (.9,.9)
        pos_hint: {'center_x':.5,'top':1}
        do_scroll_x: False
        StackLayout:
            id: button_layout
            orientation: 'lr-tb'
            padding: (0,75)
            spacing: 50
            size_hint: (1,None)

<MiscScreen>:
    Label:
        text: "Haven't gotten to this yet!"
        font_size: .1*root.height
        bold: True
        color: .67,.816,.95,1
        pos_hint: {'center_x':.5,'center_y':.7}
        size: self.texture_size
        valign: 'center'
        halign: 'center'
        text_size: (root.width,root.height)
        


<NavBar>:
    size_hint: (1,.1)
    BoxLayout:
        orientation: 'horizontal'
        Button:
            id: layout_screen
            text: 'Layout'
            on_press: root.configure_transition(requested_screen='layout_screen')
            on_release: app.root.manager.change_screen('layout_screen')
        Button:
            id: widgets_screen
            text: 'Widgets'
            on_press: root.configure_transition(requested_screen='widgets_screen')
            on_release: app.root.manager.change_screen('widgets_screen')
        Button:
            id: mirror_settings_screen
            text: 'Mirror'
            on_press: root.configure_transition(requested_screen='mirror_settings_screen')
            on_release: app.root.manager.change_screen('mirror_settings_screen')
        Button:
            id: misc_screen
            text: 'Misc'
            on_press: root.configure_transition(requested_screen='misc_screen')
            on_release: app.root.manager.change_screen('misc_screen')

<AddWidgetBar>:
    size_hint: (1,.1)
    pos_hint: {'center_x':.5}
    Button:
        font_size: self.height
        pos_hint: {'center_x':.5,'center_y':.5}
        size_hint: (None,1)
        width: self.height
        background_normal: 'images/new_widget.png'
        background_down: 'images/new_widget_pressed.png'
        on_release: root.new_widget_dialog()

<ToggleScatterBar>:
    size_hint: (1,.1)
    CheckBox:
        background_checkbox_normal: 'images/translate_symbol_disabled.png'
        background_checkbox_down: 'images/translate_symbol.png'
        pos_hint: {'center_x':.15,'center_y':.5}
        size_hint: (None,1)
        width: self.height
        state: 'down'
        on_active: app.root.manager.layout_screen.selected_widget.do_translation = self.active
    CheckBox:
        background_checkbox_normal: 'images/scale_symbol_disabled.png'
        background_checkbox_down: 'images/scale_symbol.png'
        pos_hint: {'center_x':.5,'center_y':.5}
        size_hint: (None,1)
        width: self.height
        state: 'down'
        on_active: app.root.manager.layout_screen.selected_widget.do_scale = self.active
    CheckBox:
        id: rotation
        background_checkbox_normal: 'images/rotate_symbol_disabled.png'
        background_checkbox_down: 'images/rotate_symbol.png'
        pos_hint: {'center_x':.85,'center_y':.5}
        size_hint: (None,1)
        width: self.height
        state: 'normal'
        on_active: app.root.manager.layout_screen.selected_widget.do_rotation = self.active
            
<NewWidgetBar>:
    size_hint: (1,.12)
    pos_hint: {'center_x':.5,'y':0}
    canvas:
        Color:
            rgba: .67,.816,.95,1
        Rectangle:
            size: self.size
            pos: 0,0
    Button:
        pos_hint: {'center_x':.33}
        size_hint: (None,1)
        width: self.height
        background_normal: 'images/green_checkmark.png'
        background_down: 'images/green_checkmark_pressed.png'
        border: [0,0,0,0]
        on_release: app.root.manager.layout_screen.place_widget()
    Button:
        pos_hint: {'center_x':.67}
        size_hint: (None,1)
        width: self.height
        background_normal: 'images/red_x.png'
        background_down: 'images/red_x_pressed.png'
        border: [0,0,0,0]
        on_release: app.root.manager.layout_screen.cancel_widget()
            
<EditWidgetBar>:
    size_hint: (1,.1)
    pos_hint: {'center_x':.5,'y':0}
    canvas:
        Color:
            rgba: .67,.816,.95,1
        Rectangle:
            size: self.size
            pos: 0,0
    Button:
        pos_hint: {'center_x':.15}
        size_hint: (None,1)
        width: self.height
        background_normal: 'images/green_checkmark.png'
        background_down: 'images/green_checkmark_pressed.png'
        border: [0,0,0,0]
        on_release: app.root.manager.layout_screen.place_widget()
    Button:
        pos_hint: {'center_x':.38}
        size_hint: (None,1)
        width: self.height
        background_normal: 'images/red_x.png'
        background_down: 'images/red_x_pressed.png'
        border: [0,0,0,0]
        on_press: app.root.manager.layout_screen.cancel_widget()
    Button:
        pos_hint: {'center_x':.62}
        size_hint: (None,1)
        width: self.height
        background_normal: 'images/trashbin.png'
        background_down: 'images/trashbin.png'
        border: [0,0,0,0]
        on_release: app.root.manager.layout_screen.delete_widget()
    Button:
        text: '??'
        font_size: .8*self.height
        pos_hint: {'center_x':.85}
        size_hint: (None,1)
        width: self.height
        background_color: (1,1,1,0)
        on_press: app.root.manager.layout_screen.mynemjeef()

<UnsavedChangesWarning>:
    title: 'Unsaved Changes!'
    body: 'You have unsaved changes. What would you like to do?'
    yes_text: 'Save'
    no_text: 'Discard'
    auto_dismiss: False
    on_yes:
        self.dismiss()
        app.root.manager.layout_screen.place_widget()
        app.root.manager.current = self.next_screen
    on_no:
        self.dismiss()
        app.root.manager.layout_screen.cancel_widget()
        app.root.manager.current = self.next_screen

<UnsavedWidgetSettingsDialog>:
    title: 'Unsaved Changes!'
    text: 'You have unsaved changes! What would you like to do?'
    yes_text: 'Save'
    no_text: 'Discard'
    on_yes:
        root.dismiss()
        app.root.manager.widget_screen.save_settings()
    on_no:
        root.dismiss()
        app.root.manager.widget_screen.cancel_settings()

<UnsavedMirrorSettingsPopup>:
    size_hint: (.9,None)
    height: .7*self.width
    auto_dismiss: False
    RelativeLayout:
        id: layout
        Label:
            text: 'You have unsaved changes! What would you like to do?'
            bold: True
            halign: 'center'
            valign: 'center'
            pos_hint: {'center_x':.5,'center_y':.6}
            color: root.font_color
            size_hint: (None,None)
            size: self.texture_size
            font_size: .1*root.height
            text_size: layout.size
        BoxLayout:
            orientation: 'horizontal'
            size_hint: (1,.2)
            pos_hint: {'x':0,'y':0}
            padding: 1
            spacing: 1
            Button:
                text: 'Save'
                on_release: 
                    root.dismiss()
                    app.root.manager.mirror_settings_screen.save_settings()
            Button:
                text: 'Discard'
                on_release:
                    root.dismiss()
                    app.root.manager.mirror_settings_screen.cancel_settings()

<Mirror>:
    size_hint: (None,None)
    canvas:
        BorderImage:
            source: 'images/mirror_frame.png'
            border: [root.frame_bottom,root.frame_right,root.frame_top,root.frame_left]
            pos: (0,0)
            size: self.size
    RelativeLayout:
        id: mirror_space
        pos: (root.frame_left,root.frame_bottom)
        size_hint: (None,None)
        height: root.height-root.frame_top-root.frame_bottom
        width: root.width-root.frame_left-root.frame_right
        
<LayoutScreen>:
    add_widget_bar: add_widget_bar
    mirror_plus_frame: mirror_plus_frame
    Mirror:
        id: mirror_plus_frame
        pos_hint: {'center_x':.5}
    AddWidgetBar:
        id: add_widget_bar
        y: mirror_plus_frame.y-self.height-.05*self.height

<CustomButton>:
    size_hint: (1,None)
    pos_hint: {'center_x':.5}
    font_size: .5*self.height
    height: .1*app.root.height
    color: .67,.816,.95,1
    bold: True
    
<CustomToggleButton>:
    size_hint: (1,None)
    pos_hint: {'center_x':.5}
    font_size: .7*self.height

<SwitchBlock>:
    size_hint: (1,None)
    height: title.height+body.height
    Label:
        id: title
        text: root.title
        size_hint: (None,None)
        size: self.texture_size
        pos_hint: {'x':0,'top':1}
        bold: True
        font_size: .03*app.root.height
        halign: 'left'
        valign: 'top'
    Label:
        id: body
        text: root.body
        size_hint: (None,None)
        size: self.texture_size
        text_size: (.7*root.width,None)
        y: title.y - self.height
        font_size: .6*title.font_size
        halign: 'left'
        valign: 'top'
    Switch:
        id: switch
        background_normal: SWITCH_OFF
        background_down: SWITCH_ON
        border: 0,0,0,0
        pos_hint:{'right':1,'center_y':.5}
        size_hint: (.25,None)
        on_active: root.dispatch('on_setting')

<TextInputBlock>:
    size_hint: (1,None)
    height: title.height+body.height
    Label:
        id: title
        text: root.title
        size_hint: (None,None)
        size: self.texture_size
        pos_hint: {'x':0,'top':1}
        bold: True
        font_size: .03*app.root.height
        halign: 'left'
        valign: 'top'
    Label:
        id: body
        text: root.body
        size_hint: (None,None)
        size: self.texture_size
        text_size: (.7*root.width,None)
        pos_hint: {'x':0}
        y: title.y - self.height
        font_size: .6*title.font_size
        halign: 'left'
        valign: 'top'
    Button:
        id: edit_button
        background_normal: 'images/rename.png'
        background_down: 'images/rename.png'
        border: [0,0,0,0]
        pos_hint: {'right':1,'center_y':.5}
        size_hint: (None,None)
        height: 1.25*title.font_size
        width: self.height
        on_release: app.root.manager.current_screen.rename_widget_popup()

<AlignmentBlock>:
    padding: [0,.02*app.root.height]
    size_hint: (1,None)
    height: layout.height+2*self.padding[1]
    canvas:
        Color:
            rgba: 0,0,0,.1
        Line:
            points: [.1*self.width,self.y,.9*self.width,self.y]
            width: 1.5
    RelativeLayout:
        id: layout
        size_hint: (1,None)
        height: title.height+body.height
        Label:
            id: title
            text: root.title
            size_hint: (None,None)
            size: self.texture_size
            pos_hint: {'top':.9}
            bold: True
            font_size: .035*app.root.height
            halign: 'left'
            valign: 'top'
        Label:
            id: body
            text: root.body
            size_hint: (.7,None)
            height: self.texture_size[1]
            text_size: (.7*root.width,None)
            y: title.y - self.height
            font_size: .6*title.font_size
            halign: 'left'
            valign: 'top'
        ToggleButton:
            id: right
            group: 'alignment'
            allow_no_selection: False
            size_hint: (.1,None)
            height: self.width
            pos_hint:{'right':1,'center_y':.5}
            on_release: root.dispatch('on_setting')
        ToggleButton:
            id: center
            group: 'alignment'
            allow_no_selection: False
            size_hint: (.1,None)
            height: self.width
            pos_hint:{'center_y':.5}
            right: right.x
            on_release: root.dispatch('on_setting')
        ToggleButton:
            id: left
            group: 'alignment'
            allow_no_selection: False
            size_hint: (.1,None)
            height: self.width
            pos_hint:{'center_y':.5}
            right: center.x
            on_release: root.dispatch('on_setting')

<SliderBlock>:
    size_hint: (1,None)
    height: title.height+body.height
    slider_value: slider.value
    canvas:
        Color:
            rgba: 0,0,0,.1
        Line:
            points: [.1*self.width,-.05*self.height,.9*self.width,-.05*self.height]
            width: 1
    Label:
        id: title
        text: root.title
        size_hint: (None,None)
        size: self.texture_size
        pos_hint: {'x':0,'top':1}
        bold: True
        font_size: .035*app.root.height
        halign: 'left'
        valign: 'center'
    Label:
        id: body
        text: root.body
        size_hint: (.5,None)
        height: self.texture_size[1]
        text_size: (.5*root.width,None)
        y: title.y - self.height
        font_size: .6*title.font_size
        halign: 'left'
        valign: 'top'
    Slider:
        id: slider
        value: root.slider_value
        pos_hint: {'right':1,'center_y':.5}
        size_hint: (.5,None)
        on_value: root.dispatch('on_slider')

<ButtonBlock>:
    size_hint: (1,None)
    height: title.height+body.height
    Label:
        id: title
        text: root.title
        size_hint: (None,None)
        size: self.texture_size
        pos_hint: {'x':0,'top':1}
        bold: True
        font_size: .03*app.root.height
        halign: 'left'
        valign: 'top'
    Label:
        id: body
        text: root.body
        size_hint: (None,None)
        size: self.texture_size
        text_size: (.7*root.width,None)
        pos_hint: {'x':0}
        y: title.y - self.height
        font_size: .6*title.font_size
        halign: 'left'
        valign: 'top'

<BlockSeparator>:
    pos_hint: {'center_x':.5}
    size_hint_x: .9 if self.indent else 1
    size_hint_y: None
    height: 15
    Label:
        id: txt
        text: root.title+' '
        font_size: root.height
        bold: True
        pos_hint: {'x':0,'center_y':.5}
        size_hint: (None,None)
        size: self.texture_size
    Widget:
        size_hint: (None,None)
        width: root.width - txt.width
        height: txt.height
        x: txt.right
        pos_hint: {'center_y':.5}
        canvas:
            Color:
                rgba: 0,0,0,.1
            Line:
                points: [txt.right,.5*self.height,txt.right+self.width,.5*self.height]
                width: 1

<TimeWidgetScreen>:
    button_layout: button_layout
    ScrollView:
        size_hint: (.9,.9)
        pos_hint: {'center_x':.5,'top':1}
        do_scroll_x: False
        StackLayout:
            id: button_layout
            orientation: 'lr-tb'
            padding: (0,25)
            spacing: 25
            height: self.minimum_height
            size_hint: (1,None)
    Button:
        id: apply_button
        size_hint: (.5,.1)
        pos_hint: {'x': 0,'y':0}
        text: 'Apply'
        on_release: root.apply_changes()
    Button:
        id: cancel_button
        size_hint: (.5,.1)
        x:  apply_button.right
        y: 0
        text: 'Cancel'
        on_release: root.cancel_changes()

<WeatherWidgetScreen>:
    button_layout: button_layout
    ScrollView:
        size_hint: (.9,.95)
        pos_hint: {'center_x':.5,'top':1}
        do_scroll_x: False
        StackLayout:
            id: button_layout
            height: self.minimum_height
            orientation: 'lr-tb'
            padding: (0,25)
            spacing: 25
            size_hint: (1,None)
    Button:
        id: apply_button
        size_hint: (.5,.1)
        pos_hint: {'x': 0,'y':0}
        text: 'Apply'
        on_release: root.apply_changes()
    Button:
        id: cancel_button
        size_hint: (.5,.1)
        x:  apply_button.right
        y: 0
        text: 'Cancel'
        on_release: root.cancel_changes()
        
<ClockWidgetScreen>:
    button_layout: button_layout
    ScrollView:
        size_hint: (.9,.95)
        pos_hint: {'center_x':.5,'top':1}
        do_scroll_x: False
        StackLayout:
            id: button_layout
            height: self.minimum_height
            orientation: 'lr-tb'
            padding: (0,25)
            spacing: 25
            size_hint: (1,None)
    Button:
        id: apply_button
        size_hint: (.5,.1)
        pos_hint: {'x': 0,'y':0}
        text: 'Apply'
        on_release: root.apply_changes()
    Button:
        id: cancel_button
        size_hint: (.5,.1)
        x:  apply_button.right
        y: 0
        text: 'Cancel'
        on_release: root.cancel_changes()

<MirrorSettingsScreen>:
    button_layout: button_layout
    ScrollView:
        size_hint: (.9,.95)
        pos_hint: {'center_x':.5,'y':0}
        do_scroll_x: False
        StackLayout:
            id: button_layout
            orientation: 'lr-tb'
            padding: (0,0)
            spacing: 40
            size_hint: (1,None)

''')
Builder.load_file('widgets/kv/weather.kv')
Builder.load_file('widgets/kv/time.kv')
Builder.load_file('widgets/kv/todolist.kv')
Builder.load_file('widgets/kv/clock.kv')


class RootLayout(FloatLayout):
    title = ObjectProperty()
    header = ObjectProperty()
    manager = ObjectProperty()
    nav_bar = ObjectProperty()

    def update_nav_bar(self, enable=False):
        app = App.get_running_app()
        current_screen = app.root.manager.current
        if enable:
            new_pos_hint = {'top': .1}
            for btn in app.root.nav_bar.walk():
                btn.disabled = False
            app.root.nav_bar.ids[current_screen].disabled = True
        else:
            new_pos_hint = {'top': 0}
        animation = Animation(pos_hint=new_pos_hint, duration=.25)
        animation.start(app.root.nav_bar)

    def update_header(self, title, previous_screen=None):

        # 1. Set title
        self.header.title = title

        # 2. Set back button
        self.header.back_button.size_hint_y = 0
        if previous_screen is not None:
            self.header.previous_screen = previous_screen
            self.header.back_button.size_hint_y = 1

        # 3. Set wifi symbol
        app = App.get_running_app()
        current_screen = app.root.manager.current
        if current_screen == 'mirror_select_screen':
            self.header.wifi.source = 'images/transparent.png'
            self.header.wifi.caption = ''
        else:
            if app.selected_mirror_id in app.connected_mirrors:
                self.header.wifi.source = 'images/wifi_on.png'
                self.header.wifi.caption = 'Online'
                self.header.wifi.font_color = [71/256, 149/256, 236/256, 1]
            else:
                self.header.wifi.source = 'images/wifi_off.png'
                self.header.wifi.caption = 'Offline'
                self.header.wifi.font_color = [.75, .75, .75, 1]


class Manager(ScreenManager):
    mirror_select_screen = ObjectProperty()
    config_screen = ObjectProperty()
    layout_screen = ObjectProperty()
    widgets_screen = ObjectProperty()
    mirror_settings_screen = ObjectProperty()
    misc_screen = ObjectProperty()
    time_widget_screen = ObjectProperty()
    weather_widget_screen = ObjectProperty()
    clock_widget_screen = ObjectProperty()

    # Check that there aren't unsaved changes before moving to next screen
    def change_screen(self,next_screen):
        app = App.get_running_app()

        #1. If a widget is currently selected in layout screen, prompt warning for unsaved changes
        if app.root.manager.layout_screen.selected_widget:
            UnsavedChangesWarning(next_screen=next_screen).open()
            return

        self.current = next_screen

        #3. If mirror settings have been changed, prompt warning


class NavBar(RelativeLayout):
    _enabled = BooleanProperty(False)
    active_button_pos = NumericProperty()

    # Figure out if transition should slide left or right, depending on current page
    def configure_transition(self,requested_screen):
        app = App.get_running_app()
        all_screens = app.root.manager.screen_names
        current_screen = app.root.manager.current
        if all_screens.index(requested_screen) > all_screens.index(current_screen):
            app.root.manager.transition.direction = 'left'
        else:
            app.root.manager.transition.direction = 'right'

class Header(RelativeLayout):
    title = StringProperty()
    previous_screen = StringProperty()
    back_button = ObjectProperty()
    wifi = ObjectProperty()

class ScreenTemplate(Screen):
    pass

class Mirror(RelativeLayout):
    frame_top = NumericProperty(42)
    frame_left = NumericProperty(42)
    frame_right = NumericProperty(42)
    frame_bottom = NumericProperty(42)

class WarningDialog(ModalView):
    fill_color = ListProperty()
    outline_color = ListProperty()
    active_color = ListProperty()
    outline_width = NumericProperty(1)
    title = StringProperty()
    body = StringProperty()
    yes_text = StringProperty()
    no_text = StringProperty()
    button_height = NumericProperty()
    title_height = NumericProperty()

    __events__ = ('on_yes','on_no',)

    def on_yes(self):
        pass
    def on_no(self):
        pass


class InputDialog(ModalView):
    fill_color = ListProperty()
    outline_color = ListProperty()
    active_color = ListProperty()
    outline_width = NumericProperty(1)
    title = StringProperty()
    body = StringProperty()
    yes_text = StringProperty()
    no_text = StringProperty()
    button_height = NumericProperty()
    title_height = NumericProperty()
    body_height = NumericProperty()
    text_input = StringProperty()

    __events__ = ('on_yes','on_no',)

    def on_yes(self):
        pass

    def on_no(self):
        pass

class InputWithCheckboxDialog(InputDialog):
    check_state = BooleanProperty()
    checkbox_text = StringProperty()


class ListDialog(ModalView):
    title = StringProperty()
    title_height = NumericProperty()
    button_layout = ObjectProperty()
    fill_color = ListProperty()
    outline_width = NumericProperty()
    outline_color = ListProperty()
    selected = ObjectProperty(None,allownone=True)

    list_items = DictProperty()
    __events__ = ('on_selected',)

    def __init__(self,**kwargs):
        super(ListDialog,self).__init__(**kwargs)

        # Generate list
        for title,value in self.list_items.items():
            new_item = ListDialogButton(title=title,value=str(value))
            new_item.bind(on_release=partial(self.set_selected, new_item.value))
            self.button_layout.add_widget(new_item)

    def add_option(self,widget):
        self.button_layout.add_widget(widget)

    def set_selected(self, value, *args):
        self.selected = value
        self.dismiss()

    def on_selected(self,*args):
        pass


class ListDialogButton(ButtonBehavior, BoxLayout):
    title = StringProperty(allownone=True)
    value = StringProperty()
    button_height = NumericProperty()

class CustomPopup(ModalView):
    font_color = ListProperty([.67,.816,.95,1])

class UnsavedChangesWarning(WarningDialog):
    next_screen = StringProperty()

class UnsavedWidgetSettingsDialog(WarningDialog):
    pass


class UnsavedMirrorSettingsPopup(CustomPopup):
    pass

class NewConfigDialog(InputWithCheckboxDialog):
    default_name = StringProperty('Config 1')
    max_characters = NumericProperty(20)
    checkbox_text = StringProperty('Display this layout on mirror')
    def __init__(self,**kwargs):
        super(NewConfigDialog,self).__init__(**kwargs)
        app = App.get_running_app()

        next_number = 1
        while self.default_name in app.selected_mirror['configs'].keys():
            next_number+=1
            self.default_name = 'Config '+str(next_number)

    def check_config_name(self,inputted_name):
        app = App.get_running_app()
        inputted_name = inputted_name.strip()

        #Perform various checks to make sure it's a valid name
        mirror_configs = app.selected_mirror['configs']
        if len(mirror_configs) > MAX_CONFIGS:
            self.body = 'Reached max number of configs!'
            return
        if len(inputted_name)==0 or inputted_name.isspace():
            self.body = 'Give a name for your mirror layout. You can change this later.'
            return
        if inputted_name in mirror_configs:
            self.body = 'Name already exists. Pick another name'
            return

        # If it's a valid name, create new config
        app.root.manager.config_screen.create_new_config(inputted_name,set_as_active=self.check_state)
        self.dismiss()

class RenameConfigDialog(InputDialog):
    default_name = StringProperty()
    max_characters = NumericProperty(20)

    def check_config_name(self,inputted_name):
        app = App.get_running_app()
        inputted_name = inputted_name.strip()

        #Perform various checks to make sure it's a valid name
        mirror_configs = app.selected_mirror['configs']
        if inputted_name==self.default_name:
            self.dismiss()
            return
        if len(inputted_name)==0 or inputted_name.isspace():
            self.body = "Mirror name can't be empty"
            return
        if inputted_name in mirror_configs:
            self.body = 'A config with that name already exists. Pick another name'
            return

        app.root.manager.config_screen.rename_selected_config(inputted_name)
        self.dismiss()

class DeleteConfigDialog(WarningDialog):
    selected_config_name = StringProperty()

class ForgetMirrorDialog(WarningDialog):
    selected_mirror_name = StringProperty()

class RenameMirrorDialog(InputDialog):
    default_name = StringProperty()
    max_characters = NumericProperty(15)

class DeleteWidgetDialog(WarningDialog):
    selected_widget_name = StringProperty()

class RenameWidgetDialog(InputDialog):
    default_name = StringProperty()
    max_characters = NumericProperty(15)

    def check_widget_name(self,inputted_name):
        app = App.get_running_app()
        inputted_name = inputted_name.strip()

        # Perform various checks to make sure it's a valid name
        widget_names = app.selected_mirror['configs'][app.selected_config_name]['widget_settings'].keys()
        if inputted_name==self.default_name:
            self.dismiss()
            return
        if len(inputted_name)==0 or inputted_name.isspace():
            self.body = "Widget name can't be empty"
            return
        if inputted_name in widget_names:
            self.body = 'A widget with that name already exists. Pick another name'
            return

        # If new name is valid
        app.root.manager.current_screen.rename_selected_widget(inputted_name)
        self.dismiss()

class NewWidgetDialog(ListDialog):

    def on_selected(self,*args):
        App.get_running_app().root.manager.layout_screen.add_new_widget(self.selected)

class BlockSeparator(RelativeLayout):
    title = StringProperty('')
    indent = BooleanProperty(False)

class DateFormatDialog(ListDialog):

    def __init__(self,**kwargs):
        app = App.get_running_app()

        self.title = 'Choose a date format'

        # Create dict of values for all date formats
        dummy_widget = app.generate_widget('Time')
        item_list = {}
        id = 0
        while True:
            title = dummy_widget.get_date(id)
            if not title: break
            item_list[title] = id
            id += 1
        self.list_items = item_list

        # Feed this into base init to construct dialog window
        super(DateFormatDialog,self).__init__(**kwargs)

    def on_selected(self,*args):
        app = App.get_running_app()

        app.root.manager.current_screen.date_format.setting = self.selected
        app.root.manager.current_screen.save_setting('date_format')


class MirrorOfflineDialog(WarningDialog):
    mirror_id = StringProperty()
    mirror_name = StringProperty()

class NotActiveConfigDialog(WarningDialog):
    config_name = StringProperty()

class ConfigButton(Button,FloatLayout):
    config_name = StringProperty()
    _hold_triggered = BooleanProperty(False)
    active_config = BooleanProperty(False)
    background_held = StringProperty()

    def on_press(self,*args):
        self._hold_triggered = False
        Clock.schedule_once(self.on_hold,.6)

    # This only gets triggered for quick releases
    def on_release(self,*args):
        if not self._hold_triggered:
            Clock.unschedule(self.on_hold)
            app = App.get_running_app()

            if self.config_name == app.selected_mirror['sys']['active_config']:
                app.root.manager.config_screen.go_to_layout_screen(self.config_name)
            else:
                NotActiveConfigDialog(config_name=self.config_name).open()

    # Goes here if you hold for .6 s
    def on_hold(self,*args):
        app = App.get_running_app()
        self._hold_triggered = True
        self.background_normal = self.background_held
        app.root.manager.config_screen.bring_up_toolbar(selected_config_name=self.config_name)

    def update_active_config(self,*args):
        app = App.get_running_app()

        # If button is being changed from up to down
        if self.ids['active_checkbox'].state=='down':
            Logger.info('Setting config {} to active config.'.format(self.config_name))

            #1. Update phone config
            app.selected_mirror['sys']['active_config'] = self.config_name
            app.update_phone()

            #2. Try to update mirror
            app.update_mirror()

class NewButton(Button,FloatLayout):
    pass

class RefreshButton(NewButton):
    pass

class CustomToggleButton(ToggleButton):
    pass

class WidgetButton(Button,FloatLayout):
    widget_name = StringProperty()
    _hold_triggered = BooleanProperty(False)
    background_held = StringProperty()

    def on_press(self,*args):
        self._hold_triggered = False
        Clock.schedule_once(self.on_hold,.6)

    #GOES HERE EVERY TIME
    def on_release(self,*args):
        #For short click, unschedule on_hold and go to widget settings screen
        if not self._hold_triggered:
            Clock.unschedule(self.on_hold)
            app = App.get_running_app()
            app.root.manager.transition.direction = 'left'
            app.root.manager.widgets_screen.go_to_settings(self.widget_name)

    #Only goes here if you hold for .6 s
    def on_hold(self,*args):
        app = App.get_running_app()
        self._hold_triggered = True
        self.background_normal = self.background_held
        app.root.manager.widgets_screen.bring_up_toolbar(selected_widget_name=self.widget_name)

class IconWithCaption(ButtonBehavior,RelativeLayout):
    source = StringProperty()
    caption = StringProperty()
    font_color = ListProperty([1,1,1,1])

class ConfigToolBar(ModalView):
    pass

class MirrorToolBar(ModalView):
    pass

class WidgetToolBar(ModalView):
    pass

class AddWidgetBar(RelativeLayout):
    def new_widget_dialog(self,*args):
        dict_of_items = {item:item for item in LIST_OF_WIDGETS}
        dialog = NewWidgetDialog(title='Select a widget',list_items = dict_of_items)
        dialog.open()

class ToggleScatterBar(RelativeLayout):
    def __init__(self,**kwargs):
        super(ToggleScatterBar,self).__init__(**kwargs)
        app = App.get_running_app()

        # 1. Set position below mirror
        self.y = app.root.manager.layout_screen.mirror_plus_frame.y\
                               -self.height-.05*self.height

        # 2. Enable rotation if angle is already nonzero
        if app.root.manager.layout_screen.selected_widget.rotation != 0:
            self.ids['rotation'].state = 'down'

class NewWidgetBar(RelativeLayout):
    pass

class EditWidgetBar(RelativeLayout):
    pass

class SwitchBlock(RelativeLayout):
    title = StringProperty()
    body = StringProperty()
    __events__ = ('on_setting',)

    def set_setting(self, value):
        self.ids['switch'].active = value

    def get_setting(self, *args):
        return self.ids['switch'].active
    setting = AliasProperty(get_setting, set_setting)

    def on_setting(self, *args):
        pass

class AlignmentBlock(RelativeLayout):
    title = StringProperty()
    body = StringProperty()
    alignment = OptionProperty('left',options=['left','center','right'])
    __events__ = ('on_setting',)
    def set_setting(self,value):
        self.ids['left'].state='down' if value=='left' else 'normal'
        self.ids['center'].state='down' if value=='center' else 'normal'
        self.ids['right'].state='down' if value=='right' else 'normal'
    def get_setting(self,*args):
        if self.ids['left'].state=='down':
            return 'left'
        elif self.ids['center'].state=='down':
            return 'center'
        elif self.ids['right'].state=='down':
            return 'right'
        else:
            return False
    setting = AliasProperty(get_setting,set_setting)

    def on_setting(self,*args):
        pass

class SliderBlock(RelativeLayout):
    slider_value = NumericProperty()
    title = StringProperty()
    body = StringProperty()
    __events__ = ('on_slider',)
    def on_slider(self,*args):
        pass
class TextInputBlock(RelativeLayout):
    title = StringProperty()
    body = StringProperty()

class ButtonBlock(ButtonBehavior,RelativeLayout):
    title = StringProperty()
    body = StringProperty()
    setting = ObjectProperty()


class MirrorSelectScreen(ScreenTemplate):
    button_layout = ObjectProperty()
    mirror_toolbar = ObjectProperty()
    searching_label = ObjectProperty()
    multicast_ip = StringProperty('224.3.29.71')
    multicast_port = NumericProperty(11088)
    tcp_port = NumericProperty(54321)
    response_time = NumericProperty(2)

    def on_pre_enter(self, *args):
        app = App.get_running_app()

        # Only runs if you are returning to the mirror screen
        if app.root:
            app.root.update_nav_bar(enable=False)
            self.button_layout.clear_widgets()
            self.searching_label.opacity = 1.0

    def on_enter(self,*args):
        app = App.get_running_app()

        # 1. If root NOT created yet, schedule on_enter again immediately
        if not app.root:
            Clock.schedule_once(self.on_enter, 0)
            return

        # 2. Clear selected_mirror info
        app.selected_mirror_id = ''
        app.selected_mirror = {}

        # 3. Update header
        app.root.update_header(title="Choose a Mirror!")

        # 4. Ping network and gather list of connected mirrors. Allows 2 seconds for response
        Logger.info('Searching for list of connected devices...')
        th = threading.Thread(target=self.get_connected_mirrors)
        th.start()

        # 5. Sync mirrors' storage with phone storage
        Clock.schedule_once(self.sync_mirrors, self.response_time)

        # 6. Create button list for all mirrors. Lights up the ones that are online
        Clock.schedule_once(self.load_buttons, self.response_time)

    def sync_mirrors(self,*args):
        app = App.get_running_app()
        for key in app.connected_mirrors.keys():
            Logger.info('Syncing mirror {} with phone.'.format(key))
            self.sync_mirror(key)
        Logger.info('Finished syncing mirrors with phone.')

    def sync_mirror(self,mirror_id,*args):
        app = App.get_running_app()

        mirror_ip = app.connected_mirrors[mirror_id]['ip']

        #1. If mirror config doesn't exist on phone, then automatically update phone
        if not app.store.exists(mirror_id):
            Logger.info('Config file not found in phone for mirror {}. Requesting data from mirror.'.format(mirror_id))
            self.get_data_from_mirror(mirror_id)
            return

        #2. Save last_ip to phone config, since at this point we've successfully connected to the mirror already
        try:
            phone_config = app.store.get(mirror_id)
            Logger.info('Loaded config info for mirror {}.'.format(mirror_id))
        except:
            Logger.error('Failed to load config info for mirror {} from phone storage.'.format(mirror_id))
            return

        last_edited_phone = phone_config['sys']['last_edited']
        last_edited_mirror = app.connected_mirrors[mirror_id]['last_edited']
        #2. If both last edited times are equal, no need to sync
        if last_edited_phone==last_edited_mirror:
            Logger.info('Phone and mirror already synced for mirror {}'.format(mirror_id))
            return

        #3. If phone config is newer, send data to mirror
        if last_edited_phone > last_edited_mirror:
            Logger.info('Phone config for {} is newer than mirror. Sending config file to mirror.'.format(mirror_id))
            update_thread = threading.Thread(target=app.update_mirror,args=(mirror_id,))
            update_thread.start()
            return

        #4. If mirror config is newer, request data from server
        if last_edited_mirror > last_edited_phone:
            Logger.info('Mirror config for {} is newer than phone. Requesting config data from mirror.'.format(mirror_id))
            request_thread = threading.Thread(target=self.get_data_from_mirror,args=(mirror_id,))
            request_thread.start()
            return

        Logger.critical('sync_mirror() screwed up and somehow made it through all possible options.')

    def load_buttons(self,*args):
        app = App.get_running_app()

        # 1. Clear buttons, and loading message
        self.button_layout.clear_widgets()
        self.searching_label.opacity = 0.0

        # 2. Clear selected mirror info
        app.selected_mirror_id = ''
        app.selected_mirror = {}
        self.num_mirrors = app.store.count()

        # 3. Load buttons of ALL mirror names in phone storage. Light up ones found in connected_mirrors
        for mirror_id in app.store.keys():
            mirror_name = app.store.get(mirror_id)['sys']['mirror_name']
            if mirror_id in app.connected_mirrors.keys():
                mirror_button = MirrorSelectButton(mirror_name=mirror_name, mirror_id=mirror_id, online=True)
            else:
                mirror_button = MirrorSelectButton(mirror_name=mirror_name, mirror_id=mirror_id, online=False)
            self.button_layout.add_widget(mirror_button)
        refresh_list_btn = RefreshButton(text='Refresh List',on_release=self.refresh_list)
        new_mirror_btn = NewButton(text='Find Another Mirror',on_release=self.find_new_mirror_dialog)
        self.button_layout.add_widget(refresh_list_btn)
        self.button_layout.add_widget(new_mirror_btn)

        Logger.info('Successfully loaded list of mirror buttons.')

    def find_new_mirror_dialog(self,*args):
        temp = WarningDialog(title='Not implemented yet',body="This window will help you find new mirrors on your network, that you haven't set up yet")
        temp.yes_text = 'Okay'
        temp.no_text = 'Cancel'
        temp.bind(on_yes=temp.dismiss)
        temp.bind(on_no=temp.dismiss)
        temp.open()

    # Retrieve data from mirror
    def get_data_from_mirror(self,mirror_id,*args):
        app = App.get_running_app()

        #1. Create socket and connect to mirror
        mirror_ip = app.connected_mirrors[mirror_id]['ip'][0]
        try:
            s = socket.socket()
            s.connect((mirror_ip,self.tcp_port))
            Logger.info('Established TCP connection with mirror {} on ip {}'.format(mirror_id,mirror_ip))
        except:
            Logger.error('Failed to establish TCP connection with mirror {} on ip {}.'.format(mirror_id,mirror_ip))
            return

        #2. Send request to mirror for data
        try:
            request_pickled = pickle.dumps(('','update_phone'))
            s.send(request_pickled)
            Logger.info('Sent request to mirror {} for config info.'.format(mirror_id))
        except:
            Logger.error('Error pickling and/or sending data request to mirror {}!'.format(mirror_id))
            return

        #3. Receives data in the form (mirror_id, {'sys': ..., 'configs': ...} )
        data_pickled = s.recv(4096)
        Logger.info('Received data from mirror {}.'.format(mirror_id))
        try:
            mirror_data = pickle.loads(data_pickled)
            sys = mirror_data[1]['sys']
            configs = mirror_data[1]['configs']
            Logger.info('Unpickled received data from mirror {}.'.format(mirror_id))
        except:
            Logger.error('Failed to unpickle data from mirror {}!'.format(mirror_id))
            return

        #4. Save to phone storage
        try:
            app.store.put(mirror_id,sys=sys,configs=configs)
            Logger.info('Updated phone storage for mirror {}. Closing TCP socket.'.format(mirror_id))
        except:
            Logger.error('Unable to update phone storage for mirror {}. Closing TCP socket.'.format(mirror_id))

        #5. Close connection
        s.close()

    def connected_to_wifi(self,*args):
        if platform == 'android':
            Logger.info('Running on Android OS.')
        #        Activity = autoclass('android.app.Activity')
        #        PythonActivity = autoclass('org.renpy.android.PythonActivity')
        #        activity = PythonActivity.mActivity
        #        ConnectivityManager = autoclass('android.net.ConnectivityManager')

        #        con_mgr = activity.getSystemService(Activity.CONNECTIVITY_SERVICE)
                # TYPE_WIFI deprecated for API level 28.
        #        connected = con_mgr.getNetworkInfo(ConnectivityManager.TYPE_WIFI).isConnectedorConnecting()
        #        if connected:
        #            return True
        #        else:
        #            connected = con_mgr.getNetworkInfo(ConnectivityManager.TYPE_MOBILE).isConnectedorConnecting
        #            if connected:
        #                return True
        #            else:
        #                return False
        #    if platform == 'macosx':
        #        Logger.info('Running on mac osx.')
        #    return True

    def no_wifi_popup(self, *args):
        Logger.info('Not connected to wifi!')

    def get_connected_mirrors(self, *args):
        app = App.get_running_app()

        # 0. Clear list of connected_mirrors
        app.connected_mirrors = {}

        # 1. Create datagram socket. Set timeout so it doesn't wait for replies forever
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(self.response_time)

        # 2. Set number of devices that can receive packet
        ttl = struct.pack('b', 5)  # output is '5' in binary
        s.setsockopt(socket.IPPROTO_IP,socket.IP_MULTICAST_TTL,ttl)

        # 4. Send message out to multicast address. Format is tuple of form (data,request)
        request = 'name'
        data_packed = pickle.dumps(('',request))
        s.sendto(data_packed,(self.multicast_ip,self.multicast_port))

        Logger.info('Sent multicast request to: ({},{})'.format(self.multicast_ip,self.multicast_port))

        # 5. Set loop to listen and build dict of mirrors that respond
        # Received data is tuple in format
        #       (mirror_id,mirror_name,last_edited)
        # When socket times out, breaks loop and terminates thread
        while True:
            try:
                Logger.info('Awaiting response from multicast...')
                data_pickled,address = s.recvfrom(4096)
                Logger.info('Received multicast response from network, from ip: '.format(address))
                try:
                    data = pickle.loads(data_pickled)
                except:
                    Logger.error('Failed to unpack pickled data!')
                mirror_id = data[0]
                mirror_name = data[1]
                last_edited = data[2]
                app.connected_mirrors[mirror_id] = {'mirror_name':mirror_name,'ip':address,'last_edited':last_edited}
            except:
                if len(app.connected_mirrors) == 0:
                    Logger.info('Did not find any mirrors on network! Closing multicast socket.')
                else:
                    Logger.info('Retrieved response from {} mirrors. Closing multicast socket.'.format(len(app.connected_mirrors)))
                break

        s.close()

    def refresh_list(self, *args):

        # 1. Clear button list
        self.button_layout.clear_widgets()

        # 2. Add "searching.." label
        self.searching_label.opacity = 1.0

        # 3. Reload screen
        Clock.schedule_once(self.on_enter, 0)

    def bring_up_toolbar(self,selected_mirror_id):
        app = App.get_running_app()

        app.selected_mirror_id = selected_mirror_id
        app.selected_mirror = app.store.get(selected_mirror_id)
        self.mirror_toolbar = MirrorToolBar()
        self.mirror_toolbar.open()

    def forget_mirror_popup(self,*args):
        app = App.get_running_app()
        mirror_name = app.store.get(app.selected_mirror_id)['sys']['mirror_name']
        popup = ForgetMirrorDialog(selected_mirror_name=mirror_name)
        popup.open()

    def forget_selected_mirror(self,*args):
        app = App.get_running_app()

        #1. Delete mirror from storage
        app.store.delete(app.selected_mirror_id)

        #2. Load buttons again
        self.mirror_toolbar.dismiss()
        self.load_buttons()

    def rename_mirror_popup(self,*args):
        app = App.get_running_app()

        mirror_name = app.store.get(app.selected_mirror_id)['sys']['mirror_name']
        popup = RenameMirrorDialog(default_name=mirror_name)
        popup.open()

    def rename_selected_mirror(self,new_name):
        app = App.get_running_app()

        #1. Update in memory
        app.selected_mirror['sys']['mirror_name'] = new_name

        #2. Update phone storage
        app.update_phone()

        #3. If mirror is online, update it
        app.update_mirror()

        #4. Refresh page to reflect changes
        self.mirror_toolbar.dismiss()
        self.load_buttons()

    def go_to_config_screen(self,mirror_id, *args):
        app = App.get_running_app()

        # 1. Declare selected_mirror_name and configs/sys
        app.selected_mirror_id = mirror_id
        app.selected_mirror = app.store.get(mirror_id)

        # 2. Go to config screen
        app.root.manager.transition.direction = 'left'
        app.root.manager.change_screen('config_screen')

        Logger.info('Opening config screen for mirror {}'.format(mirror_id))

class MirrorSelectButton(Button, FloatLayout):
    _hold_triggered = BooleanProperty(False)
    mirror_name = StringProperty()
    mirror_id = StringProperty()
    online = BooleanProperty(False)
    background_held = StringProperty()

    def on_press(self,*args):
        self._hold_triggered = False
        Clock.schedule_once(self.on_hold,.6)

    def on_release(self,*args):
        if not self._hold_triggered:
            Clock.unschedule(self.on_hold)
            app = App.get_running_app()

            if self.online:
                app.root.manager.mirror_select_screen.go_to_config_screen(self.mirror_id)
            if not self.online:
                MirrorOfflineDialog(mirror_name=self.mirror_name,mirror_id=self.mirror_id).open()

    # Brings up menu to rename or forget mirror
    def on_hold(self,*args):
        app = App.get_running_app()
        self._hold_triggered = True
        self.background_normal = self.background_held
        app.root.manager.mirror_select_screen.bring_up_toolbar(selected_mirror_id=self.mirror_id)

class ConfigScreen(ScreenTemplate):
    button_layout = ObjectProperty()
    config_toolbar = ObjectProperty()

    def on_pre_enter(self,*args):
        app = App.get_running_app()

        #1. Remove nav bar (if coming from layout screen)
        app.root.update_nav_bar(enable=False)

        #2. Load config list
        Clock.schedule_once(self.update_config_list,0)

    def on_enter(self,*args):
        app = App.get_running_app()

        #1. Update header
        app.root.update_header(title=app.selected_mirror['sys']['mirror_name'],previous_screen='mirror_select_screen')


    def update_config_list(self,*args):
        app = App.get_running_app()

        #1. Clear buttons
        self.button_layout.clear_widgets()

        #2. Clear selected config
        #app.selected_config_name = ''

        #3. Load buttons from config names in storage
        for name in app.selected_mirror['configs'].keys():
            if name==app.selected_mirror['sys']['active_config']:
                new_btn = ConfigButton(config_name=name,active_config=True)
            else:
                new_btn = ConfigButton(config_name=name)
            self.button_layout.add_widget(new_btn)

        #4. Button to create new configs
        new_config_btn = NewButton(text='New Config',on_release=self.new_config_popup)
        self.button_layout.add_widget(new_config_btn)

    def create_new_config(self,name,set_as_active=False):
        app = App.get_running_app()

        #1. Update phone storage
        app.selected_mirror['configs'][name] = {'widget_settings':{},'mirror_settings':deepcopy(MIRROR_SETTINGS)}
        if set_as_active:
            app.selected_mirror['sys']['active_config'] = name
        app.update_phone()

        #2. If mirror is online, update
        app.update_mirror()

        #3. Reload buttons list
        self.update_config_list()

        Logger.info('New config created.')

    def delete_config_popup(self,*args):
        app = App.get_running_app()
        DeleteConfigDialog(selected_config_name=app.selected_config_name).open()

    def delete_selected_config(self,*args):
        app = App.get_running_app()

        #1. Delete from dict
        app.selected_mirror['configs'].pop(app.selected_config_name)
        if app.selected_config_name == app.selected_mirror['sys']['active_config']:
            app.selected_mirror['sys']['active_config'] = None

        #2. Save phone pckl & update mirror
        app.update_phone()

        #3. Update mirror if it's online
        app.update_mirror()

        #4. Refresh button list
        self.config_toolbar.dismiss()
        self.update_config_list()

    def rename_config_popup(self,*args):
        app = App.get_running_app()
        RenameConfigDialog(default_name=app.selected_config_name).open()

    def rename_selected_config(self,new_name):
        app = App.get_running_app()

        #1. Save dict to new name, delete old name from dict
        old_config = app.selected_mirror['configs'][app.selected_config_name]
        app.selected_mirror['configs'][new_name] = old_config
        app.selected_mirror['configs'].pop(app.selected_config_name)

        #2. Update phone storage
        app.update_phone()

        #3. If mirror is online, update it
        app.update_mirror()

        #4. Refresh page to reflect changes
        self.config_toolbar.dismiss()
        self.update_config_list()


    def new_config_popup(self,*args):
        NewConfigDialog().open()

    def bring_up_toolbar(self,selected_config_name):
        app = App.get_running_app()
        app.selected_config_name = selected_config_name
        self.config_toolbar = ConfigToolBar()
        self.config_toolbar.open()

    def go_to_layout_screen(self,config_name,*args):
        app = App.get_running_app()
        app.selected_config_name = config_name
        app.root.manager.transition.direction = 'left'
        app.root.manager.change_screen('layout_screen')

        Logger.info('Going to layout screen for {}'.format(config_name))

class LayoutScreen(ScreenTemplate):
    add_widget_bar = ObjectProperty()
    toggle_scatter_bar = ObjectProperty() #Translate, Scale, Rotate
    new_widget_bar = ObjectProperty() #Place, Cancel
    edit_widget_bar = ObjectProperty()
    mirror_plus_frame = ObjectProperty()
    mirror = ObjectProperty()
    selected_widget = ObjectProperty(None,allownone=True)

    def on_pre_enter(self,*args):
        app = App.get_running_app()

        #1. Add nav bar
        app.root.update_nav_bar(enable=True)

        #2. Configure size of virtual mirror
        self.create_virtual_mirror()

        #3. Add widgets to virtual mirror
        self.load_virtual_mirror()

    def on_enter(self,*args):
        app = App.get_running_app()
        app.root.update_header(title='Layout',previous_screen='config_screen')

        # Initialize the options bars that will be used
        self.new_widget_bar = NewWidgetBar()
        self.edit_widget_bar = EditWidgetBar()

    def on_leave(self,*args):
        self.unschedule_widget_updates()

    def add_new_widget(self, new_widget_type):
        app = App.get_running_app()
        widget_settings = app.selected_mirror['configs'][app.selected_config_name]['widget_settings']

        # 1. Create unique widget name
        next_number = 1
        new_widget_name = new_widget_type
        while new_widget_name in widget_settings.keys():
            next_number += 1
            if new_widget_name+' '+str(next_number) in widget_settings.keys():
                continue
            new_widget_name += ' '+str(next_number)

        # 2. Create instance of widget
        new_widget = app.generate_widget(new_widget_type)
        new_widget.name = new_widget_name

        # 3. Add to center of virtual mirror - schedule for after kv properties have updated
        new_widget.parent_width = self.mirror.width
        new_widget.parent_height = self.mirror.height
        x = .5*self.mirror.width - .5*new_widget.width
        y = .5*self.mirror.height - .5*new_widget.height
        Clock.schedule_once(partial(self.add_widget_to_center, new_widget), 0)

        # 4. Assign to selected_widget - must schedule for after kivy properties have updated
        self.selected_widget = new_widget
        Clock.schedule_once(self.selected_widget.select, 0)

        # 5. Add new widget to virtual mirror & schedule updates
        self.mirror.add_widget(new_widget)
        Clock.schedule_interval(new_widget.update, new_widget.update_interval)

        # 6. Update toolbars
        app.root.update_nav_bar(enable=False)
        self.remove_widget(self.add_widget_bar)
        self.toggle_scatter_bar = ToggleScatterBar()  # create new instance to reset buttons
        self.add_widget(self.toggle_scatter_bar)
        self.add_widget(self.new_widget_bar)

        Logger.info("Created new widget '{}'".format(new_widget_name))

    def add_widget_to_center(self,widget,*args):
        full_pos,(full_width,full_height) = widget.full_bbox_parent
        x = .5*(self.mirror.width - full_width)
        y = .5*(self.mirror.height - full_height)
        widget.pos = (x,y)

    def place_widget(self,*args):
        app = App.get_running_app()
        selected_config = app.selected_mirror['configs'][app.selected_config_name]['widget_settings']

        #1. Update options bars
        app.root.update_nav_bar(enable=True)
        self.remove_widget(self.toggle_scatter_bar)
        if self.selected_widget.name in selected_config.keys():
            self.remove_widget(self.edit_widget_bar)  # If selected_widget already existed
        else:
            self.remove_widget(self.new_widget_bar)  # If selected_widget is a new widget
        self.add_widget(self.add_widget_bar)

        # 2. Save new widget settings to memory and then phone
        widget_name = self.selected_widget.name
        if widget_name not in selected_config.keys():
            selected_config[widget_name] = deepcopy(WIDGET_SETTINGS[self.selected_widget.type])

        selected_config[widget_name]['magnitude'] = self.selected_widget.scale
        selected_config[widget_name]['tilt'] = self.selected_widget.rotation
        selected_config[widget_name]['position'] = (self.selected_widget.x/self.mirror.width,
                                                          self.selected_widget.y/self.mirror.height)

        #3. Save changes to phone storage
        app.update_phone()

        #4. Attempt to update mirror
        app.update_mirror()

        #5. Clear selected_widget
        self.selected_widget.unselect()
        self.selected_widget = None

    def load_virtual_mirror(self,*args):
        app = App.get_running_app()
        selected_config = app.selected_mirror['configs'][app.selected_config_name]

        # 1. clear mirror of widgets
        self.unschedule_widget_updates()
        self.mirror.clear_widgets()

        # 2. Load all widgets from dictstore onto virtual mirror
        for widget_name, widget_config in selected_config['widget_settings'].items():

            # 2a. Generate instance of widget from config
            new_widget = app.generate_widget(widget_config['type'], config=widget_config)
            new_widget.name = widget_name

            # 2b. Configure size, scale, rotation
            new_widget.parent_width = self.mirror.width
            new_widget.parent_height = self.mirror.height
            new_widget.scale = widget_config['magnitude']
            new_widget.rotation = widget_config['tilt']

            # 2c. Must schedule position assignment after scale/rotation have been established
            x = self.mirror.width*widget_config['position'][0]
            y = self.mirror.height*widget_config['position'][1]
            new_widget.pos = (x, y)
            Logger.info("Adding widget '{}' to virtual mirror.".format(widget_name))

            # 2d. Schedule widget updates
            Clock.schedule_interval(new_widget.update, new_widget.update_interval)

            # 2e. Add to mirror - must schedule, so it's done after position assignment in (2c)
            self.mirror.add_widget(new_widget)

            # 2f. Check widget to make sure it is still in bounds of mirror
            Clock.schedule_once(new_widget.check_widget, 0)

    def cancel_widget(self,*args):
        app = App.get_running_app()
        config = app.selected_mirror['configs'][app.selected_config_name]

        #1. Update options bars
        app.root.update_nav_bar(enable=True)
        self.remove_widget(self.toggle_scatter_bar)
        self.add_widget(self.add_widget_bar)
        if self.selected_widget.name in config['widget_settings'].keys():
            self.remove_widget(self.edit_widget_bar)
        else:
            self.remove_widget(self.new_widget_bar) #If selected_widget was new

        #2. Restore previous widget settings, if they exist
        if self.selected_widget.name in config['widget_settings'].keys():
            widget_info = config['widget_settings'][self.selected_widget.name]
            self.selected_widget.scale = widget_info['magnitude']
            self.selected_widget.rotation = widget_info['tilt']

            # Must schedule position assignment after scale/rotation have been established
            x = self.mirror.width*widget_info['position'][0]
            y = self.mirror.height*widget_info['position'][1]
            self.selected_widget.pos = (x,y)
        else:
            self.mirror.remove_widget(self.selected_widget)
            Clock.unschedule(self.selected_widget.update)

        #3. Unselect widget
        self.selected_widget.unselect()
        self.selected_widget = None

    def edit_widget(self,widget):
        app = App.get_running_app()

        #1. Define selected widget
        self.selected_widget = widget
        self.selected_widget.select()

        #2. Update options bars
        app.root.update_nav_bar(enable=False)
        self.remove_widget(self.add_widget_bar)
        self.toggle_scatter_bar = ToggleScatterBar()
        self.add_widget(self.toggle_scatter_bar)
        self.add_widget(self.edit_widget_bar)

    def delete_widget(self,*args):
        app = App.get_running_app()

        #1. Remove selected_widget from memory and phone
        app.selected_mirror['configs'][app.selected_config_name]['widget_settings'].pop(self.selected_widget.name)
        app.update_phone()

        #2. Remove from virtual mirror & unschedule updates
        self.mirror.remove_widget(self.selected_widget)
        Clock.unschedule(self.selected_widget.update)

        #3. Attempt to update mirror
        app.update_mirror()

        #3. Clear selected_widget
        self.selected_widget.unselect()
        self.selected_widget = None

        #4. Update options bars
        app.root.update_nav_bar(enable=True)
        self.remove_widget(self.edit_widget_bar)
        self.remove_widget(self.toggle_scatter_bar)
        self.add_widget(self.add_widget_bar)

    def create_virtual_mirror(self,*args):
        app = App.get_running_app()

        #1. Determine mirror dimensions from mirror id
        mirror_ratio = app.selected_mirror['sys']['ratio']

        #2. Determine if this config has portrait or landscape
        enable_portrait = app.selected_mirror['configs'][app.selected_config_name]['mirror_settings']['enable_portrait']
        if enable_portrait:
            mirror_ratio = mirror_ratio[::-1]

        #3. Determine max available space for virtual mirror
        max_height = app.root.height - app.root.nav_bar.height\
                     -.15*app.root.height-app.root.header.height - .02*app.root.height
        max_width = .98*app.root.width

        #4. Calculate size of virtual mirror, either filling up available height or available width
        mirror_width = max_width
        mirror_height = mirror_width/mirror_ratio
        if mirror_height > max_height:
            mirror_height = max_height
            mirror_width = mirror_height*mirror_ratio
        self.mirror_plus_frame.size = (mirror_width,mirror_height)

        #5. Determine pos of mirror. Puts in middle of available y space
        self.mirror_plus_frame.y = app.root.nav_bar.height+.15*app.root.height\
                        +.5*(max_height-mirror_height)

        #4. Save the editable mirror space as an obj property, so we can add widgets to it later
        self.mirror = self.mirror_plus_frame.ids['mirror_space']

        Logger.info('Done creating virtual mirror.')

    def unschedule_widget_updates(self,*args):
        for child in self.mirror.children:
            Clock.unschedule(child.update)

class TimeWidgetScreen(ScreenTemplate):
    button_layout = ObjectProperty()
    dummy_widget = ObjectProperty()

    # Settings blocks
    autotime = ObjectProperty()
    timezone = ObjectProperty()
    enable_location = ObjectProperty()
    date_format = ObjectProperty()
    enable_military = ObjectProperty()
    enable_seconds = ObjectProperty()


    def on_pre_enter(self,*args):
        app = App.get_running_app()

        # 1. Create copy of settings that we can edit
        self.widget_name = app.root.manager.widgets_screen.selected_widget_name
        self.new_settings = deepcopy(app.root.manager.widgets_screen.selected_widget)
        self.dummy_widget = app.generate_widget('Time')

        # 2. Load buttons and stuff
        self.load_settings()

    def on_enter(self,*args):
        app = App.get_running_app()

        #1. Update title and back button
        app.root.update_header(title=self.widget_name,previous_screen='widgets_screen')

    def load_settings(self,*args):
        app = App.get_running_app()

        #0. Clear buttons list
        self.button_layout.clear_widgets()

        #1. auto-timezone
        self.button_layout.add_widget(BlockSeparator(height=20,title='LOCATION '))
        self.autotime = SwitchBlock()
        self.autotime.title = 'Automatic date & time'
        self.autotime.body = "Use your phone's GPS settings to automatically get the local date and time."
        self.autotime.setting =  self.new_settings['autotime']
        self.autotime.bind(on_setting=self.load_settings) #this gets run AFTER the line below
        self.autotime.bind(on_setting=partial(self.save_setting, 'autotime'))
        self.button_layout.add_widget(self.autotime)

        #2. Load timezone settings, if autotimezone is turned OFF
        if not self.autotime.setting:
            self.city_id = ButtonBlock()
            self.city_id.title = 'Select city'
            self.city_id.setting = self.new_settings['city_id']
            current_city = list(filter(lambda city: city['id'] == self.new_settings['city_id'], app.city_list))[0]
            self.city_id.body = 'Current city: '+current_city['name']+', '+current_city['country']
            self.city_finder_dialog = CityFinderDialog()
            self.city_finder_dialog.bind(on_select=self.set_city_id)
            self.city_id.bind(on_release=self.city_finder_dialog.open)
            self.button_layout.add_widget(self.city_id)

        # 3. Display location
        self.enable_location = SwitchBlock()
        self.enable_location.title = 'Display location'
        self.enable_location.body = 'Display location of the current time.'
        self.enable_location.setting = self.new_settings['enable_location']
        self.enable_location.bind(on_setting=partial(self.save_setting,'enable_location'))
        self.button_layout.add_widget(self.enable_location)

        # 4. Date format
        self.button_layout.add_widget(BlockSeparator(height=20,title='DATE '))
        self.date_format = ButtonBlock()
        self.date_format.title = 'Date format'
        self.date_format.setting = self.new_settings['date_format']
        self.date_format.body = 'Current format: '+self.dummy_widget.get_date(self.date_format.setting)
        self.date_dialog = DateFormatDialog()
        self.date_format.bind(on_release=self.date_dialog.open)
        self.button_layout.add_widget(self.date_format)

        #3. Military time
        self.button_layout.add_widget(BlockSeparator(height=20,title='APPEARANCE '))
        self.enable_military = SwitchBlock()
        self.enable_military.title = 'Military time'
        self.enable_military.body = 'Enable to display time in 24-hour format'
        self.enable_military.setting = self.new_settings['enable_military']
        self.enable_military.bind(on_setting=partial(self.save_setting,'enable_military'))
        self.button_layout.add_widget(self.enable_military)
        self.button_layout.add_widget(BlockSeparator())

        #5. Display seconds
        self.enable_seconds = SwitchBlock()
        self.enable_seconds.title = 'Display seconds'
        self.enable_seconds.body = 'Display the seconds to the right of the time'
        self.enable_seconds.setting = self.new_settings['enable_seconds']
        self.enable_seconds.bind(on_setting=partial(self.save_setting,'enable_seconds'))
        self.button_layout.add_widget(self.enable_seconds)
        self.button_layout.add_widget(BlockSeparator())

    def set_city_id(self,*args):
        self.city_id.setting = self.city_finder_dialog.selected_city_info['id']
        self.save_setting('city_id')#self.new_settings['city_id'] = self.city_finder_dialog.selected_city_info['id']

    def save_setting(self,key,*args):
        self.new_settings[key] = getattr(self, key).setting

        # Special cases where body text needs to be updated
        if key=='date_format':
            self.date_format.body = 'Current format: '+self.dummy_widget.get_date(self.date_format.setting)
        if key=='city_id':
            app = App.get_running_app()
            current_city = list(filter(lambda city : city['id']==self.new_settings['city_id'],app.city_list))[0]
            self.city_id.body = 'Current city: '+current_city['name']+', '+current_city['country']

    def apply_changes(self, *args):
        app = App.get_running_app()

        #1. Save new_settings and new_name to memory
        old_widget_name = app.root.manager.widgets_screen.selected_widget_name
        app.selected_mirror['configs'][app.selected_config_name]['widget_settings'].pop(old_widget_name)
        app.selected_mirror['configs'][app.selected_config_name]['widget_settings'][self.widget_name] = self.new_settings

        #2. Update selected_widget
        app.root.manager.widgets_screen.selected_widget_name = self.widget_name
        app.root.manager.widgets_screen.selected_widget = self.new_settings

        #3. Save to phone/mirror
        app.update_phone()
        app.update_mirror()

    def cancel_changes(self,*args):
        app = App.get_running_app()

        #1. Reset new_settings and new_name
        self.new_settings = deepcopy(app.root.manager.widgets_screen.selected_widget)
        self.widget_name = app.root.manager.widgets_screen.selected_widget_name

        #2. Reload settings
        self.load_settings()


class WeatherWidgetScreen(ScreenTemplate):
    button_layout = ObjectProperty()
    dummy_widget = ObjectProperty()

    # Settings blocks
    autolocation = ObjectProperty()
    metric_units = ObjectProperty()
    display_units = ObjectProperty()
    display_location = ObjectProperty()
    display_forecast = ObjectProperty()
    forecast_days = ObjectProperty()
    city_id = ObjectProperty()

    def on_pre_enter(self,*args):
        app = App.get_running_app()

        # 1. Create copy of settings that we can edit
        self.widget_name = app.root.manager.widgets_screen.selected_widget_name
        self.new_settings = deepcopy(app.root.manager.widgets_screen.selected_widget)

        # 2. Load buttons and stuff
        self.load_settings()

    def on_enter(self,*args):
        app = App.get_running_app()

        # 1. Update title and back button
        app.root.update_header(title=self.widget_name, previous_screen='widgets_screen')

    def load_settings(self, *args):
        app = App.get_running_app()

        # 0. Clear buttons list
        self.button_layout.clear_widgets()

        # 1. auto-timezone
        self.button_layout.add_widget(BlockSeparator(height=20, title='LOCATION '))
        self.autolocation = SwitchBlock()
        self.autolocation.title = 'Get local weather'
        self.autolocation.body = "Use your phone's GPS settings to automatically get the local weather."
        self.autolocation.setting = self.new_settings['autolocation']
        self.autolocation.bind(on_setting=partial(self.save_setting, 'autolocation'))
        self.button_layout.add_widget(self.autolocation)

        # 2. Load manual city select if auto is turned OFF
        if not self.autolocation.setting:
            self.city_id = ButtonBlock()
            self.city_id.title = 'Select city'
            self.city_id.setting = self.new_settings['city_id']
            # Old way:
            # list(filter(lambda city : city['id'] == self.new_settings['city_id'], app.city_list))[0]
            # ^ Searched through entire city list (in memory) for dict with matching id
            # Instead, just save city name now to pckl. Avoids issue of having to load entire json
            self.city_id.body = 'Current city: '+self.new_settings['city_name']
            self.city_finder_dialog = CityFinderDialog()
            self.city_finder_dialog.bind(on_select=partial(self.save_setting, 'city_id'))
            self.city_id.bind(on_release=self.city_finder_dialog.open)
            self.button_layout.add_widget(self.city_id)

        # 3. Display location
        self.display_location = SwitchBlock()
        self.display_location.title = 'Display location'
        self.display_location.body = 'Display the location of this weather widget.'
        self.display_location.setting = self.new_settings['display_location']
        self.display_location.bind(on_setting=partial(self.save_setting, 'display_location'))
        self.button_layout.add_widget(self.display_location)

        # 4. Forecast
        self.button_layout.add_widget(BlockSeparator(height=20, title='FORECAST '))
        self.display_forecast = SwitchBlock()
        self.display_forecast.title = 'Display forecast'
        self.display_forecast.body = "Display the weather forecast for the upcoming days."
        self.display_forecast.setting =  self.new_settings['display_forecast']
        self.display_forecast.bind(on_setting=partial(self.save_setting, 'display_forecast'))
        self.button_layout.add_widget(self.display_forecast)

        # 5. Load manual city select if auto is turned OFF
        if self.display_forecast.setting:
            self.forecast_days = ButtonBlock()
            self.forecast_days.title = 'Forecast days'
            self.forecast_days.setting = self.new_settings['forecast_days']
            self.forecast_days.body = 'Number of days in advance the forecast displays'
            self.forecast_dialog = ListDialog(list_items={'1':1,'2':2,'3':3,'4':4,'5':5})
            self.forecast_days.bind(on_release=self.forecast_dialog.open)
            self.forecast_dialog.bind(selected=partial(self.save_setting, 'forecast_days'))
            self.button_layout.add_widget(self.forecast_days)

        # 6. Units
        self.button_layout.add_widget(BlockSeparator(height=20, title='APPEARANCE '))
        self.metric_units = SwitchBlock()
        self.metric_units.title = 'Units'
        self.metric_units.setting = self.new_settings['metric_units']
        units = 'Metric' if self.new_settings['metric_units'] else 'Freedom'
        self.metric_units.body = 'Current units: '+units
        self.metric_units.bind(on_setting=partial(self.save_setting,'metric_units'))
        self.button_layout.add_widget(self.metric_units)
        self.button_layout.add_widget(BlockSeparator())

        #  7. display units
        self.display_units = SwitchBlock()
        self.display_units.title = 'Display units'
        self.display_units.setting = self.new_settings['display_units']
        self.display_units.body = 'Enable to display units on this widget'
        self.display_units.bind(on_setting=partial(self.save_setting, 'display_units'))
        self.button_layout.add_widget(self.display_units)
        self.button_layout.add_widget(BlockSeparator())

    def save_setting(self, key, *args):

        if key == 'autolocation':
            self.new_settings[key] = getattr(self, key).setting
            self.load_settings()
        if key == 'city_id':
            city_info = self.city_finder_dialog.selected_city_info
            self.new_settings['city_id'] = city_info['id']
            self.new_settings['city_name'] = city_info['name']
            self.city_id.setting = self.city_finder_dialog.selected_city_info['id']
            self.city_id.body = 'Current city: '+self.new_settings['city_name']
        if key == 'metric_units':
            units = 'Metric' if self.new_settings['metric_units'] else 'Freedom'
            self.metric_units.body = 'Current units: '+units
        if key == 'display_forecast':
            self.new_settings[key] = getattr(self, key).setting
            self.load_settings()
        if key == 'forecast_days':
            self.new_settings[key] = self.forecast_dialog.selected
            print('Saving new forecast_days as {}'.format(self.forecast_dialog.selected))
            self.forecast_days.setting = self.forecast_dialog.selected
        if key == 'display_units':
            self.new_settings[key] = getattr(self, key).setting

    def apply_changes(self, *args):
        app = App.get_running_app()

        # 1. Save new_settings and new_name to memory
        old_widget_name = app.root.manager.widgets_screen.selected_widget_name
        app.selected_mirror['configs'][app.selected_config_name]['widget_settings'].pop(old_widget_name)
        app.selected_mirror['configs'][app.selected_config_name]['widget_settings'][self.widget_name] = self.new_settings

        # 2. Update selected_widget
        app.root.manager.widgets_screen.selected_widget_name = self.widget_name
        app.root.manager.widgets_screen.selected_widget = self.new_settings

        #3. Save to phone/mirror
        app.update_phone()
        app.update_mirror()

    def cancel_changes(self,*args):
        app = App.get_running_app()

        #1. Reset new_settings and new_name
        self.new_settings = deepcopy(app.root.manager.widgets_screen.selected_widget)
        self.widget_name = app.root.manager.widgets_screen.selected_widget_name

        #2. Reload settings
        self.load_settings()

class ClockWidgetScreen(ScreenTemplate):
    def on_pre_enter(self,*args):
        app = App.get_running_app()

        #1. Create copy of settings that we can edit
        self.widget_name = app.root.manager.widgets_screen.selected_widget_name
        self.new_settings = deepcopy(app.root.manager.widgets_screen.selected_widget)
        self.dummy_widget = app.generate_widget('Clock')

        #2. Load buttons and stuff
        self.load_settings()

    def on_enter(self,*args):
        app = App.get_running_app()

        #1. Update title and back button
        app.root.update_header(title=self.widget_name,previous_screen='widgets_screen')


    def load_settings(self,*args):
        app = App.get_running_app()

        # 0. Clear buttons list
        self.button_layout.clear_widgets()

        # 5. Display seconds
        self.enable_seconds = SwitchBlock()
        self.enable_seconds.title = 'Display seconds'
        self.enable_seconds.body = 'Display seconds hand on clock'
        self.enable_seconds.setting = self.new_settings['enable_seconds']
        self.enable_seconds.bind(on_setting=partial(self.save_setting,'enable_seconds'))
        self.button_layout.add_widget(self.enable_seconds)
        self.button_layout.add_widget(BlockSeparator())

    def save_setting(self,key,*args):
        self.new_settings[key] = getattr(self, key).setting

        # Special cases where body text needs to be updated
        if key=='date_format':
            self.date_format.body = 'Current format: '+self.dummy_widget.get_date(self.date_format.setting)
        if key=='city_id':
            app = App.get_running_app()
            current_city = list(filter(lambda city : city['id']==self.new_settings['city_id'],app.city_list))[0]
            self.city_id.body = 'Current city: '+current_city['name']+', '+current_city['country']

    def apply_changes(self, *args):
        app = App.get_running_app()

        #1. Save new_settings and new_name to memory
        old_widget_name = app.root.manager.widgets_screen.selected_widget_name
        app.selected_mirror['configs'][app.selected_config_name]['widget_settings'].pop(old_widget_name)
        app.selected_mirror['configs'][app.selected_config_name]['widget_settings'][self.widget_name] = self.new_settings

        #2. Update selected_widget
        app.root.manager.widgets_screen.selected_widget_name = self.widget_name
        app.root.manager.widgets_screen.selected_widget = self.new_settings

        #3. Save to phone/mirror
        app.update_phone()
        app.update_mirror()

    def cancel_changes(self,*args):
        app = App.get_running_app()

        #1. Reset new_settings and new_name
        self.new_settings = deepcopy(app.root.manager.widgets_screen.selected_widget)
        self.widget_name = app.root.manager.widgets_screen.selected_widget_name

        #2. Reload settings
        self.load_settings()


class WidgetsScreen(ScreenTemplate):
    button_layout = ObjectProperty()
    selected_widget_name = StringProperty(None,allownone=True)
    widget_toolbar = ObjectProperty()

    def on_pre_enter(self,*args):
        app = App.get_running_app()

        #1. Create buttons layout
        self.load_widget_list()
        app.root.update_nav_bar(enable=True)

    def on_enter(self,*args):
        app = App.get_running_app()
        app.root.update_header(title='Widget Settings',previous_screen='layout_screen')

    def load_widget_list(self,*args):
        app = App.get_running_app()

        # 1. Clear list
        self.selected_widget_name = None
        self.selected_widget = {}
        self.button_layout.clear_widgets()

        # 2. Load buttons from widget names in active_config
        widget_settings = app.selected_mirror['configs'][app.selected_config_name]['widget_settings']
        num_widgets = len(widget_settings)
        for widget_name,widget_info in widget_settings.items():
            new_btn = WidgetButton(widget_name=widget_name)
            self.button_layout.add_widget(new_btn)

        new_widget_btn = NewButton(text='Add new widget!',on_release=self.add_new_widget)
        new_widget_btn.bind(on_release=self.add_new_widget)
        self.button_layout.add_widget(new_widget_btn)

        # 3. Determine height of button layout, to allow scrolling
        self.button_layout.height = 2*self.button_layout.padding[1]+new_widget_btn.height\
                                    +num_widgets*(new_widget_btn.height+self.button_layout.spacing[1])


    def add_new_widget(self,*args):
        app = App.get_running_app()

        #1. Change screen to layout_screen
        app.root.nav_bar.configure_transition(requested_screen='layout_screen')
        app.root.manager.change_screen(next_screen='layout_screen')

        #2. Open new widget selection popup, allow delay for screen transition time
        Clock.schedule_once(NewWidgetDialog().open,.39)

    def go_to_settings(self,widget_name,*args):
        app = App.get_running_app()

        #1. Set selected widget name, create copy of widget settings
        self.selected_widget_name = widget_name
        self.selected_widget = app.selected_mirror['configs'][app.selected_config_name]['widget_settings'][widget_name]

        #2. Go to settings screen for this widget type
        widget_type = self.selected_widget['type']
        app.root.manager.transition.direction = 'left'
        app.root.manager.change_screen(next_screen=widget_type.lower()+'_widget_screen')

        #3. Remove nav bar
        app.root.update_nav_bar(enable=False)

    def bring_up_toolbar(self,selected_widget_name):
        app = App.get_running_app()

        self.selected_widget_name = selected_widget_name
        self.selected_widget = app.selected_mirror['configs'][app.selected_config_name]['widget_settings'][self.selected_widget_name]
        self.widget_toolbar = WidgetToolBar()
        self.widget_toolbar.open()

    def delete_widget_popup(self,*args):
        app = App.get_running_app()
        DeleteWidgetDialog(selected_widget_name=self.selected_widget_name).open()

    def delete_selected_widget(self,*args):
        app = App.get_running_app()

        #1. Delete from memory
        app.selected_mirror['configs'][app.selected_config_name]['widget_settings'].pop(self.selected_widget_name)

        #2. Save phone pckl & update mirror
        app.update_phone()

        #3. Update mirror if it's online
        app.update_mirror()

        #4. Refresh button list
        self.widget_toolbar.dismiss()
        self.load_widget_list()

    def rename_widget_popup(self,*args):
        app = App.get_running_app()
        RenameWidgetDialog(default_name=self.selected_widget_name).open()

    def rename_selected_widget(self,new_name):
        app = App.get_running_app()

        #1. Save dict to new name, delete old name from dict
        old_config = app.selected_mirror['configs'][app.selected_config_name]['widget_settings'][self.selected_widget_name]
        app.selected_mirror['configs'][app.selected_config_name]['widget_settings'][new_name] = old_config
        app.selected_mirror['configs'][app.selected_config_name]['widget_settings'].pop(self.selected_widget_name)

        #2. Update phone storage
        app.update_phone()

        #3. If mirror is online, update it
        app.update_mirror()

        #4. Refresh page to reflect changes
        self.widget_toolbar.dismiss()
        self.load_widget_list()

class MirrorSettingsScreen(ScreenTemplate):
    button_layout = ObjectProperty()
    def on_enter(self, *args):
        app = App.get_running_app()
        app.root.update_header(title='Mirror Settings', previous_screen='layout_screen')

    def on_pre_enter(self,*args):
        app = App.get_running_app()
        app.root.update_nav_bar(enable=False)

        # 1. Create copy of settings that we can edit
        self.new_settings = deepcopy(app.selected_mirror['configs'][app.selected_config_name]['mirror_settings'])


        #2. Load buttons and stuff
        self.load_settings()

    def load_settings(self, *args):
        app = App.get_running_app()

        #0. Clear layout
        self.button_layout.clear_widgets()

        #1. Mirror name
        #self.name_block = TextInputBlock()
        #self.name_block.title = 'Name of Mirror'
        #self.name_block.body = app.selected_mirror['sys']['mirror_name']
        #self.button_layout.add_widget(self.name_block)

        #2. Enable portrait
        self.enable_portrait = SwitchBlock()
        self.enable_portrait.title = 'Mirror Orientation'
        current_orientation = 'Portrait' if self.new_settings['enable_portrait'] else "Landscape"
        self.enable_portrait.body = "Current orientation: "+current_orientation
        self.enable_portrait.setting = self.new_settings['enable_portrait']
        self.enable_portrait.bind(on_setting=partial(self.save_setting, 'enable_portrait'))
        self.button_layout.add_widget(self.enable_portrait)

        #2. Mirror brightness
        #self.brightness_block = SliderBlock()
        #self.brightness_block.title = 'Brightness'
        #self.brightness_block.body = 'Choose the brightness of the mirror display.'
        #self.brightness_block.slider_value = mirror_settings['brightness']
        #self.brightness_block.bind(on_slider=self.save_settings)
        #self.button_layout.add_widget(self.brightness_block)

    def save_setting(self, key, *args):
        self.new_settings[key] = getattr(self, key).setting

        # Special cases where body text needs to be updated
        if key == 'mirror_name':
            pass
        if key == 'enable_portrait':
            current_orientation = 'Portrait' if self.new_settings['enable_portrait'] else "Landscape"
            self.enable_portrait.body = "Current orientation: "+current_orientation

    def apply_changes(self,*args):
        app = App.get_running_app()

        #1. Save new_settings and new_name to memory
        # Save mirror name here - to do
        app.selected_mirror['configs'][app.selected_config_name]['mirror_settings'] = self.new_settings

        #2. Save to phone/mirror
        app.update_phone()
        app.update_mirror()

class MiscScreen(ScreenTemplate):
    def on_enter(self,*args):
        app = App.get_running_app()
        app.root.update_header(title='Misc Settings',previous_screen='layout_screen')
    def on_pre_enter(self,*args):
        app = App.get_running_app()
        app.root.update_nav_bar(enable=True)

    #Ideas for buttons:
    #Reset to factory button
    #About
    #Contact

class MirrorApp(App):
    connected_mirrors = DictProperty()
    #selected_mirror_id
    #selected_mirror

    selected_config_name = StringProperty()
    store = DictStore('phone_config.pckl')

    def generate_widget(self, widget_type, config={}, *args):

        # 1. Create default widget
        if widget_type == 'Time':
            new_widget = TimeWidget()
        elif widget_type == 'Weather':
            new_widget = WeatherWidget()
        elif widget_type == 'ToDoList':
            new_widget = ToDoListWidget()
        elif widget_type == 'Clock':
            new_widget = ClockWidget()
        else:
            Logger.critical('Not implemented yet howd you get here')
            return False

        # 2. Load specified configuration, if provided. Otherwise just gives default widget
        config_keys = config.keys()
        new_widget_properties = new_widget.properties()
        for key in config_keys:
            if key in new_widget_properties:
                setattr(new_widget, key, config[key])

        # 3. Update widget to reflect the above settings we just put in
        new_widget.initialize()

        return new_widget

    def get_GPS_coords(self, *args):
        Logger.info('Getting GPS coordinates *not implemented yet*')
        lat = 34.09885
        lon = -118.2896

        return lat, lon

    # Saves phone config with current sys/configs in memory
    def update_phone(self,*args):

        new_time = time.time()
        self.selected_mirror['sys']['last_edited'] = new_time

        self.store.put(self.selected_mirror_id, sys=self.selected_mirror['sys'], configs=self.selected_mirror['configs'])

        Logger.info('Updated phone storage.')

    # Takes phone config and sends it to mirror
    def update_mirror(self, mirror_id=None, *args):
        app = App.get_running_app()
        if mirror_id is None:
            mirror_id = app.selected_mirror_id

        # If mirror is online, send new config info
        if mirror_id in self.connected_mirrors.keys():
            Logger.info('Attempting to establish TCP connection with mirror {}'.format(mirror_id))

            # 1. Retrieve config from phone ** can't use self.selected_mirror if mirror_name != selected_mirror
            try:
                phone_config = app.store.get(mirror_id)
            except:
                Logger.error('Failed to load data from phone config. Could not update mirror.')
                return

            # 2. Package phone config info, in form {'sys': ..., 'configs': ...}
            try:
                data_pickled = pickle.dumps((phone_config, 'update_mirror'))
            except:
                Logger.error('Failed to pickle phone config data. Could not update mirror.')
                return

            # 3. Create TCP socket
            mirror_ip = self.connected_mirrors[mirror_id]['ip'][0]
            mirror_port = app.root.manager.mirror_select_screen.tcp_port
            try:
                s = socket.socket()
                s.connect((mirror_ip, mirror_port))
                Logger.info('Successfully connected to mirror {} on ip {}'.format(mirror_id, mirror_ip))
            except:
                Logger.error('Failed to connect to mirror {} with ip {}.'.format(mirror_id, mirror_ip))
                return

            # 4. Send phone config to mirror
            try:
                s.send(data_pickled)
                Logger.info('Successfully sent pickled config file to mirror {}. Closing socket.'.format(mirror_id))
            except:
                Logger.error('Failed to send pickled config file to mirror {} on ip {}. Closing socket.'.format(mirror_id, mirror_ip))
            s.close()
        else:
            Logger.info("Mirror is offline, can't update.")

    def load_city_list(self):
        ts = time.time()
        with open('dialogs/city_list.json') as f:
            self.city_list = json.load(f)
        Logger.info('Loaded city list in {:.2f} seconds.'.format(time.time()-ts))

    def build(self):

        if platform == 'macosx':
            Logger.info('System detected: Mac OSX.')
            Window.clearcolor = (223/256, 238/256, 250/256, 1)
            Window.size = (330, 570)
        if platform == 'android':
            Logger.info('System detected: Android')
            Window.clearcolor = (223/256, 238/256, 250/256, 1)

        self.load_city_list()

        return RootLayout()


if __name__ == '__main__':
    MirrorApp().run()

#3. Option to rearrange mirror layouts
#4. set scrollview edge conditions (to bounce back)
#5. Set so if you click and hold on "add new config" button, it maybe brings up special options
#6. Write on_hold as an event that gets triggered, and can be binded in the kv file
#7. when you hold down on config button, trigger vibrate
#8. when entering layout screen, double check to make sure configtoolbar is dismissed
#9. An extra size "spacing" is added to new widget popup
#10. Change disabled button color in new widget popup
#11. For some reason finger scrolling doesnt work on new widget popup (the touch event goes to the toggle
#button underneath instead of the scrollview)
#12. Change frame_width to be more dynamically proportional to varying size of mirror
#13. When fading mirror background, instead of doing "with canvas:", make the canvas color a ListProperty
#of the mirror and then change it
#14. Bug where if selected_widget breaks bounding box in two or more directions, it can't fix itself
#15. Make back button on layout_screen warn you if you press it while laying a new widget
#16. Iron out bugs related to limiting size of selected_widget to mirror's size
#17. MUCH LATER - assign back button on android, and what happens when you alt tab or force close
#18. For all python-defined "on__" functions, make sure I call the super().on__ function too. This may fix
#my scrolling issue in the new widgets list
#19. Have a "reverse snap" effect on scaling and rotating - For example. Don't begin scaling until you've already moved your
#fingers 5-10% of the size of the object. Or, don't start rotating until you've rotated it at least 5 deg (same as min snap
#angle)
#21. BUG: back_button reference becomes "None" if you click config button and back button repeatedly really fast
#Make CustomScatter's on_hold only register if you keep your touch over the scatter widget for the whole hold duration
#BUG IDENTIFIED: if on_hold is registered for >1 widgets, gives error. Find way to assign touch to only 1 of the widgets
#(like the one on top)
#PROBLEM: update_widget for TimeWidget constantly runs, even when not on page. Additionally, it continues even after
#you destroy a widget
#PROBLEM: if you leave and reenter layout screen numerous times, you just add a million things to the clock
#BUG: If you hold a widget to edit, then hit place, it resets the alignment to left
#22. Only trigger on_hold for config button if the final location is also over the button
#23. When you hold down widget, bind on_transform_with_touch: layout_screen.check_widget(self) and on_rotation: self.on_transform_with_touch
#BUG: When you add new widget, the border isn't properly applied
#Mirror Setting: Add feature to turn mirror off at certain times
#24.Need to disable on_hold for previewed widgetst
#25. If you update_mirror, but it can't create a socket or connect, it incorrectly updates the last edited time
#26. For MIRROR, when app closes make it shut down threads/servers too
#27. Problem: if app doesnt find any mirrors, it gets stuck in infinite loop looking for mirrors and never goes to next step
#28. Properly center "Searching for devices..." messages in window
#29. When you change widget name in time widget settings screen, doesn't update header to reflect name change
#30. Choose more concrete method for order of widgets in NewWidgetDialog - python2 has trouble fetching the items in the same
#order that they're placed in the dict (since dicts dont keep track of order in a straightforward way). Maybe alphabetically?
#Or instead of dict, create a list with 2-item tuples for each item?
#31. After renaming widget via hold-down-button method, dismiss the toolbar at the bottom automatically (and unselect widget)
#32. To enable edit-mode for widget, check that on_hold is in bounds of widget's "true_size", rather than just size
#33. When you rename mirror on mirrorselectscreen, automatically reload list of buttons (no need to multicast again)
#34. NewWidgetDialog doesn't load correctly when opened from widget settings screen
#35. If you have one config, create a second one (do NOT make active), delete the original config (the one marked as active) (so
#36. that the remaining config is still unmarked), go back to mirror screen, then bcak to config, then try to open inactive config,
#it crashes and says app.selected_mirror is empty
#37. Sometimes if you go to config screen and back to mirror screen, there are 2 identical mirror buttonsd isplayed
#38. if you're on layout screen, and press back really quckly twce, t crashes before gettng to mrror screen
#39. SEGFAULT: If you load a fresh mirror, and try adding a weather widget as your first widget, it crashes the mirror and
#     gives a seg fault. The error happens when an instance of WeatherWidget() is created
#40. When wifi turned off, gives "network" is unreachable error
#41. When you load phone app and there are no mirrors in list and you hit refresh, sometimes it crashes program
    #Cause: says searching_label weak ref doesn't exist anymore

#TODO: For weather widget, have switch option to display forecast. if checked yes, choose how many days in future to show forecast
#TODO: Create a ButtonBase that has on_hold event built in
#TODO: New png for when button is held

#TODO: Better way to order buttons
#   For example: On config screen, make the active config the ony on top (and maybe make the button a different color or have a glow)
#               Then the order of the rest of the configs should be based on how recently they were edited
#                   (or just random or alphabetical, since it's all in a dict and that'd be a huge pain to order chronologically)
#   For mirror screen: order by last_edited
#       Also: Maybe issue a warning letting them no they are deleting the active config, so no config will be displayed on mirror
#TODO: To select a widget and make it active, make touchable region within full_bbox
#TODO: To change translate,scale, or rotate custmowidget, maybe make it so fingers dont have to be on the widget itself
#TODO: Set minimum size for custom widgets
#TODO: On listdialog, make clicking anywhere on the option trigger return (not just the arrow)
#TODO: Somehow get the virtual mirror same dimensions as the actual monitor
#TODO: Fix button size issue on list
#TODO: change listdialog input to list with tuples
#TODO: Change wifi symbol into iconwithcaption
#TODO: On mirror select screen, add a "last edited: " line on buttons
#TODO: Make clicking on wifi symbol in header do something, like scan network again to see if device is now online
#TODO: Unsaved changes dialog if you leave widget settings without applying
#TODO: Make thunderstorm and snow icons for weather (and maybe add more on top of that)
#TODO: Every time you hold and then place weather widget, it queries openweathermap again (how to limit # times per hour?)


#QUALITY CONTROL TESTS
#THE FOLLOWING IS A LIST OF A TESTS THAT SHOULD BE REGULARLY DONE
#Turn wifi off/on (with router), see if app can still find mirrors
#Make new config then immediately close and reopen, see if it loads correctly
#Load list of mirror buttons while mirrors are online, turn them off, then attempt to click one of them
#Create new config on offline mirror
#Create new config on online mirror
#Select online mirror, turn mirror offline, then create a new config (does it try to socket to the mirror?)
#Select offline mirror, turn mirror online, then create new config (does it try to socket to offline mirror?)
#Try to create new config with name that already exists
#Try to create new config with empty name
#Open online mirror, create config, close app, reopen app and see if updated config info
#Open offline mirror, ^ repeat
#Open online mirror, delete config
#Open offline mirror, delete config
#Rename mirror, do all the same tests as the "create new config" section
#Create config, delete config, rename config, and then hit back button to go back to mirror select screen
#Add new widget to a config, close app, reopen and see if it loads properly

#PROBLEM:
