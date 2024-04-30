
from parapy.geom import *
from parapy.core import *
from parapy.core.widgets import Dropdown

class RiskVolume(GeomBase):
    engines = Input()
    risk_volume_height = Input(10.)
    risk_volume_orientation = Input(90.)

    # number_of_engines = list(range(engines.quantify))
    engine_index = Input(0, widget=Dropdown([0,1], labels=['Left', 'Right'], autocompute=True))

    # number_of_stages = list(range(engines[0].shaft.stages.quantify))
    engine_stage_index = Input(0, widget=Dropdown([0,1,2,3,4],
                                                  labels=['Fan', 'LP-comp', 'HP-comp', 'HP-turb', 'LP-turb']))
    @Attribute
    def engine_shaft_location(self):
        return self.engines[self.engine_index].position

    @Attribute
    def engine_stage(self):
        return self.engines[self.engine_index].shaft.stages[self.engine_stage_index]

    @Attribute
    def risk_volume_length(self):
        return self.engine_stage.blade_depths

    @Attribute
    def risk_volume_width(self):
        return self.engine_stage.blade_heights


class CWTurning(RiskVolume):

    @Part
    def risk_volume_CW_turning(self):
        return Box(quantify=self.engine_stage.rotors.quantify,
                   width=self.risk_volume_height,
                   length=self.engine_stage.blade_heights,
                   height=self.engine_stage.blade_depths,
                   position=translate(
                       rotate(self.engine_stage.position,'z', angle = self.risk_volume_orientation, deg=True),
                       'y', self.engine_stage.stage_hub_diameter / 2,
                   'z', child.index * self.engine_stage.blade_depths * 2),
                   color = 'red'
                   )

class CCWTurning(RiskVolume):

    @Part
    def risk_volume_CCW_turning(self):
        return Box(quantify=self.engine_stage.rotors.quantify,
                   width=self.risk_volume_height,
                   length=self.engine_stage.blade_heights,
                   height=self.engine_stage.blade_depths,
                   position=translate(
                       rotate(self.engine_stage.position,'z', angle = self.risk_volume_orientation, deg=True),
                       'y', self.engine_stage.stage_hub_diameter / 2,
                   'z', child.index * self.engine_stage.blade_depths * 2,
                   'y', -1 * (self.engine_stage.stage_hub_diameter + self.engine_stage.blade_heights)),
                   color = 'red'
                   )