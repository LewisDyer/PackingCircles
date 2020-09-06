from json import load
from pprint import pprint
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

        # these parameters specify the minimum and maximum radius for each circle in the image, in units.
        self.min_radius=data.get('min_radius', 0.05)
        self.max_radius=data.get('max_radius', 2)
        # this specifies the maximum amount of circles allowed in the image. Note that the actual number of circles rendered will normally be less than this.
        self.max_circles=data.get('max_circles', 5000)
        # this specifies how many different locations should be tried for placing a circle until the current circle is abandoned.
        self.max_attempts=data.get('max_attempts', 50)
        # this gives a radius around each circle that is left blank, in units.
        self.padding=data.get('padding', 0)
        

        # this determines the list of possible colours for each circle, with one colour being randomly chosen per circle.
        colour_list = data.get('colours', {"colour": "#FFFFFF"})
        self.colours = []
        for colour_dict in colour_list:
            self.colours.append(Colour(colour_dict))

        # if this parameter is true, an inner section of the circle will also be coloured, as defined by inner_colours and inner_proportion

        self.inner = data.get('inner', 'False').lower() == 'true'

        # specifies the list of possible colours for the inside of each circle
        inner_list = data.get('inner_colours', {"colour": "#FFFFFF"})
        self.inner_colours = []
        for colour_dict in colour_list:
            self.inner_colours.append(Colour(colour_dict))

        # determines how much of the inner section of the circle is filled in (based on the circle's *radius*, not area)
        self.inner_proportion = data.get('inner_proportion', 0.5)

        # if clip_walls is true, circles must fit entirely inside the boundaries of the image
        self.clip_walls = data.get('clip_walls', 'False').lower() == 'true'

        # if is_gradient is true, circles are filled in using two randomly chosen colours with a gradient between them. (does not impact inner colours)
        self.is_gradient = data.get('is_gradient', 'False').lower() == 'true'





