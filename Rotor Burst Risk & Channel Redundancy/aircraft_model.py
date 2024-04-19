

from parapy.geom import *
from parapy.core import *

from ref_frame import Frame
from wing import Wing
from fuselage import Fuselage
from channel import ChannelX, ChannelY



class Aircraft (GeomBase):
    @Part
    def aircraft_frame(self):
        return Frame(pos=self.position)  # this helps visualizing the aircraft reference frame, /
        # which, in this case, is the same as the global reference frame XOY)

    @Part
    def fuselage(self):
        return Fuselage(position=translate(self.position, 'x'))

    @Part
    def right_wing(self):
        return Wing(position=translate(self.position, 'x',22, 'y', 1.5, 'z', -0.8), transparency=0.5)  # the wing is defined in a different /
        # reference system than its parent aircraft
    @Part
    def left_wing(self):
        return MirroredShape(shape_in=self.right_wing,
                             reference_point=self.position,
                             # Two vectors to define the mirror plane
                             vector1=self.position.Vz,
                             vector2=self.position.Vx,
                             mesh_deflection=0.0001,
                             transparency = 0.5)



    @Part
    def channel1(self):
        return ChannelX(ch_radius= 0.2,position=translate(self.position, 'x',5, 'y',1, 'z',0.1),color="Green")

    @Part
    def channel2(self):
        return ChannelX(ch_radius= 0.2,position=translate(self.position, 'x',5, 'y', -1, 'z',0.1),color="Green")

    @Part
    def channel3(self):
        return ChannelX(ch_radius=.1, position=translate(self.position, 'x', 5, 'y', 1, 'z', 1),color="Green")

    @Part
    def channel4(self):
        return ChannelX(ch_radius=.1, position=translate(self.position, 'x', 5, 'y', -1, 'z', 1),color='Green')

    @Part
    def channelY(self):
        return ChannelY(ch_radius=.1, position=translate(self.position, 'x', 5, 'y', -1, 'z', 1),color='Green')

if __name__ == '__main__':
    from parapy.gui import display

    obj = Aircraft(label="aircraft")
    display(obj)