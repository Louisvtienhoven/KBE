from parapy.geom import *
from parapy.core import *
from parapy.core.widgets import Dropdown

from assembly.config_t_tail import FuselageMounted
from assembly.config_conv import WingMounted
from fuselage.aircraft_body import AircraftBody

from fuselage.EWIS import WingChannel
from rotorburst_volumes.risk_volume import RiskVolume


class RotorBurstAnalysis(GeomBase):
    aircraftConfig = Input(
        True,
        widget=Dropdown([True, False], labels=["Wing Mounted", "Fuselage Mounted"]),
    )

    rotationDirection = Input(0, widget=Dropdown([1, 0], labels=["CW", "CCW"]))

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
        return RiskVolume(
            engines=self.engines,
            pass_down="aircraftConfig, rotationDirection",
        )

    @Attribute
    def channelShapes(self):
        channelShapes = []
        for part in self.wiring.parts:
            if part.TOPODIM == 3:
                channelShapes.append(part)
        return channelShapes

    # TODO: make working with CW turning as well and for all stages
    # @Part
    # def channelInRiskZone(self):
    #     return FusedSolid(
    #         quantify=len(self.channelShapes),
    #         shape_in=self.channelShapes[child.index],
    #         tool=self.riskVolume.riskVolumeCCWTurning[0],
    #         color="red",
    #     )  # , keep_tool=True, color='red')


if __name__ == "__main__":
    from parapy.gui import display

    obj = RotorBurstAnalysis()
    display(obj)
