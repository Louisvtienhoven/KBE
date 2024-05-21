from parapy.geom import *
from parapy.core import *

from wiring.channel_definitions import ChannelX, ChannelVtail


class EmpennageChannels(GeomBase):
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
