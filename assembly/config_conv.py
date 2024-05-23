from parapy.geom import *
from parapy.core import *

from engine.engine_full import Engine
from fuselage.wing import Wing
from wiring.channel_definitions import ChannelSweep, ChannelZ, ChannelX

from engine.engine_pylon import Pylon


class WingMounted(GeomBase):
    # The position of the wing in longitudinal direction (x)
    x_pos_engine_wing = Input(16.5)

    # The position of the wing in lateral (y) direction
    y_pos_engine_wing = Input(5)

    # The position of the wing in vertical (z) direction
    z_pos_engine_wing = Input(-2.15)

    @Part
    def engines(self):
        """
        Create two engines as parts placed underneath the wing
        :return: sequence of Engine objects
        """
        return Engine(
            quantify=2,
            label=["left", "right"][child.index],
            position=translate(
                self.position.rotate90("y", "z"),
                "x",
                self.y_pos_engine_wing * (-1) ** child.index,
                "y",
                self.z_pos_engine_wing,
                "z",
                self.x_pos_engine_wing,
            ),
        )  # circles are in XY plane, thus need rotation

    @Part
    def pylon(self):
        """
        Create the engine pylon connecting the engine to the wing
        :return: Pylon object
        """
        return Pylon(
            position=translate(
                self.position.rotate90("y", "z"),
                "x",
                self.y_pos_engine_wing,
                "y",
                self.z_pos_engine_wing,
                "z",
                self.x_pos_engine_wing,
            ),
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
            position=translate(self.position, "x", 40.5, "y", 1.3, "z", 0),
            w_semi_span=4.5,
            dihedral=0.5,
            w_c_root=3.31,
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

    obj = WingMounted()
    display(obj)
