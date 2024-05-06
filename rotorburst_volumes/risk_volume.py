import numpy as np
from parapy.geom import *
from parapy.core import *
from parapy.core.widgets import Dropdown


class RiskVolume(GeomBase):
    aircraftConfig = Input()
    rotationDirection = Input()
    engines = Input()
    riskVolumeHeight = Input(10.0)
    riskVolumeOrientation = Input(0.0)
    spreadAngle = Input(5.0)

    # number_of_engines = list(range(engines.quantify))
    engineIndex = Input(
        0, widget=Dropdown([0, 1], labels=["Left", "Right"], autocompute=True)
    )

    # number_of_stages = list(range(engines[0].shaft.stages.quantify))
    engineStageIndex = Input(
        0,
        widget=Dropdown(
            [0, 1, 2, 3, 4], labels=["Fan", "LP-comp", "HP-comp", "HP-turb", "LP-turb"]
        ),
    )

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
    def orientationCorrection(self):
        if self.aircraftConfig != True:
            bladeOrientation = 0
        else:
            bladeOrientation = 90

        return bladeOrientation

    @Attribute
    def riskVolumePosition(self):
        return Position(self.engineStage.position,
                        orientation=Orientation(x=Vector(1,0,0),y=Vector(0,1,0),z=Vector(0,0,1)))

    @Part
    def riskVolumePlane(self):
        return Rectangle(
            width=self.engineStage.stageThickness,
            length=self.engineStage.riskVolumeSize,
            position=translate(rotate(self.riskVolumePosition,
                            'x', angle = self.riskVolumeOrientation, deg=True),
                               'x', self.engineStage.stageThickness / 2,
                            'y', self.engineStage.offAxisTranslation - self.engineStage.riskVolumeSize / 2,
                            'y', -2**self.rotationDirection * self.rotationDirection *
                               (self.engineStage.offAxisTranslation - self.engineStage.riskVolumeSize / 2))
        )

    @Part
    def riskVolumeSpread(self):
        return Rectangle(
            width=self.engineStage.stageThickness
            + 2 * np.tan(np.deg2rad(self.spreadAngle)) * self.riskVolumeHeight,
            length=self.engineStage.riskVolumeSize,
            position=translate(self.riskVolumePlane.position,
                               "z", self.riskVolumeHeight)
        )

    @Part
    def RiskZone(self):
        return LoftedShell(
            profiles=[self.riskVolumePlane, self.riskVolumeSpread],
            color="red",
            transparency=0.8,
        )