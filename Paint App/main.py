# In main.py

from kivy.config import Config
Config.set('graphics', 'resizable', False)
Config.set('graphics', 'width', '960')
Config.set('graphics', 'height', '540')  # 16:9
Config.set('input', 'mouse', 'mouse, disable_multitouch')


from kivy.clock import Clock
from kivy.utils import get_color_from_hex
from kivy.uix.widget import Widget
from kivy.graphics import Color, Line, Triangle, Rectangle, Ellipse
from kivy.core.window import Window
from kivy.app import App
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.behaviors import ToggleButtonBehavior
from datetime import datetime as dt

class CanvasWidget(Widget):
    line_width = 2
    color_paint = get_color_from_hex('#2980B9')
    shape = 1
    defaut_size = 5
    start_x = 0
    start_y = 0

    def on_touch_down(self, touch):
        self.set_color(self.color_paint)
        if Widget.on_touch_down(self, touch):
            return

        with self.canvas:
            if 45 < touch.y < self.height-45 and 25 < touch.x < self.width-25:
                if self.shape == 1:
                    touch.ud['current_line'] = Line(points=(touch.x-self.defaut_size/2, touch.y-self.defaut_size/2), width=self.line_width)
                elif self.shape == 2:
                    self.start_x = touch.x-self.defaut_size/2
                    self.start_y = touch.y-self.defaut_size/2
                    touch.ud['current_ellipse'] = Ellipse(pos=(touch.x-self.defaut_size/2, touch.y-self.defaut_size/2), size=(self.defaut_size,self.defaut_size))
                elif self.shape == 3:
                    self.start_x = touch.x
                    self.start_y = touch.y-self.defaut_size
                    touch.ud['current_rectangle'] = Rectangle(pos=(touch.x, touch.y-self.defaut_size), size=(self.defaut_size,self.defaut_size))
                elif self.shape == 4:
                    touch.ud['current_triangle'] = Triangle(points=(touch.x, touch.y, touch.x+self.defaut_size/2, touch.y+self.defaut_size, touch.x+self.defaut_size, touch.y ))
                

    def set_line_width(self, line_width='Normal'):
        self.line_width = {'Thin': 1, 'Normal': 2, 'Thick': 4}[line_width]
    
    def set_shape(self, shape = 'Line'):
        self.shape = {'Line': 1, 'Circle' : 2, 'Rectangle' : 3, 'Triangle' : 4}[shape]

    def on_touch_move(self, touch):
        if 45 < touch.y < self.height-45 and 25 < touch.x < self.width-25:
            if 'current_line' in touch.ud:
                if self.shape == 1:
                    touch.ud['current_line'].points += (touch.x, touch.y)
            elif 'current_ellipse' in touch.ud:
                if self.shape == 2:
                    touch.ud['current_ellipse'].pos =(self.start_x-touch.ud['current_ellipse'].size[0]/2, self.start_y-touch.ud['current_ellipse'].size[1]/2)
                    touch.ud['current_ellipse'].size = (abs(self.start_x - touch.x), abs(self.start_y - touch.y))
            elif 'current_rectangle' in touch.ud:
                if self.shape == 3:
                    touch.ud['current_rectangle'].pos = (self.start_x, abs(self.start_y-touch.ud['current_rectangle'].size[1]))
                    touch.ud['current_rectangle'].size = (abs(self.start_x - touch.x), abs(self.start_y - touch.y))
            elif 'current_triangle' in touch.ud:
                if self.shape == 4:
                    x1 = touch.ud['current_triangle'].points[0]
                    y1 = touch.ud['current_triangle'].points[1]
                    x2 = touch.ud['current_triangle'].points[2]
                    y2 = touch.ud['current_triangle'].points[3]
                    x3 = touch.ud['current_triangle'].points[4]
                    y3 = touch.ud['current_triangle'].points[5]
                    y_change = (touch.y - y2)
                    x_change = (touch.x - x2)
                    touch.ud['current_triangle'].points = (x1, y1, x2+x_change/2, y2+y_change, x3+x_change, y3)

    def clear_canvas(self):
        color = self.color_paint
        saved = self.children[:]

        # saving before delete
        # self.save_png()

        self.clear_widgets()
        self.canvas.clear()
        for widget in saved:
            self.add_widget(widget)

        self.color_paint = color
        self.create_outline()

    def save_png(self):
        color = self.color_paint
        saved = self.children[:]  # See below

        # untuk menghapus element bukan gambar
        for i in saved:
            self.remove_widget(i)
        self.canvas.remove(self.border)

        # untuk mensave gambar menjadi png
        d = dt.now().day
        mo = dt.now().month
        y = dt.now().year

        h = dt.now().hour
        me = dt.now().minute
        s = dt.now().second
        self.export_to_png(
            'Paint{:04d}{:02d}{:02d}{:02d}{:02d}{:02d}.png'.format(y, mo, d, h, me, s))
        for widget in saved:
            self.add_widget(widget)
        self.color_paint = color
        self.create_outline()

    def create_outline(self):
        self.canvas.add(Color(*get_color_from_hex('#000000')))
        self.border = Line(points=(25, 45, 25, Window.size[1]-45,
                                   Window.size[0]-25, Window.size[1]-45,
                                   Window.size[0]-25, 45, 25, 45), width=1)
        self.canvas.add(self.border)

    def set_color(self, new_color):
        self.color_paint = new_color
        self.canvas.add(Color(*new_color))


class RadioButton(ToggleButton):
    def _do_press(self):
        if self.state == 'normal':
            ToggleButtonBehavior._do_press(self)


class PaintApp(App):
    def build(self):
        # The set_color() method will be implemented shortly.
        self.canvas_widget = CanvasWidget()
        self.canvas_widget.set_color(self.canvas_widget.color_paint)
        self.canvas_widget.create_outline()
        return self.canvas_widget


if __name__ in ('__main__', '__android__'):
    Window.clearcolor = get_color_from_hex('#FFFFFF')
    PaintApp().run()
