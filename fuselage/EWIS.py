from parapy.geom import *
from parapy.core import *

from fuselage.channel import ChannelY, ChannelZ, ChannelX, ChannelVtail


class Ewis(GeomBase):
    lower_channel_zposition = Input(-1)
    upper_channel_zposition = Input(1)
    channels_ypostion = Input(1)

    @Part
    def lower_channel(self):
        return ChannelX(
            ch_radius=0.2,
            position=translate(
                self.position,
                "x",
                5,
                "y",
                self.channels_ypostion,
                "z",
                self.lower_channel_zposition,
            ),
            color="Blue",
        )

    @Part
    def lower_channel2(self):
        return MirroredShape(
            shape_in=self.lower_channel,
            reference_point=self.position,
            # Two vectors to define the mirror plane
            vector1=self.position.Vz,
            vector2=self.position.Vx,
            mesh_deflection=0.0001,
            color="Blue",
        )

    @Part
    def upper_channel(self):
        return ChannelX(
            ch_radius=0.1,
            position=translate(
                self.position,
                "x",
                5,
                "y",
                self.channels_ypostion,
                "z",
                self.upper_channel_zposition,
            ),
            color="Blue",
            ch_length=35.2,
        )

    @Part
    def upper_channel2(self):
        return MirroredShape(
            shape_in=self.upper_channel,
            reference_point=self.position,
            # Two vectors to define the mirror plane
            vector1=self.position.Vz,
            vector2=self.position.Vx,
            mesh_deflection=0.0001,
            color="Blue",
        )

    @Part
    def connectorY1(self):
        return ChannelY(
            ch_length=self.channels_ypostion * 2,
            ch_radius=0.1,
            position=translate(
                self.position,
                "x",
                7,
                "y",
                -1 * self.channels_ypostion,
                "z",
                self.lower_channel_zposition,
            ),
            color="Blue",
        )

    @Part
    def connectorY2(self):
        return ChannelY(
            ch_length=self.channels_ypostion * 2,
            ch_radius=0.1,
            position=translate(
                self.position,
                "x",
                40,
                "y",
                -1 * self.channels_ypostion,
                "z",
                self.upper_channel_zposition,
            ),
            color="Blue",
        )

    @Part
    def connectorY3(self):
        return ChannelY(
            ch_length=self.channels_ypostion * 2,
            ch_radius=0.1,
            position=translate(
                self.position,
                "x",
                36.5,
                "y",
                -1 * self.channels_ypostion,
                "z",
                self.upper_channel_zposition,
            ),
            color="Blue",
        )

    @Part
    def connectorZ1(self):
        return ChannelZ(
            ch_length=self.upper_channel_zposition - self.lower_channel_zposition,
            ch_radius=0.1,
            position=translate(
                self.position, "x", 37.7, "y", -1, "z", self.lower_channel_zposition
            ),
            color="Blue",
        )

    @Part
    def connectorZ2(self):
        return ChannelZ(
            ch_length=self.upper_channel_zposition - self.lower_channel_zposition,
            ch_radius=0.1,
            position=translate(
                self.position, "x", 7, "y", 1, "z", self.lower_channel_zposition
            ),
            color="Blue",
        )

    @Part
    def connectorZ3(self):
        return ChannelZ(
            ch_length=self.upper_channel_zposition - self.lower_channel_zposition,
            ch_radius=0.1,
            position=translate(
                self.position, "x", 7, "y", -1, "z", self.lower_channel_zposition
            ),
            color="Blue",
        )

    @Part
    def connectorZ4(self):
        return ChannelZ(
            ch_length=self.upper_channel_zposition - self.lower_channel_zposition,
            ch_radius=0.1,
            position=translate(
                self.position, "x", 37.7, "y", 1, "z", self.lower_channel_zposition
            ),
            color="Blue",
        )

    # @Part
    # def wing_frontspar(self):
    #     return ChannelSweep(ch_radius=.07, position=translate(self.position, 'x', 17, 'y', 1, 'z', -1), color='Blue')
    #
    # @Part
    # def wing_frontspar2(self):
    #     return MirroredShape(shape_in=self.wing_frontspar,
    #                          reference_point=self.position,
    #                          # Two vectors to define the mirror plane
    #                          vector1=self.position.Vz,
    #                          vector2=self.position.Vx,
    #                          mesh_deflection=0.0001,
    #                          color='Blue')
    # @Part
    # def wing_aftspar(self):
    #     return ChannelSweep(ch_radius=.07, position=translate(self.position, 'x', 20.7, 'y', 1, 'z', -1.05), color='Blue',sweep_rad=1.03, dihedral=0.145, ch_length=10.5)

    # @Part
    # def wing_aftspar2(self):
    #     return MirroredShape(shape_in=self.wing_aftspar,
    #                          reference_point=self.position,
    #                          # Two vectors to define the mirror plane
    #                          vector1=self.position.Vz,
    #                          vector2=self.position.Vx,
    #                          mesh_deflection=0.0001,
    #                          color='Blue')

    @Part
    def wing_connector(self):
        return ChannelX(
            ch_radius=0.06,
            position=translate(self.position, "x", 21.1, "y", 6, "z", -0.6),
            color="Blue",
            ch_length=2.15,
        )

    @Part
    def wing_connector2(self):
        return MirroredShape(
            shape_in=self.wing_connector,
            reference_point=self.position,
            # Two vectors to define the mirror plane
            vector1=self.position.Vz,
            vector2=self.position.Vx,
            mesh_deflection=0.0001,
            color="Blue",
        )

    @Part
    def vtail_frontspar(self):
        return ChannelVtail(
            ch_radius=0.04,
            position=translate(self.position, "x", 36.5, "y", 0, "z", 1),
            color="Blue",
            sweep_rad=0.33,
            dihedral=0.0,
            ch_length=6.5,
        )

    @Part
    def vtail_aftspar(self):
        return ChannelVtail(
            ch_radius=0.04,
            position=translate(self.position, "x", 40, "y", 0, "z", 1),
            color="Blue",
            sweep_rad=1.0,
            dihedral=0.0,
            ch_length=5.5,
        )

    @Part
    def vtail_connector(self):
        return ChannelX(
            ch_radius=0.02,
            position=translate(self.position, "x", 39.3, "y", 0, "z", 4),
            color="Blue",
            ch_length=2.3,
        )

