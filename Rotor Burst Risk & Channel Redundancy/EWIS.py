from parapy.geom import *
from parapy.core import *

from channel import ChannelY, ChannelZ, ChannelX, ChannelSweep

class Ewis(GeomBase):
    @Part
    def channel1(self):
        return ChannelX(ch_radius=0.2, position=translate(self.position, 'x', 5, 'y', 1, 'z', -0.6), color="Blue")

    @Part
    def channel2(self):
        return ChannelX(ch_radius=0.2, position=translate(self.position, 'x', 5, 'y', -1, 'z', -0.6), color="Blue")

    @Part
    def channel3(self):
        return ChannelX(ch_radius=.1, position=translate(self.position, 'x', 5, 'y', 1, 'z', 1), color="Blue")

    @Part
    def channel4(self):
        return ChannelX(ch_radius=.1, position=translate(self.position, 'x', 5, 'y', -1, 'z', 1), color='Blue')

    @Part
    def channel5(self):
        return ChannelY(ch_radius=.1, position=translate(self.position, 'x', 7, 'y', -1, 'z', -0.6), color='Blue')

    @Part
    def channel6(self):
        return ChannelY(ch_radius=.1, position=translate(self.position, 'x', 30, 'y', -1, 'z', -0.6), color='Blue')

    @Part
    def channel7(self):
        return ChannelZ(ch_radius=.1, position=translate(self.position, 'x', 30, 'y', -1, 'z', -0.6), color='Blue')

    @Part
    def channel8(self):
        return ChannelZ(ch_radius=.1, position=translate(self.position, 'x', 7, 'y', 1, 'z', -0.6), color='Blue')

    @Part
    def channel9(self):
        return ChannelZ(ch_radius=.1, position=translate(self.position, 'x', 7, 'y', -1, 'z', -0.6), color='Blue')

    @Part
    def channel10(self):
        return ChannelZ(ch_radius=.1, position=translate(self.position, 'x', 30, 'y', 1, 'z', -0.6), color='Blue')

    @Part
    def channel11(self):
        return ChannelSweep(ch_radius=.07, position=translate(self.position, 'x', 17, 'y', 1, 'z', -0.6), color='Blue')

    @Part
    def channel12(self):
        return MirroredShape(shape_in=self.channel11,
                             reference_point=self.position,
                             # Two vectors to define the mirror plane
                             vector1=self.position.Vz,
                             vector2=self.position.Vx,
                             mesh_deflection=0.0001,
                             color='Blue')
    @Part
    def channel13(self):
        return ChannelSweep(ch_radius=.07, position=translate(self.position, 'x', 20.7, 'y', 1, 'z', -0.6), color='Blue',sweep_rad=1.03, ch_length=10.5)

    @Part
    def channel14(self):
        return MirroredShape(shape_in=self.channel13,
                             reference_point=self.position,
                             # Two vectors to define the mirror plane
                             vector1=self.position.Vz,
                             vector2=self.position.Vx,
                             mesh_deflection=0.0001,
                             color='Blue')

    @Part
    def channel15(self):
        return ChannelX(ch_radius=0.07, position=translate(self.position, 'x', 21.1, 'y', 6, 'z', -0.6), color="Blue", ch_length=2.12)

    @Part
    def channel16(self):
        return MirroredShape(shape_in=self.channel15,
                             reference_point=self.position,
                             # Two vectors to define the mirror plane
                             vector1=self.position.Vz,
                             vector2=self.position.Vx,
                             mesh_deflection=0.0001,
                             color='Blue')

if __name__ == '__main__':
    from parapy.gui import display
    obj = Ewis()
    display(obj)