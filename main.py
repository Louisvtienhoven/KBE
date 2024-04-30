from parapy.geom import *
from parapy.core import *
from parapy.core.widgets import Dropdown

from assembly.config_t_tail import FuselageMounted
from assembly.config_conv import WingMounted
from fuselage.aircraft_body import AircraftBody

from fuselage.EWIS import WingChannel
from rotorburst_volumes.risk_volume import CWTurning, CCWTurning


class RotorBurstAnalysis(GeomBase):
    aircraft_config = Input(True, widget=Dropdown(
        [True, False], labels=["Wing Mounted", "Fuselage Mounted"]))

    rotation_direction = Input(1, widget=Dropdown(
        [0, 1], labels=["CW", "CCW"]))

    @Part
    def configuration(self):
        return DynamicType(type=WingMounted if self.aircraft_config == True else FuselageMounted)

    @Attribute
    def engines(self):
        return self.configuration.engine

    @Part
    def wiring(self):
        return WingChannel(front_spar_root_pos=self.structures.right_wing.front_spar_root_location,
                           aft_spar_root_pos=self.structures.right_wing.aft_spar_root_location,
                           front_spar_tip_pos=self.structures.right_wing.front_spar_tip_location,
                           aft_spar_tip_pos=self.structures.right_wing.aft_spar_tip_location)

    @Part
    def structures(self):
        return AircraftBody()

    @Part
    def risk_volume(self):
        return DynamicType(type=CWTurning if self.rotation_direction == 0 else CCWTurning, engines=self.engines)

    #
    # number_of_engines = list(range(engines.quantify))
    # engine_index = Input(0, widget=Dropdown(number_of_engines, autocompute=True))
    #
    # number_of_stages = list(range(engines[0].shaft.stages.quantify))
    # engine_stage_index = Input(0, widget=Dropdown(number_of_stages,
    #                                               labels=['Fan', 'LP-comp', 'HP-comp', 'HP-turb', 'LP-turb']))
    #
    # @Attribute
    # def engine_shaft_location(self):
    #     return self.engines[self.engine_index].position
    #
    # @Attribute
    # def engine_stage(self):
    #     return self.engines[self.engine_index].shaft.stages[self.engine_stage_index]
    #
    # @Attribute
    # def risk_volume_length(self):
    #     return self.engine_stage.blade_depths
    #
    # @Attribute
    # def risk_volume_width(self):
    #     return self.engine_stage.blade_heights
    #
    # @Part
    # def risk_volume_CW_turning(self):
    #     return Box(quantify=self.engine_stage.rotors.quantify,
    #                width=self.risk_volume_height,
    #                length=self.engine_stage.blade_heights,
    #                height=self.engine_stage.blade_depths,
    #                position=translate(
    #                    rotate(self.engine_stage.position,'z', angle = self.risk_volume_orientation, deg=True),
    #                    'y', self.engine_stage.stage_hub_diameter / 2,
    #                'z', child.index * self.engine_stage.blade_depths * 2),
    #                color = 'red'
    #                )
    #
    # @Part
    # def risk_volume_CCW_turning(self):
    #     return Box(quantify=self.engine_stage.rotors.quantify,
    #                width=self.risk_volume_height,
    #                length=self.engine_stage.blade_heights,
    #                height=self.engine_stage.blade_depths,
    #                position=translate(
    #                    rotate(self.engine_stage.position,'z', angle = self.risk_volume_orientation, deg=True),
    #                    'y', self.engine_stage.stage_hub_diameter / 2,
    #                'z', child.index * self.engine_stage.blade_depths * 2,
    #                'y', -1 * (self.engine_stage.stage_hub_diameter + self.engine_stage.blade_heights)),
    #                color = 'red'
    #                )
if __name__ == '__main__':
    from parapy.gui import display
    obj = RotorBurstAnalysis()
    display(obj)