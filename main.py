from parapy.geom import *
from parapy.core import *
from parapy.core.widgets import Dropdown

from assembly.config_t_tail import FuselageMounted
from assembly.config_conv import WingMounted
from fuselage.aircraft_body import AircraftBody

from fuselage.EWIS import WingChannel
from rotorburst_volumes.risk_volume import CWTurning, CCWTurning


class RotorBurstAnalysis(GeomBase):
    aircraftConfig = Input(
        True,
        widget=Dropdown([True, False], labels=["Wing Mounted", "Fuselage Mounted"]),
    )

    rotationDirection = Input(1, widget=Dropdown([0, 1], labels=["CW", "CCW"]))

    @Part
    def configuration(self):
        return DynamicType(
            type=WingMounted if self.aircraftConfig == True else FuselageMounted
        )

    @Attribute
    def engines(self):
        return self.configuration.engine

    @Part
    def wiring(self):
        return WingChannel(
            front_spar_root_pos=self.structures.right_wing.front_spar_root_location,
            aft_spar_root_pos=self.structures.right_wing.aft_spar_root_location,
            front_spar_tip_pos=self.structures.right_wing.front_spar_tip_location,
            aft_spar_tip_pos=self.structures.right_wing.aft_spar_tip_location,
            color="blue",
        )

    @Part
    def structures(self):
        return AircraftBody()

    @Part
    def riskVolume(self):
        return DynamicType(
            type=CWTurning if self.rotationDirection == 0 else CCWTurning,
            engines=self.engines,
            pass_down="aircraftConfig",
        )

    @Attribute
    def channelShapes(self):
        channelShapes = []
        for part in self.wiring.parts:
            if part.TOPODIM == 3:
                channelShapes.append(part)
        return channelShapes

    # TODO: make working with CW turning as well and for all stages
    @Part
    def channelInRiskZone(self):
        return FusedSolid(
            quantify=len(self.channelShapes),
            shape_in=self.channelShapes[child.index],
            tool=self.riskVolume.riskVolumeCCWTurning[0],
            color="red",
        )  # , keep_tool=True, color='red')


if __name__ == "__main__":
    from parapy.gui import display

    obj = RotorBurstAnalysis()
    display(obj)
