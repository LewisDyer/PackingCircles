from json import load
from pprint import pprint
from shapes import shape_list
'''
This file contains multiple methods for handling layer parameters. In particular, layers are defined in json files,
which are then converted into Layer objects, which are passed to rendering methods

'''
class Colour:
    def __init__(self, colour_dict):
        colour_code = colour_dict['colour'].lstrip('#')
        self.colour = tuple(int(colour_code[i:i+2], 16) for i in (0, 2, 4)) # convert to RGB tuple
        self.opacity = colour_dict.get('opacity', 1)

class Layer:
    def __init__(self, json_name):
        with open(f'params/{json_name}.json', 'r') as source:
            data = load(source)

        # these parameters specify the minimum and maximum radius for each shape in the image, in units.
        self.min_radius=data.get('min_radius', 0.05)
        self.max_radius=data.get('max_radius', 2)
        # this specifies the maximum amount of shapes allowed in the image. Note that the actual number of shapes rendered will normally be less than this.
        self.max_shapes=data.get('max_shapes', 5000)
        # this specifies how many different locations should be tried for placing a shape until the current shape is abandoned.
        self.max_attempts=data.get('max_attempts', 50)
        # this gives a radius around each shape that is left blank, in units.
        self.padding=data.get('padding', 0)
        

        # this determines the list of possible colours for each shape, with one colour being randomly chosen per shape.
        colour_list = data.get('colours', {"colour": "#FFFFFF"})
        self.colours = []
        for colour_dict in colour_list:
            self.colours.append(Colour(colour_dict))

        # if this parameter is true, an inner section of the shape will also be coloured, as defined by inner_colours and inner_proportion

        self.inner = data.get('inner', 'False').lower() == 'true'

        # if this is true, the inner section will be the same as the background colour

        self.inner_hole = data.get('inner_hole', 'False').lower() == 'true'

        # specifies the list of possible colours for the inside of each shape
        inner_list = data.get('inner_colours', {"colour": "#FFFFFF"})
        self.inner_colours = []
        for colour_dict in colour_list:
            self.inner_colours.append(Colour(colour_dict))

        # determines how much of the inner section of the shape is filled in (based on the shape's *radius*, not area)
        self.inner_proportion = data.get('inner_proportion', 0.5)

        # if clip_walls is true, shapes must fit entirely inside the boundaries of the image
        self.clip_walls = data.get('clip_walls', 'False').lower() == 'true'

        # if is_gradient is true, shapes are filled in using two randomly chosen colours with a gradient between them. (does not impact inner colours)
        self.is_gradient = data.get('is_gradient', 'False').lower() == 'true'

        self.shapes = data.get('shapes', [{"name": "circle"}])

class Background:
    def __init__(self, json_name):
        with open(f'bgs/{json_name}.json', 'r') as source:
            data = load(source)
        
        self.width = data.get('width', 500)
        self.height = data.get('height', 500)

        self.colour = Colour(data.get('colour', {"colour": "#000000"}))





