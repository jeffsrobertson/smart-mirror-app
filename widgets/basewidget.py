from kivy.app import App
from kivy.uix.scatterlayout import ScatterLayout
from kivy.graphics import Color, Line, InstructionGroup
from kivy.properties import StringProperty,BooleanProperty,NumericProperty,AliasProperty
from kivy.clock import Clock


class ScatterBase(ScatterLayout):
    name = StringProperty()
    _hold_triggered = BooleanProperty(False)
    selected = BooleanProperty(False)
    scale_min = NumericProperty(.2)
    do_rotation = BooleanProperty(False)
    do_scale = BooleanProperty(False)
    do_translation = BooleanProperty(False)
    parent_width = NumericProperty()
    parent_height = NumericProperty()

    # Check if the touch collides with any of the children widgets
    def collide_point(self, x, y):
        local_x,local_y = self.to_local(x, y)
        for child in self.content.walk(restrict=True):
            if child==self.content:
                continue
            if child.collide_point(local_x, local_y):
                return True
        return False

    def get_full_bbox_parent(self, *args):
        all_corners = []
        # Can also iterate through self.content.walk(restrict=True), but takes longer
        for child in self.content.children:
            if child == self.content:
                continue
            all_corners += [child.pos, (child.x, child.top), (child.right, child.y), (child.right, child.top)]
        all_corners_parent = [self.to_parent(*point) for point in all_corners]
        xmin = min([point[0] for point in all_corners_parent])
        ymin = min([point[1] for point in all_corners_parent])
        xmax = max([point[0] for point in all_corners_parent])
        ymax = max([point[1] for point in all_corners_parent])
        return (xmin, ymin), (xmax-xmin, ymax-ymin)
    full_bbox_parent = AliasProperty(get_full_bbox_parent, None)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self._hold_triggered = False

            # If this is the "selected widget", treat as a movable scatter
            if self.selected:
                return super(ScatterBase, self).on_touch_down(touch)

            # Only detect on_hold if there is no currently selected widget
            if not self.selected:
                Clock.schedule_once(self.on_hold, .6)

    def on_touch_up(self,touch):

        # Unschedule on_hold for short presses
        if not self._hold_triggered:
            Clock.unschedule(self.on_hold)

        if self.selected:
            super(ScatterBase, self).on_touch_up(touch)

    def on_hold(self, *args):
        app = App.get_running_app()

        # 1. If already selected, do nothing
        if self.selected:
            return

        # 2. If a selected widget already exists, do nothing
        if not app.root.manager.layout_screen.selected_widget:
            self._hold_triggered = True
            app.root.manager.layout_screen.edit_widget(self)

    def on_transform_with_touch(self,*args):
        self.check_widget()

    # When widget is changed, check to make sure it is still in bounds of mirror
    def check_widget(self, *args):
        (bbox_x,bbox_y),(bbox_width,bbox_height) = self.full_bbox_parent

        # 1. Size check
        if bbox_width > self.parent_width:
            widget_to_bbox_ratio = bbox_width/self.parent_width
            self.scale = self.scale/widget_to_bbox_ratio
        if bbox_height > self.parent_height:
            widget_to_bbox_ratio = bbox_height/self.parent_height
            self.scale = self.scale/widget_to_bbox_ratio

        # 2. Translation check - Make sure widget is within mirror
        bbox_right = bbox_x+bbox_width
        bbox_top = bbox_y+bbox_height
        if bbox_x < 0:
            self.x -= bbox_x
        if bbox_right > self.parent_width:
            self.x += self.parent_width - bbox_right
        if bbox_y < 0:
            self.y -= bbox_y
        if bbox_top > self.parent_height:
            self.y += self.parent_height - bbox_top

    def select(self, *args):

        # 0. Set as selected
        self.selected = True

        # 1. Locate outermost bounding box of widget
        all_corners = []
        for widget in self.content.walk(restrict=True):
            if widget == self.content:
                continue
            all_corners += [widget.pos, (widget.x, widget.top), (widget.right, widget.y), (widget.right, widget.top)]
        xmin = min([point[0] for point in all_corners])
        ymin = min([point[1] for point in all_corners])
        xmax = max([point[0] for point in all_corners])
        ymax = max([point[1] for point in all_corners])

        # 2. Draw outline around widget
        self.outline = InstructionGroup()
        self.outline.clear()
        self.outline.add(Color(.67, .816, .95, 1))
        self.outline.add(Line(points=[xmin, ymin, xmax, ymin, xmax, ymax, xmin, ymax],
                              width=2,
                              joint='none',
                              close=True))
        self.canvas.add(self.outline)

        # 3. Bring to front, make movable
        self.do_translation = True
        self.do_scale = True
        if self.rotation != 0:
            self.do_rotation = True
        self.auto_bring_to_front = True

    def unselect(self, *args):

        # 0. Deselect
        self.selected = False

        # 1. Remove outline
        self.canvas.remove(self.outline)

        # 2. Lock widget
        self.do_translation = False
        self.do_scale = False
        self.do_rotation = False
        self.auto_bring_to_front = False
