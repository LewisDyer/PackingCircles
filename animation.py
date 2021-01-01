# Produces a gif rendering an image with rotating shapes.
import imageio
from PIL import Image
import numpy

import circle_packing, handle_params

NO_FRAMES = 360

gif_writer=imageio.get_writer("outputs/playstation.mp4", mode="I", fps=60)

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

bg = handle_params.Background('big_black')
ctx, surface = circle_packing.render_background(bg)

stream, stream_tint = handle_params.Layer('nse'), handle_params.Layer('playstation_tint')
main_shapes = circle_packing.define_layer(bg, stream, ctx)
tint_shapes = circle_packing.define_layer(bg, stream_tint, ctx)

for i in range(NO_FRAMES):
    circle_packing.draw_layer(bg, stream, main_shapes, ctx)
    circle_packing.draw_layer(bg, stream_tint, tint_shapes, ctx)

    add_image(gif_writer, surface)
    for shape in main_shapes:
        shape.angle = (shape.angle + (360/NO_FRAMES)) % 360
    for shape in tint_shapes:
        shape.angle = (shape.angle + (360/NO_FRAMES)) % 360

    ctx.rectangle(0, 0, bg.width, bg.height)
    bg_col = bg.colour.colour
    ctx.set_source_rgb(bg_col[0], bg_col[1], bg_col[2])
    ctx.fill()