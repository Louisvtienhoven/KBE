from parapy.geom import *
from parapy.core import *

from engine.engine_full import Engine
from fuselage.wing import Wing

from engine.engine_pylon import Pylon


class FuselageMounted(GeomBase):
    # The position of the engine in longitudinal direction (x)
    x_pos_engine_fus = Input(32)

    # The position of the engine in lateral (y) direction
    y_pos_engine_fus = Input(3)

    # The position of the engine in vertical (z) direction
    z_pos_engine_fus = Input(1)

    @Part
    def engines(self):
        """
        Create two engines as parts placed underneath the wing
        :return: sequence of Engine objects
        """
        return Engine(
            quantify=2,
            position=translate(
                self.position.rotate90("y"),
                "x",
                -1 * self.z_pos_engine_fus,
                "y",
                -1 * self.y_pos_engine_fus * (-1) ** child.index,
                "z",
                self.x_pos_engine_fus,
            ),
        )  # circles are in XY plane, thus need rotation

    @Part
    def pylon(self):
        """
        Create the engine pylon connecting the shaft to the structures
        :return: GeomBase.LoftedSolid
        """
        return Pylon(
            position=translate(
                self.position.rotate90("y"),
                "x",
                -1 * self.z_pos_engine_fus,
                "y",
                -1 * self.y_pos_engine_fus,
                "z",
                self.x_pos_engine_fus,
            ),
            length=2.0,
        )

    @Part
    def pylon_mirror(self):
        """
        Create the pylon on the left wing as a mirrored shape of pylon, mirrored in the xz-plane
        :return: GeomBase.MirroredShape
        """
        return MirroredShape(
            shape_in=self.pylon,
            reference_point=self.position,
            # Two vectors to define the mirror plane
            vector1=self.position.Vz,
            vector2=self.position.Vx,
            mesh_deflection=0.0001,
            color="Black",
        )

    @Part
    def right_h_tail(self):
        """
        Create the right half horizontal tail plane as a part
        :return: Wing object
        """
        return Wing(
            position=translate(self.position, "x", 43.0, "y", 0.1, "z", 5.8),
            w_semi_span=4.5,
            dihedral=0.5,
            w_c_root=2.5,
            w_c_tip=1.24,
            sweep_TE=15,
            transparency=0.5,
        )

    @Part
    def left_h_tail(self):
        """
        Create the left half horizontal tail plane as a part by mirroring right_h_tail in the xz-plane
        :return: GeomBase.MirroredShape of Wing object
        """
        return MirroredShape(
            shape_in=self.right_h_tail,
            reference_point=self.position,
            # Two vectors to define the mirror plane
            vector1=self.position.Vz,
            vector2=self.position.Vx,
            mesh_deflection=0.0001,
            transparency=0.5,
        )


if __name__ == "__main__":
    from parapy.gui import display

    obj = FuselageMounted()
    display(obj)
