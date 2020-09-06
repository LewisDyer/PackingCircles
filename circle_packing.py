import cairo
from random import uniform, choice, randint
from math import pi, sqrt, sin, cos

from handle_params import Layer
WIDTH = 1920 # width in units
HEIGHT = 1080 # height in units
PIXEL_SCALE = 1 # how many pixels per unit?

surface = cairo.ImageSurface(cairo.FORMAT_RGB24, WIDTH*PIXEL_SCALE, HEIGHT*PIXEL_SCALE)

ctx = cairo.Context(surface)
ctx.scale(PIXEL_SCALE, PIXEL_SCALE)

# background
ctx.rectangle(0, 0, WIDTH, HEIGHT)
ctx.set_source_rgb(0, 0, 0)
ctx.fill()

def render_circle_layer(layer):
    circles = []
    for i in range(layer.max_circles):
        draw_circle(layer, circles)

class Circle:
    def __init__(self, min_radius, colours):
        self.x = uniform(0, WIDTH)
        self.y = uniform(0, HEIGHT)
        self.radius = min_radius
        chosen_colour = choice(colours)
        self.r, self.g, self.b = chosen_colour.colour
        self.a = chosen_colour.opacity

def draw_circle(layer, circles):
    place_to_draw = False
    for i in range(layer.max_attempts):
        circle = Circle(layer.min_radius, layer.colours)

        if check_collision(circle, circles, layer):
            continue
        else:
            place_to_draw = True
            break

    if not place_to_draw:
        return


    new_radius = layer.max_radius
    for other_circle in circles:
        dx = circle.x - other_circle.x
        dy = circle.y - other_circle.y
        distance = sqrt(dx*dx + dy*dy) - other_circle.radius - layer.padding

        if distance < new_radius:
            new_radius = distance
    
    circle.radius = new_radius

    circles.append(circle)
    ctx.arc(circle.x, circle.y, circle.radius, 0, 2*pi)


    if layer.is_gradient and len(layer.colours) > 1:
        sc = choice(layer.colours)
        ec = choice(layer.colours)
        while sc == ec:
            ec = choice(layer.colours) # enforce two different colours

        pattern = cairo.LinearGradient(circle.x, circle.y - circle.radius, circle.x, circle.y + circle.radius)
        pattern.add_color_stop_rgba(0, sc.colour[0]/255, sc.colour[1]/255, sc.colour[2]/255, sc.opacity)
        pattern.add_color_stop_rgba(1, ec.colour[0]/255, ec.colour[1]/255, ec.colour[2]/255, ec.opacity)
        ctx.set_source(pattern)
    else:
        ctx.set_source_rgba(circle.r/255, circle.g/255, circle.b/255, circle.a)
    ctx.fill()

    if layer.inner:
        ctx.move_to(circle.x+layer.inner_proportion*circle.radius, circle.y)
        ctx.arc(circle.x, circle.y, layer.inner_proportion*circle.radius, 0, 2*pi)
        tint = choice(layer.inner_colours)
        ctx.set_source_rgba(tint[0]/255, tint[1]/255, tint[2]/255, tint[3])
        ctx.fill() 

def check_collision(circle, circles, layer):
    for other_circle in circles:
        max_dist = circle.radius + other_circle.radius + layer.padding
        dx = circle.x - other_circle.x
        dy = circle.y - other_circle.y

        if max_dist >= sqrt(dx*dx + dy*dy):
            return True
    if layer.clip_walls:
        if (circle.x + circle.radius >= WIDTH) or (circle.x - circle.radius <= 0):
            return True
        
        if (circle.y + circle.radius >= HEIGHT) or (circle.y - circle.radius <= 0):
            return True

    return False

if __name__ == '__main__':
    render_circle_layer(Layer('base'))
    render_circle_layer(Layer('tint'))

    surface.write_to_png('outputs/circle_packing_test.png')