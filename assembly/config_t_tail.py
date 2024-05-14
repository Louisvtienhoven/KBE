from parapy.geom import *
from parapy.core import *

from engine.engine_full import Engine
from fuselage.wing import Wing
from fuselage.channel import ChannelSweep, ChannelX

from engine.engine_pylon import Pylon


class FuselageMounted(GeomBase):
    y_pos_engine_fus = Input(3)
    z_pos_engine_fus = Input(1.0)
    x_pos_engine_fus = Input(32)

    @Part
    def engine(self):
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
        return MirroredShape(
            shape_in=self.pylon,
            reference_point=self.position,
            # Two vectors to define the mirror plane
            vector1=self.position.Vz,
            vector2=self.position.Vx,
            mesh_deflection=0.0001,
            color="Black",
        )

    # @Part
    # def engine(self):
    #     return Engine(quantify=2,
    #                   position=translate(self.position.rotate90('y'),
    #                                      'x', -1*self.y_pos_engine_wing ,
    #                                      'y', -1*self.z_pos_engine_wing * (-1) ** child.index,
    #                                      'z', self.x_pos_engine_wing)
    #                   )  # circles are in XY plane, thus need rotation

    @Part
    def h_tail(self):
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
    def channel_htail1(self):
        return ChannelSweep(
            ch_radius=0.02,
            position=translate(self.position, "x", 41, "y", 0, "z", 5.85),
            color="Blue",
            sweep_rad=1.05,
            ch_length=4,
            dihedral=0.15,
        )

    @Part
    def channel_htail2(self):
        return MirroredShape(
            shape_in=self.channel_htail1,
            reference_point=self.position,
            # Two vectors to define the mirror plane
            vector1=self.position.Vz,
            vector2=self.position.Vx,
            mesh_deflection=0.0001,
            color="Blue",
        )

    @Part
    def channel_htail3(self):
        return ChannelSweep(
            ch_radius=0.02,
            position=translate(self.position, "x", 42.8, "y", 0, "z", 5.8),
            color="Blue",
            sweep_rad=1.3,
            dihedral=0.4,
            ch_length=3.3,
        )

    @Part
    def channel_htail4(self):
        return MirroredShape(
            shape_in=self.channel_htail3,
            reference_point=self.position,
            # Two vectors to define the mirror plane
            vector1=self.position.Vz,
            vector2=self.position.Vx,
            mesh_deflection=0.0001,
            color="Blue",
        )

    @Part
    def channel_htail7(self):
        return ChannelX(
            ch_radius=0.02,
            position=translate(self.position, "x", 41.65, "y", 1.2, "z", 5.9),
            color="Blue",
            ch_length=1.47,
        )

    @Part
    def channel_htail8(self):
        return MirroredShape(
            shape_in=self.channel_htail7,
            reference_point=self.position,
            # Two vectors to define the mirror plane
            vector1=self.position.Vz,
            vector2=self.position.Vx,
            mesh_deflection=0.0001,
            color="Blue",
        )

    @Part
    def mirrored_h_tail(self):
        return MirroredShape(
            shape_in=self.h_tail,
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