class WingChannel4(Ewis):
    front_spar_tip_pos = Input(Position(Point(0,0,0)))
    front_spar_root_pos = Input(Position(Point(1,0,0)))
    aft_spar_tip_pos = Input(Position(Point(0,1,0)))
    aft_spar_root_pos = Input(Position(Point(1,1,0)))

    @Attribute
    def front_spar_plane_normal(self):
        return self.front_spar_tip_pos - self.front_spar_root_pos

    @Attribute
    def aft_spar_plane_normal(self):
        return self.aft_spar_tip_pos - self.aft_spar_root_pos

    @Part
    def front_spar(self):
        return LineSegment(
            start=self.front_spar_root_pos.point,
            end=self.front_spar_tip_pos.point,
            hidden=True,
        )

    @Part
    def aft_spar(self):
        return LineSegment(
            start=self.aft_spar_root_pos.point,
            end=self.aft_spar_tip_pos.point,
            hidden=True,
        )

    @Part
    def rightWingFrontSpar(self):
        return PipeSolid(path=self.front_spar, radius=0.07)

    @Part
    def rightWingAftSpar(self):
        return PipeSolid(path=self.aft_spar, radius=0.07)

    @Part
    def leftWingFrontSpar(self):
        return MirroredShape(
            shape_in=self.rightWingFrontSpar,
            reference_point=self.position,
            # Two vectors to define the mirror plane
            vector1=self.position.Vz,
            vector2=self.position.Vx,
            mesh_deflection=0.0001,
        )

    @Part
    def leftWingAftSpar(self):
        return MirroredShape(
            shape_in=self.rightWingAftSpar,
            reference_point=self.position,
            vector1=self.position.Vz,
            vector2=self.position.Vx,
            mesh_deflection=0.0001,
        )


if __name__ == "__main__":
    from parapy.gui import display

    obj = WingChannel4()
    display(obj)
