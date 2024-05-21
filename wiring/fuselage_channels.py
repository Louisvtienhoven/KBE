from parapy.geom import *
from parapy.core import *

from wiring.channel_definitions import ChannelY, ChannelX
from wiring.torus import ChannelTor

class FuselageChannels(GeomBase):
    lower_channel_zposition = Input(-1)
    upper_channel_zposition = Input(1.2)
    channels_ypostion = Input(1.1)

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


class ThreeChannels(FuselageChannels):
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

class FourChannels(FuselageChannels):
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