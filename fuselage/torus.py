from parapy.geom import *
from parapy.core import *
from math import *

class ChannelTor(GeomBase):




    @Part
    def torus(self):
        return Torus(position=translate(self.position.rotate90('y')),major_radius=1.45, minor_radius=0.05,color='Blue',angle=4)


if __name__ == '__main__':
    from parapy.gui import display
    obj = ChannelTor()
    display(obj)