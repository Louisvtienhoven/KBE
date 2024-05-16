from parapy.geom import *
from parapy.core import *

from wiring.channel_definitions import ChannelY, ChannelX, ChannelVtail
from wiring.torus import ChannelTor
from wiring.wing_channels import WingChannels


class Ewis(GeomBase):
    lower_channel_zposition = Input(-1)
    upper_channel_zposition = Input(1.2)
    channels_ypostion = Input(1.1)

    front_spar_root_pos = Input()
    aft_spar_root_pos = Input()
    front_spar_tip_pos = Input()
    aft_spar_tip_pos = Input()

    @Part
    def wing_channels(self):
        return WingChannels(pass_down="front_spar_root_pos, aft_spar_root_pos, front_spar_tip_pos, aft_spar_tip_pos")

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
            ch_length=2,
            ch_radius=0.04,
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

class ThreeChannels(Ewis):
    @Part
    def fuselage_connector(self):
        return ChannelTor(position=translate(self.position, "x", 10, "y", 0, "z", -0.2),
                          lower_channel1=self.lower_channel,
                          lower_channel2=self.lower_channel2,
                          upper_channels=[self.upper_channel])

    @Part
    def fuselage_connector2(self):
        return ChannelTor(position=translate(self.position, "x", 33, "y", 0, "z", -0.2),
                          lower_channel1 = self.lower_channel,
                          lower_channel2 = self.lower_channel2,
                          upper_channels=[self.upper_channel])

    @Part
    def upper_channel(self):
        return ChannelX(
            ch_radius=0.1,
            position=translate(
                self.position, "x", 7, "y", 0, "z", self.upper_channel_zposition
            ),
            color="Blue",
            ch_length=33.2,
        )

class FourChannels(Ewis):
    @Part
    def fuselage_connector(self):
        return ChannelTor(position=translate(self.position, "x", 10, "y", 0, "z", -0.2),
                          lower_channel1=self.lower_channel,
                          lower_channel2=self.lower_channel2,
                          upper_channels=[self.upper_channel])

    @Part
    def fuselage_connector2(self):
        return ChannelTor(position=translate(self.position, "x", 33, "y", 0, "z", -0.2),
                          lower_channel1 = self.lower_channel,
                          lower_channel2 = self.lower_channel2,
                          upper_channels=[self.upper_channel])

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

if __name__ == "__main__":
    from parapy.gui import display

    obj = FourChannels()
    display(obj)