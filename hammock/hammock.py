import pyglet
import numpy as np
from pyglet.gl import *
# %%


class Hammock():

    scale = 100
    upper_length = 4.0

    x_offset = 100
    y_offset = 100

    def __init__(self, upper_length = 4):
        self.calculate_shape(upper_length)
        self.calculate_drawing_points()
        self.draw()

    def calculate_shape(self, upper_length):
        self.slack = 0.275*upper_length
        self.height = 1.6
        self.beta = 45
        self.gamma = np.rad2deg(np.arctan(self.slack/self.upper_length))
        self.delta = self.gamma + self.beta
        self.alpha = 180 - self.delta 
        self.epsilon = self.alpha-90
        self.overhang = self.height*np.tan(np.deg2rad(self.epsilon))
        self.bottom_length = self.upper_length-2*self.overhang
        self.side_length = self.height/np.cos(np.deg2rad(self.epsilon))

        self.bottom_safety = self.height-self.slack

    def calculate_drawing_points(self):
        self.Bx = (0)*self.scale+self.x_offset
        self.By = (self.height)*self.scale+self.y_offset
        self.Ax = (self.overhang)*self.scale+self.x_offset
        self.Ay = (0)*self.scale+self.y_offset
        self.Cx = (self.upper_length)*self.scale+self.x_offset
        self.Cy = (self.height)*self.scale+self.x_offset
        self.Dx = (self.overhang+self.bottom_length)*self.scale+self.x_offset
        self.Dy = (0)*self.scale+self.y_offset
        self.Ex = (self.upper_length/2)*self.scale+self.x_offset
        self.Ey = (self.height-self.slack)*self.scale+self.y_offset

    def draw(self):
        glClear(GL_COLOR_BUFFER_BIT)
        glLoadIdentity()
        main_batch = pyglet.graphics.Batch()
        pyglet.graphics.draw(4, GL_LINES, 
                ("v2f", (0, 0, 0, 5, self.Bx, self.By, self.Ax, self.Ay))
            )
        pyglet.graphics.draw(4, GL_LINES, 
                ("v2f", (0, 0, 0, 5, self.Dx, self.Dy, self.Ax, self.Ay))
            )
        pyglet.graphics.draw(4, GL_LINES, 
                ("v2f", (0, 0, 0, 5, self.Dx, self.Dy, self.Cx, self.Cy))
            )
        pyglet.graphics.draw(4, GL_LINES, 
                ("v2f", (0, 0, 0, 5, self.Cx, self.Cy, self.Ex, self.Ey))
            )
        pyglet.graphics.draw(4, GL_LINES, 
                ("v2f", (0, 0, 0, 5, self.Bx, self.By, self.Ex, self.Ey))
            )