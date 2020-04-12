import pyglet
import numpy as np
from hammock import Hammock

#print(f"Bottom safety: {bottom_safety}")
#print(f"Bottom piece: {bottom_length}")
#print(f"Side piece length: {side_length}")
#print(f"Angle: {alpha}")




hammock = Hammock(upper_length = 4)

window = pyglet.window.Window()

@window.event
def on_draw():
    hammock.__init__()
pyglet.app.run()