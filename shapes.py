from math import pi, cos, sin
from random import randint
'''
This file defines multiple different methods for drawing shapes, along with a mechanism to define which shapes to draw in layers.
'''

def circle(shape, ctx):
    ctx.arc(shape.x, shape.y, shape.radius, 0, 2*pi)

def polygon(shape, ctx, sides):
    start_angle = randint(0, 359)
    ctx.move_to(shape.x + (shape.radius * cos(start_angle * pi / 180)), shape.y + (shape.radius * sin(start_angle * pi / 180)))
    for i in range(sides - 1):
        start_angle = (start_angle + (360/sides)) % 360
        ctx.line_to(shape.x + (shape.radius * cos(start_angle * pi / 180)), shape.y + (shape.radius * sin(start_angle * pi / 180)))
    ctx.close_path()

shape_list = {
    'circle': {'function': circle},
    'polygon': {'function': polygon,
                'args': ['sides']}
}



