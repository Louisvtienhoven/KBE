

from parapy.geom import *
from parapy.core import *

from ref_frame import Frame
from wing import Wing
from fuselage import Fuselage
from channel import Channel



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
        return Wing(position=translate(self.position, 'x', 25, 'y', 2, 'z', 0))  # the wing is defined in a different /
        # reference system than its parent aircraft
    @Part
    def left_wing(self):
        return MirroredShape(shape_in=self.right_wing,
                             reference_point=self.position,
                             # Two vectors to define the mirror plane
                             vector1=self.position.Vz,
                             vector2=self.position.Vx,
                             mesh_deflection=0.0001)



    @Part
    def channel1(self):
        return Channel(ch_radius= 1,position=translate(self.position, 'x',10, 'y',1, 'z',10))

if __name__ == '__main__':
    from parapy.gui import display

    obj = Aircraft(label="aircraft")
    display(obj)
# if __name__ == '__main__':
#     from parapy.gui import display
#     obj = Fuselage(label="fuselage", mesh_deflection=0.0001)
#     display(obj)