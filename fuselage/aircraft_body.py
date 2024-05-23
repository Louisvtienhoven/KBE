from parapy.geom import *
from parapy.core import *

from utilities.ref_frame import Frame
from fuselage.wing import Wing
from fuselage.fuselage_structure import Fuselage


class AircraftBody(GeomBase):
    @Part
    def aircraft_frame(self):
        """
        Visualize the reference frame of the aircraft
        :return: GeomBase.Frame
        """
        return Frame(
            pos=self.position
        )

    @Part
    def fuselage(self):
        """
        Create the fuselage as part
        :return: GeomBase.LoftedShell
        """
        return Fuselage(position=translate(self.position, "x"), transparency=0.5)

    @Part
    def right_wing(self):
        """
        Create the right wing of the aircraft as part
        :return: GeomBase.LoftedSolid
        """
        return Wing(
            position=translate(self.position, "x", 22, "y", 1.3, "z", -1.2),
            transparency=0.5,
        )

    @Part
    def left_wing(self):
        """
        Create the left wing of the aircraft as a mirror image of the right_wing mirrored in the xz-plane
        :return: GeomBase.LoftedSolid
        """
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
        """
        Create the vertical tail plane of the aircraft as part
        :return: GeomBase.LoftedSolid
        """
        return Wing(
            position=translate(self.position.rotate90("x"), "x", 41, "y", 1, "z", 0),
            w_semi_span=5.87,
            dihedral=0,
            transparency=0.5,
            dire='./fuselage/whitcomb_tail.dat'
        )


if __name__ == "__main__":
    from parapy.gui import display

    obj = AircraftBody(label="aircraft")
    display(obj)
