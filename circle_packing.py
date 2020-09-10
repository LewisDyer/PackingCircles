import cairo
from random import uniform, choice, randint
from math import pi, sqrt, sin, cos

from handle_params import Layer, Background
from shapes import shape_list

def render_background(bg):
    surface = cairo.ImageSurface(cairo.FORMAT_RGB24, bg.width, bg.height)

    ctx = cairo.Context(surface)
    ctx.scale(1, 1)

    # background
    ctx.rectangle(0, 0, bg.width, bg.height)
    bg_col = bg.colour.colour
    ctx.set_source_rgb(bg_col[0], bg_col[1], bg_col[2])
    ctx.fill()

    return(ctx, surface)

def render_shape_layer(bg, layer, ctx):
    shapes = define_layer(bg, layer, ctx)
    draw_layer(bg, layer, shapes, ctx)

def define_layer(bg, layer, ctx):
    shapes = []
    for i in range(layer.max_shapes):
        new_shape = create_shape(bg, layer, shapes, ctx)
        if new_shape:
            shapes.append(new_shape)
    return(shapes)

def draw_layer(bg, layer, shapes, ctx):
    for shape in shapes:
        draw_shape(bg, layer, shape, ctx)

class Shape:
    def __init__(self, bg, min_radius, colours):
        self.x = uniform(0, bg.width)
        self.y = uniform(0, bg.height)
        self.radius = min_radius
        self.angle = randint(0, 359)
        chosen_colour = choice(colours)
        self.r, self.g, self.b = chosen_colour.colour
        self.a = chosen_colour.opacity
        gradient_colour = choice(colours)
        while chosen_colour == gradient_colour and len(colours) > 1:
            gradient_colour = choice(colours)
        self.gr, self.gg, self.gb = gradient_colour.colour
        self.ga = gradient_colour.opacity


def create_shape(bg, layer, shapes, ctx):
    place_to_draw = False
    for i in range(layer.max_attempts):
        shape = Shape(bg, layer.min_radius, layer.colours)
        if check_collision(shape, shapes, layer):
            continue
        else:
            place_to_draw = True
            break

    if not place_to_draw:
        return


    new_radius = layer.max_radius
    for other_shape in shapes:
        dx = shape.x - other_shape.x
        dy = shape.y - other_shape.y
        distance = sqrt(dx*dx + dy*dy) - other_shape.radius - layer.padding

        if distance < new_radius:
            new_radius = distance
    
    shape.radius = new_radius

    return(shape)

def draw_shape(bg, layer, shape, ctx):
    draw_function = shape_list[layer.shape]['function']

    draw_function(shape, ctx, *layer.args)
    
    #ctx.arc(shape.x, shape.y, shape.radius, 0, 2*pi)


    if layer.is_gradient and len(layer.colours) > 1:
        pattern = cairo.LinearGradient(shape.x, shape.y - shape.radius, shape.x, shape.y + shape.radius)
        pattern.add_color_stop_rgba(0, shape.r/255, shape.g/255, shape.b/255, shape.a)
        pattern.add_color_stop_rgba(1,shape.gr/255, shape.gg/255, shape.gb/255, shape.ga)
        ctx.set_source(pattern)
    else:
        ctx.set_source_rgba(shape.r/255, shape.g/255, shape.b/255, shape.a)
    ctx.fill()

    if layer.inner:
        ctx.move_to(shape.x+layer.inner_proportion*shape.radius, shape.y)
        old_radius = shape.radius
        shape.radius *= layer.inner_proportion
        draw_function(shape, ctx, *layer.args)
        shape.radius = old_radius
        tint = choice(layer.inner_colours)
        if layer.inner_hole:
            tint = bg.colour
        ctx.set_source_rgba(tint.colour[0]/255, tint.colour[1]/255, tint.colour[2]/255, tint.opacity)
        ctx.fill() 

def check_collision(shape, shapes, layer):
    for other_shape in shapes:
        max_dist = shape.radius + other_shape.radius + layer.padding
        dx = shape.x - other_shape.x
        dy = shape.y - other_shape.y

        if max_dist >= sqrt(dx*dx + dy*dy):
            return True
    if layer.clip_walls:
        if (shape.x + shape.radius >= WIDTH) or (shape.x - shape.radius <= 0):
            return True
        
        if (shape.y + shape.radius >= HEIGHT) or (shape.y - shape.radius <= 0):
            return True

    return False

if __name__ == '__main__':

    bg = Background('big_black')
    ctx, surface = render_background(bg)

    render_shape_layer(bg, Layer('stream'), ctx)
    render_shape_layer(bg, Layer('stream_tint'), ctx)

    surface.write_to_png('outputs/stream_background_new.png')