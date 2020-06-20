import cairo
from random import uniform, choice
from math import pi, sqrt

import imageio
from PIL import Image
import numpy
WIDTH = 10 # width in units
HEIGHT = 10 # height in units
PIXEL_SCALE = 100 # how many pixels per unit?

surface = cairo.ImageSurface(cairo.FORMAT_RGB24, WIDTH*PIXEL_SCALE, HEIGHT*PIXEL_SCALE)

ctx = cairo.Context(surface)
ctx.scale(PIXEL_SCALE, PIXEL_SCALE)

gif_writer=imageio.get_writer("outputs/slower_gif.gif", mode="I")

# background
ctx.rectangle(0, 0, WIDTH, HEIGHT)
ctx.set_source_rgb(0, 0, 0)
ctx.fill()

base_params = {
    'min_radius': 0.05,
    'max_radius': 2,
    'max_circles': 5000,
    'max_attempts': 50,
    'padding': 0.05,
    'colours': [(212, 172, 13, 255), (169, 50, 38, 255), (36, 113, 163, 255), (19, 141, 117, 255)],
    'inner_colours': [(0, 0, 0, 255)],
    'inner_proportion': 0.9,
    'inner': False,
    'clip_walls': False
}

pride_params = {
    'min_radius': 0.05,
    'max_radius': 2.8,
    'max_circles': 5000,
    'max_attempts': 50,
    'padding': 0.05,
    'colours': [(228, 3, 3, 255), (255, 140, 0, 255), (255, 237, 0, 255), (0, 128, 38, 255), (0, 77, 255, 255), (117, 7, 135, 255)],
    'inner_colours': [(228, 3, 3, 255), (255, 140, 0, 255), (255, 237, 0, 255), (0, 128, 38, 255), (0, 77, 255, 255), (117, 7, 135, 255)],
    'inner': True,
}

tint_params = {
    'min_radius': 0.05,
    'max_radius': 2.8,
    'max_circles': 5000,
    'max_attempts': 50,
    'padding': 0.05,
    'colours': [(0, 0, 0, 255*0.25)],
}

gradient_params = {
    'min_radius': 0.05,
    'max_radius': 2,
    'max_circles': 5000,
    'max_attempts': 50,
    'padding': 0.05,
    'colours': [(212, 172, 13, 255), (169, 50, 38, 255), (36, 113, 163, 255), (19, 141, 117, 255)],
    'inner_colours': [(0, 0, 0, 255)],
    'inner_proportion': 0.9,
    'inner': False,
    'clip_walls': False,
    'is_gradient': True,
}

def as_numpy_array(surface):

    w = surface.get_width()
    h = surface.get_height()
    
    data = surface.get_data()
    
    a = numpy.ndarray(shape=(h,w), dtype=numpy.uint32, buffer=data)
    
    i = Image.frombytes("RGBA", (w,h), a, "raw", "BGRA", 0, 1)
    
    return numpy.asarray(i)

def add_image(writer, surface):
    
    a = as_numpy_array(surface)
    writer.append_data(a)

def render_circle_layer(p):
    circles = []
    for i in range(p['max_circles']):
        make_circle(p, circles)

class Circle:
    def __init__(self, min_radius, colours):
        self.x = uniform(0, WIDTH)
        self.y = uniform(0, HEIGHT)
        self.radius = min_radius
        sc = choice(colours)
        if len(colours) > 1:
            ec = choice(colours)
            while sc == ec:
                ec = choice(colours)
            self.er, self.eg, self.eb, self.ea = ec
        self.r, self.g, self.b, self.a = sc
        

def make_circle(p, circles):
    place_to_draw = False
    for i in range(p['max_attempts']):
        circle = Circle(p['min_radius'], p['colours'])

        if check_collision(circle, circles, p):
            continue
        else:
            place_to_draw = True
            break

    if not place_to_draw:
        return


    start_animation = 0.75
    while(circle.radius < p['max_radius']):
        circle.radius += start_animation
        if check_collision(circle, circles,p):
            circle.radius -= start_animation
            start_animation /= 2
            if start_animation < 0.01:
                break
        else:
            render_circle(circle, p)

    circles.append(circle)

def render_circle(circle, p):
    if circle.radius >= p.get('threshold_radius', 0):
        ctx.move_to(circle.x+circle.radius, circle.y)
        ctx.arc(circle.x, circle.y, circle.radius, 0, 2*pi)


    if p.get('is_gradient', False):
        pattern = cairo.LinearGradient(circle.x, circle.y - circle.radius, circle.x, circle.y + circle.radius)
        pattern.add_color_stop_rgba(0, circle.r/255, circle.g/255, circle.b/255, circle.a/255)
        pattern.add_color_stop_rgba(1, circle.er/255, circle.eg/255, circle.eb/255, circle.ea/255)
        ctx.set_source(pattern)
    else:
        ctx.set_source_rgba(circle.r/255, circle.g/255, circle.b/255, circle.a/255)
    ctx.fill()

    if p.get('inner', False):
        ctx.move_to(circle.x+0.6*circle.radius, circle.y)
        ctx.arc(circle.x, circle.y, p['inner_proportion']*circle.radius, 0, 2*pi)
        tint = choice(p['inner_colours'])
        ctx.set_source_rgba(tint[0]/255, tint[1]/255, tint[2]/255, tint[3]/255)
        ctx.fill()
    
    add_image(gif_writer, surface)
    

def check_collision(circle, circles, p):
    for other_circle in circles:
        max_dist = circle.radius + other_circle.radius + p['padding']
        dx = circle.x - other_circle.x
        dy = circle.y - other_circle.y

        if max_dist >= sqrt(dx*dx + dy*dy):
            return True
    if p.get('clip_walls', False):
        if (circle.x + circle.radius >= WIDTH) or (circle.x - circle.radius <= 0):
            return True
        
        if (circle.y + circle.radius >= HEIGHT) or (circle.y - circle.radius <= 0):
            return True

    return False


render_circle_layer(gradient_params)

for i in range(30):
    add_image(gif_writer, surface)
#render_circle_layer(tint_params)

surface.write_to_png('outputs/circle_packing.png')