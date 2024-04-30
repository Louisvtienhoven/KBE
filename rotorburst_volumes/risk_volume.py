
from parapy.geom import *
from parapy.core import *
from parapy.core.widgets import Dropdown

class RiskVolume(GeomBase):
    engines = Input()
    riskVolumeHeight = Input(10.)
    riskVolumeOrientation = Input(90.)

    # number_of_engines = list(range(engines.quantify))
    engineIndex = Input(0, widget=Dropdown([0, 1], labels=['Left', 'Right'], autocompute=True))

    # number_of_stages = list(range(engines[0].shaft.stages.quantify))
    engineStageIndex = Input(0, widget=Dropdown([0, 1, 2, 3, 4],
                                                labels=['Fan', 'LP-comp', 'HP-comp', 'HP-turb', 'LP-turb']))
    @Attribute
    def engineShaftLocation(self):
        return self.engines[self.engineIndex].position

    @Attribute
    def engineStage(self):
        return self.engines[self.engineIndex].shaft.stages[self.engineStageIndex]

    @Attribute
    def riskVolumeLength(self):
        return self.engineStage.rotorThickness

    @Attribute
    def riskVolumeWidth(self):
        return self.engineStage.bladeSpan


class CWTurning(RiskVolume):

    @Part
    def riskVolumeCWTurning(self):
        return Box(quantify=self.engineStage.rotors.quantify,
                   width=self.riskVolumeHeight,
                   length=self.engineStage.bladeSpan,
                   height=self.engineStage.rotorThickness,
                   position=translate(
                       rotate(self.engineStage.position, 'z', angle = self.riskVolumeOrientation, deg=True),
                       'y', self.engineStage.hubDiameter / 2,
                   'z', child.index * self.engineStage.rotorThickness * 2),
                   color = 'red'
                   )

class CCWTurning(RiskVolume):

    @Part
    def riskVolumeCCWTurning(self):
        return Box(quantify=self.engineStage.rotors.quantify,
                   width=self.riskVolumeHeight,
                   length=self.engineStage.bladeSpan,
                   height=self.engineStage.rotorThickness,
                   position=translate(
                       rotate(self.engineStage.position, 'z', angle = self.riskVolumeOrientation, deg=True),
                       'y', self.engineStage.hubDiameter / 2,
                   'z', child.index * self.engineStage.rotorThickness * 2,
                   'y', -1 * (self.engineStage.hubDiameter + self.engineStage.bladeSpan)),
                   color = 'red'
                   )