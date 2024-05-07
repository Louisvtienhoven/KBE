from parapy.geom import *
from parapy.core import *
from parapy.core.widgets import Dropdown

from assembly.config_t_tail import FuselageMounted
from assembly.config_conv import WingMounted
from fuselage.aircraft_body import AircraftBody

from fuselage.EWIS import WingChannel
from rotorburst_volumes.risk_volume import RiskVolume


class RotorBurstAnalysis(GeomBase):
    # the configuration of the aircraft: wing mounted or fuselage mounted engines
    aircraft_config = Input(
        True,
        widget=Dropdown([True, False], labels=["Wing Mounted", "Fuselage Mounted"]),
    )

    @Input
    def test(self):
        return self.aircraft_config

    @Part
    def configuration(self):
        """
        The configuration of the aircraft based on [aircraft_config]
        :return: WingMounted or FuselageMounted objects with corresponding empenage layout and engine placement
        """
        return DynamicType(
            type=WingMounted if self.aircraft_config == True else FuselageMounted
        )

    @Part
    def wiring(self):
        """
        The layout of the channels in both the wing and fuselage
        :return: GeomBase.Ewis object
        """
        return WingChannel(
            front_spar_root_pos=self.structures.right_wing.front_spar_root_location,
            aft_spar_root_pos=self.structures.right_wing.aft_spar_root_location,
            front_spar_tip_pos=self.structures.right_wing.front_spar_tip_location,
            aft_spar_tip_pos=self.structures.right_wing.aft_spar_tip_location,
            color="blue"
        )

    @Part
    def structures(self):
        """
        The fuselage, wing and vertical tail models
        :return: GeomBase.AircraftBody object
        """
        return AircraftBody()

    @Part
    def risk_volume(self):
        """
        The risk volumes based on the stage of the engine of interest. The orientation of the risk volume can be modified
        by the user
        :return: GeomBase.RiskVolume object
        """
        return RiskVolume(
            engines=self.configuration.engine,
            pass_down="aircraftConfig",
        )

    @Attribute
    def channel_shapes(self):
        """
        Creates a list of all the shapes in [self.wiring] which can be used to determine intersection with a risk volume
        :return: list
        """
        channelShapes = []
        for part in self.wiring.parts:
            if part.TOPODIM == 3: # Only work with Solids
                channelShapes.append(part)
        return channelShapes

    @Part
    def channel_in_risk_zone(self):
        """
        Create fused solids for the shapes in [channel_shapes] that intersect with a risk volume at the determined
        orientation corresponding to a stage of an engine
        :return: GeomBase.FusedSolid
        """
        return FusedSolid(
            quantify=len(self.channel_shapes),
            shape_in=self.channel_shapes[child.index],
            tool=self.risk_volume.risk_volume_shell,
            color="red",
        )  # , keep_tool=True, color='red')


if __name__ == "__main__":
    from parapy.gui import display

    obj = RotorBurstAnalysis()
    display(obj)
