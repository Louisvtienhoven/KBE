import numpy as np
from parapy.geom import *
from parapy.core import *
from parapy.core.widgets import Dropdown
from numpy import tan


class RiskVolume(GeomBase):
    aircraftConfig = Input()
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
            bladeOrientation = 180
        else:
            bladeOrientation = 90

        return bladeOrientation

    @Part
    def riskVolumePlane(self):
        return Rectangle(
            width=self.engineStage.stageThickness,
            length=self.engineStage.riskVolumeSize,
            position=self.position,
        )

    @Part
    def riskVolumeSpread(self):
        return Rectangle(
            width=self.engineStage.stageThickness
            + 2 * np.tan(np.deg2rad(self.spreadAngle)) * self.riskVolumeHeight,
            length=self.engineStage.riskVolumeSize,
            position=translate(self.position, "z", self.riskVolumeHeight),
        )


class CWTurning(RiskVolume):
    @Part
    def testRiskVolume(self):
        return LoftedShell(
            profiles=[self.riskVolumePlane, self.riskVolumeSpread],
            position=translate(
                rotate(
                    self.engineStage.position,
                    "z",
                    angle=self.riskVolumeOrientation + self.orientationCorrection,
                    deg=True,
                ),
                "y",
                -1
                * (
                    self.engineStage.riskVolumeSize
                    - self.engineStage.offAxisTranslation
                ),
                "z",
                child.index * self.engineStage.rotorThickness * 2,
            ),
            color="red",
            transparency=0.8,
        )

    @Part
    def riskVolumeCWTurning(self):
        return Box(
            quantify=self.engineStage.rotors.quantify,
            width=self.riskVolumeHeight,
            length=self.engineStage.riskVolumeSize,
            height=self.engineStage.rotorThickness,
            position=translate(
                rotate(
                    self.engineStage.position,
                    "z",
                    angle=self.riskVolumeOrientation + self.orientationCorrection,
                    deg=True,
                ),
                "y",
                -1
                * (
                    self.engineStage.riskVolumeSize
                    - self.engineStage.offAxisTranslation
                ),
                "z",
                child.index * self.engineStage.rotorThickness * 2,
            ),
            color="red",
            transparency=0.8,
        )


class CCWTurning(RiskVolume):
    @Part
    def testRiskVolume(self):
        return LoftedShell(
            profiles=[self.riskVolumePlane, self.riskVolumeSpread],
            position=translate(
                rotate(
                    self.engineStage.position,
                    "z",
                    angle=self.riskVolumeOrientation + self.orientationCorrection,
                    deg=True,
                ),
                "y",
                -1 * (self.engineStage.offAxisTranslation),
            ),
            color="red",
            transparency=0.8,
        )

    @Part
    def riskVolumeCCWTurning(self):
        return Box(
            width=self.riskVolumeHeight,
            length=self.engineStage.riskVolumeSize,
            height=self.engineStage.rotorThickness,
            position=translate(
                rotate(
                    self.engineStage.position,
                    "z",
                    angle=self.riskVolumeOrientation + self.orientationCorrection,
                    deg=True,
                ),
                "y",
                -1 * (self.engineStage.offAxisTranslation),
            ),
            color="red",
        )

    # @Part
    # def riskVolumeCCWTurning(self):
    #     return Box(quantify=self.engineStage.rotors.quantify,
    #                width=self.riskVolumeHeight,
    #                length=self.engineStage.riskVolumeSize,
    #                height=self.engineStage.rotorThickness,
    #                position=translate(
    #                    rotate(self.engineStage.position, 'z',
    #                           angle = self.riskVolumeOrientation + self.orientationCorrection, deg=True),
    #                    'y', self.engineStage.offAxisTranslation,
    #                'z', child.index * self.engineStage.rotorThickness * 2,
    #                'y', -1 * (self.engineStage.hubDiameter + self.engineStage.bladeSpan)),
    #                color = 'red'
    #                )
