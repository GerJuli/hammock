import pyglet
import numpy as np
from pyglet.gl import GL_LINES, glClear, GL_COLOR_BUFFER_BIT, glLoadIdentity
# %%


class Hammock():


    max_height = 400
    max_width = 400

    max_slack = 3
    max_beta = 90

    def __init__(self, upper_length = 4, slack = 1, wood_strength = 10):
        """ All units in m, wood strength = wood_with = wood_height"""
        self.x_offset = 0
        self.y_offset = 0
        self.upper_length = upper_length
        self.slack = slack
        self.wood_strength = wood_strength
        self.beta = 45
        self.height = 1.6
        self.draw()

    def _calculate_shape(self):
        self.gamma = np.rad2deg(np.arctan(self.slack/self.upper_length))
        self.delta = self.gamma + self.beta
        self.alpha = 180 - self.delta 
        self.epsilon = self.alpha-90
        self.overhang = self.height*np.tan(np.deg2rad(self.epsilon))
        self.bottom_length = self.upper_length-2*self.overhang
        self.side_length = self.height/np.cos(np.deg2rad(self.epsilon))
        self.bottom_safety = self.height-self.slack

    def _calculate_drawing_points(self):
        width = self.upper_length
        height = self.height
        display_aspect = width / float(height)
        if display_aspect > 1:
            self.scale = self.max_width/width
        else:
            self.scale = self.max_height/height
        self.Bx = (0)*self.scale+self.x_offset
        self.By = (self.height)*self.scale+self.y_offset
        self.Ax = (self.overhang)*self.scale+self.x_offset
        self.Ay = (0)*self.scale+self.y_offset
        self.Cx = (self.upper_length)*self.scale+self.x_offset
        self.Cy = (self.height)*self.scale+self.y_offset
        self.Dx = (self.overhang+self.bottom_length)*self.scale+self.x_offset
        self.Dy = (0)*self.scale+self.y_offset
        self.Ex = (self.upper_length/2)*self.scale+self.x_offset
        self.Ey = (self.height-self.slack)*self.scale+self.y_offset

    def draw(self):
        self._calculate_shape()
        self._calculate_drawing_points()
        pyglet.gl.glLineWidth(10)
#        glClear(GL_COLOR_BUFFER_BIT)
#        glLoadIdentity()
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

    def calculate_stress(self):
        safety_coefficient = 1.2
        human_mass = 100
        gravity = 9.81
        """Strength properties are given in N/mm² Oak and Spruce wood ~30"""
        wood_strength = 30

        """Downward force of a human, sitting in the middle of the hammock"""
        Fh = human_mass*gravity
        print(f"Fh: {Fh}N")

        """Force of one rope (Newton)"""
        Fr = 0.5*Fh/(np.sin(np.deg2rad(self.gamma)))
        print(f"Fr: {Fr}N")

        """Fb: Force that bends the side part inwards"""
        Fb = np.cos(np.deg2rad(self.gamma))*Fr
        print(f"Fb: {Fb}N")

        """Momentum that bends the side part inside N*m"""
        Mb = Fb*self.side_length
        print(f"Mb: {Mb:.5}Nm")

        area_moment_of_interia_side = (self.wood_strength*1000)**4/12
        outer_fibre_distance = 0.5*self.wood_strength*1000
        section_modulus = area_moment_of_interia_side/outer_fibre_distance
        print(f"Section Modulus: {section_modulus/1000:.5}kmm³")

        """Bending Stress"""
        bending_stress_side = Mb*1000/section_modulus
        print(f"Bending Stress on side part: {bending_stress_side:.3}N/mm²")

        """Safety coefficient side"""
        safety_coefficient_side = wood_strength/bending_stress_side
        print(f"Safety coefficient side: {safety_coefficient_side:.3}")

        if safety_coefficient > safety_coefficient_side:
            print(f"Warning: safty coefficient side is {safety_coefficient_side} (< {safety_coefficient})")

    def print_results(self):
        print(f"Bottom safety: {self.bottom_safety}")
        print(f"Bottom piece: {self.bottom_length}")
        print(f"Side piece length: {self.side_length}")
        print(f"Angle: {self.alpha}")
