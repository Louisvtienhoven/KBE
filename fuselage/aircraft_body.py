from parapy.geom import *
from parapy.core import *

from utilities.ref_frame import Frame
from fuselage.wing import Wing
from fuselage.fuselage_structure import Fuselage


class AircraftBody(GeomBase):
    @Part
    def aircraft_frame(self):
        return Frame(
            pos=self.position
        )  # this helps visualizing the aircraft reference frame, /
        # which, in this case, is the same as the global reference frame XOY)

    @Part
    def fuselage(self):
        return Fuselage(position=translate(self.position, "x"), transparency=0.5)

    @Part
    def right_wing(self):
        return Wing(
            position=translate(self.position, "x", 22, "y", 1.3, "z", -1.2),
            transparency=0.5,
        )  # the wing is defined in a different /
        # reference system than its parent aircraft

    @Part
    def left_wing(self):
        return MirroredShape(
            shape_in=self.right_wing,
            reference_point=self.position,
            # Two vectors to define the mirror plane
            vector1=self.position.Vz,
            vector2=self.position.Vx,
            mesh_deflection=0.0001,
            transparency=0.5,
        )

    @Part
    def v_tail(self):
        return Wing(
            position=translate(self.position.rotate90("x"), "x", 41, "y", 1, "z", 0),
            w_semi_span=5.87,
            dihedral=0,
            transparency=0.5,
        )


if __name__ == "__main__":
    from parapy.gui import display

    obj = AircraftBody(label="aircraft")
    display(obj)
