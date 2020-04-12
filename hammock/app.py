import pyglet
import numpy as np
from hammock import Hammock
i = 1


hammock = Hammock(upper_length = 4, slack = 1)

window = pyglet.window.Window()


@window.event
def on_mouse_press(x, y, button, modifiers):
    redraw(window, hammock)

def redraw(window, hammock):
    print("Redraw")
    window.clear()
    hammock.slack = hammock.slack + 0.1
    print(f"Slack {hammock.slack}")
    hammock.calculate_shape()
    hammock.calculate_drawing_points()
    hammock.draw()
    hammock.print_results()

pyglet.app.run()