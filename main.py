from parapy.geom import *
from parapy.core import *
from parapy.core.widgets import Dropdown

from assembly.config_t_tail import FuselageMounted
from assembly.config_conv import WingMounted
from fuselage.aircraft_body import AircraftBody

from fuselage.EWIS import WingChannel4
from fuselage.EWISB import WingChannel3
from rotorburst_volumes.risk_volume import CWTurning, CCWTurning


class RotorBurstAnalysis(GeomBase):
    aircraftConfig = Input(True, widget=Dropdown(
        [True, False], labels=["Wing Mounted", "Fuselage Mounted"]))

    wiringConfig = Input(False, widget=Dropdown(
        [True, False], labels=["3 Channel Configuration", "4 Channel Configuration"]
    ))

    rotationDirection = Input(1, widget=Dropdown(
        [0, 1], labels=["CW", "CCW"]))

    @Part
    def aicraft_configuration(self):
        return DynamicType(type=WingMounted if self.aircraftConfig == True else FuselageMounted)

    @Attribute
    def engines(self):
        return self.configuration.engine

    # @Part
    # def wiring_configuration(self):
    #     return DynamicType(type=WingChannel3(front_spar_root_pos=self.structures.right_wing.front_spar_root_location,
    #                        aft_spar_root_pos=self.structures.right_wing.aft_spar_root_location,
    #                        front_spar_tip_pos=self.structures.right_wing.front_spar_tip_location,
    #                        aft_spar_tip_pos=self.structures.right_wing.aft_spar_tip_location) if self.wiringConfig == True else WingChannel4(front_spar_root_pos=self.structures.right_wing.front_spar_root_location,
    #                        aft_spar_root_pos=self.structures.right_wing.aft_spar_root_location,
    #                        front_spar_tip_pos=self.structures.right_wing.front_spar_tip_location,
    #                        aft_spar_tip_pos=self.structures.right_wing.aft_spar_tip_location))

    @Part
    def wiring_configuration(self):
        return DynamicType(type=WingChannel3 if self.wiringConfig == True else WingChannel4)

    # @Part
    # def wiring(self):
    #     return WingChannel3(front_spar_root_pos=self.structures.right_wing.front_spar_root_location,
    #                        aft_spar_root_pos=self.structures.right_wing.aft_spar_root_location,
    #                        front_spar_tip_pos=self.structures.right_wing.front_spar_tip_location,
    #                        aft_spar_tip_pos=self.structures.right_wing.aft_spar_tip_location)

    @Part
    def structures(self):
        return AircraftBody()

    @Part
    def riskVolume(self):
        return DynamicType(type=CWTurning if self.rotationDirection == 0 else CCWTurning, engines=self.engines)

if __name__ == '__main__':
    from parapy.gui import display
    obj = RotorBurstAnalysis()
    display(obj)