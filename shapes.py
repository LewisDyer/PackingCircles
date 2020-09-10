from math import pi, cos, sin
from random import randint
'''
This file defines multiple different methods for drawing shapes, along with a mechanism to define which shapes to draw in layers.
'''

def get_circle_point(shape, angle):
    # given an angle in degrees and a shape, returns the point on the bounding circle corresponding to that angle.
     x = shape.x + (shape.radius * cos(angle * pi / 180))
     y = shape.y + (shape.radius * sin(angle * pi / 180))
     return (x, y)

def circle(shape, ctx):
    ctx.arc(shape.x, shape.y, shape.radius, 0, 2*pi)

def cross(shape, ctx, lines):
    # defines a cross with the given number of rectangles, equally spaced.
    start_angle = randint(0, 359)
    for i in range(lines):
        angle_shift = 7.5 # how many degrees on either side?
        p1 = get_circle_point(shape, start_angle - angle_shift)
        p2 = get_circle_point(shape, start_angle + angle_shift)
        p3 = get_circle_point(shape, start_angle - angle_shift + 180)
        p4 = get_circle_point(shape, start_angle + angle_shift + 180)

        ctx.move_to(p1[0], p1[1])
        ctx.line_to(p2[0], p2[1])
        ctx.line_to(p3[0], p3[1])
        ctx.line_to(p4[0], p4[1])
        ctx.close_path()

        start_angle = (start_angle + (180/lines)) % 360

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
                'args': ['sides']},
    'cross': {'function': cross,
                'args': ['lines']}
}



