from hammock import Hammock
import pyglet
from pyglet.gl import *
import weakref

def draw_rect(x, y, width, height):
    glBegin(GL_LINE_LOOP)
    glVertex2f(x, y)
    glVertex2f(x + width, y)
    glVertex2f(x + width, y + height)
    glVertex2f(x, y + height)
    glEnd()


class Control(pyglet.event.EventDispatcher):
    x = y = 0
    width = height = 10

    def __init__(self, parent):
        super(Control, self).__init__()
        self.parent = weakref.proxy(parent)

    def hit_test(self, x, y):
        return (self.x < x < self.x + self.width and
                self.y < y < self.y + self.height)

    def capture_events(self):
        self.parent.push_handlers(self)

    def release_events(self):
        self.parent.remove_handlers(self)


class Button(Control):
    charged = False

    def draw(self):
        if self.charged:
            glColor3f(1, 0, 0)
        draw_rect(self.x, self.y, self.width, self.height)
        glColor3f(1, 1, 1)
        self.draw_label()

    def on_mouse_press(self, x, y, button, modifiers):
        self.capture_events()
        self.charged = True

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        self.charged = self.hit_test(x, y)

    def on_mouse_release(self, x, y, button, modifiers):
        self.release_events()
        if self.hit_test(x, y):
            self.dispatch_event('on_press')
        self.charged = False


Button.register_event_type('on_press')


class TextButton(Button):
    def __init__(self, *args, **kwargs):
        super(TextButton, self).__init__(*args, **kwargs)
        self._text = pyglet.text.Label('', anchor_x='center', anchor_y='center')

    def draw_label(self):
        self._text.x = self.x + self.width / 2
        self._text.y = self.y + self.height / 2
        self._text.draw()

    def set_text(self, text):
        self._text.text = text

    text = property(lambda self: self._text.text,
                    set_text)


class Slider(Control):
    THUMB_WIDTH = 6
    THUMB_HEIGHT = 10
    GROOVE_HEIGHT = 2
    RESPONSIVNESS = 0.3

    def __init__(self, *args, **kwargs):
        super(Slider, self).__init__(*args, **kwargs)
        self.seek_value = None

    def draw(self):
        print("Drawing slider")
        center_y = self.y + self.height / 2
        draw_rect(self.x, center_y - self.GROOVE_HEIGHT / 2,
                  self.width, self.GROOVE_HEIGHT)
        pos = self.x + self.value * self.width / (self.max - self.min)
        #pos = 20*self.width / (self.max - self.min)
        draw_rect(pos - self.THUMB_WIDTH / 2, center_y - self.THUMB_HEIGHT / 2,
                  self.THUMB_WIDTH, self.THUMB_HEIGHT)
        print("Finished drawing slider")

    def coordinate_to_value(self, x):
        value = float(x - self.x) / self.width * (self.max - self.min) + self.min
        return value

    def on_mouse_press(self, x, y, button, modifiers):
        value = self.coordinate_to_value(x)
        self.capture_events()
        self.dispatch_event('on_begin_scroll')
        self.dispatch_event('on_change', value)
        pyglet.clock.schedule_once(self.seek_request, self.RESPONSIVNESS)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        # On some platforms, on_mouse_drag is triggered with a high frequency.
        # Seeking takes some time (~200ms). Asking for a seek at every 
        # on_mouse_drag event would starve the event loop. 
        # Instead we only record the last mouse position and we
        # schedule seek_request to dispatch the on_change event in the future.
        # This will allow subsequent on_mouse_drag to change the seek_value
        # without triggering yet the on_change event.
        value = min(max(self.coordinate_to_value(x), self.min), self.max)
        if self.seek_value is None:
            # We have processed the last recorded mouse position.
            # We re-schedule seek_request
            pyglet.clock.schedule_once(self.seek_request, self.RESPONSIVNESS)
        self.seek_value = value

    def on_mouse_release(self, x, y, button, modifiers):
        self.release_events()
        self.dispatch_event('on_end_scroll')
        self.seek_value = None

    def seek_request(self, dt):
        if self.seek_value is not None:
            self.dispatch_event('on_change', self.seek_value)
            self.seek_value = None


Slider.register_event_type('on_begin_scroll')
Slider.register_event_type('on_end_scroll')
Slider.register_event_type('on_change')


class GUI(pyglet.window.Window):
    GUI_WIDTH = 400
    GUI_HEIGHT = 40
    GUI_PADDING = 40
    GUI_BUTTON_HEIGHT = 40

    def __init__(self, hammock):
        super(GUI, self).__init__(caption='Hammock Calculator',
                                           visible=False,
                                           resizable=True)

        self.play_pause_button = TextButton(self)
        self.play_pause_button.x = self.GUI_PADDING
        self.play_pause_button.y = self.GUI_PADDING
        self.play_pause_button.height = self.GUI_BUTTON_HEIGHT
        self.play_pause_button.width = 405
        self.play_pause_button.text = "Whatever"
        
        #self.play_pause_button.on_press = hammock.print_results()
        
        self.slider = Slider(self)
        self.slider.push_handlers(self)
        self.slider.x = self.GUI_PADDING
        self.slider.y = self.GUI_PADDING * 2 + self.GUI_BUTTON_HEIGHT
        self.slider.min = 0.
        self.slider.max = 600
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        self.controls = [
                self.play_pause_button,
                self.slider
                ]

    def on_mouse_press(self, x, y, button, modifiers):
        print(f"Mouse pressed")
        for control in self.controls:
            if control.hit_test(x, y):
                print(f"Hit {control}")
                control.on_mouse_press(x, y, button, modifiers)

    def on_draw(self):
        self.clear()
        # GUI
        self.slider.value = 60
        for control in self.controls:
            print(f"drawing {control}")
            control.draw()
#hammock = Hammock()
class HamMock:
    def __init__(self):
        pass
    def print_results(self):
        print("Results here")
        
hammock = HamMock()
gui = GUI(hammock)
gui.set_visible(True)
pyglet.app.run()