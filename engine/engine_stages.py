# -*- coding: utf-8 -*-
#
# Copyright (C) 2016-2023 ParaPy Holding B.V.
#
# You may use the contents of this file in your application code.
#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY
# KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS FOR A PARTICULAR
# PURPOSE.

"""
Model blades initially as ruled surfaces
"""

from parapy.geom import *
from parapy.core import *
from engine.engine_blades import EngineStageRotor
from utilities.ref_frame import Frame
from math import *
import numpy as np


class EngineStage(GeomBase):
    outerDiameter = Input(2.0)
    hubDiameter = Input(0.5)
    stageThickness = Input(0.2)
    nRotors = Input(1)
    nBladesPerRotor = Input(18)
    rotorIndex = Input(0)

    @Attribute
    def rotorThickness(self):
        return self.stageThickness / (self.nRotors * 2)

    @Attribute
    def bladeSpan(self):
        return (self.outerDiameter - self.hubDiameter) / 2

    @Attribute
    def fragmentSize(self):
        if self.rotorIndex != 0:
            fragmentSize = self.hubDiameter / 2 + self.bladeSpan / 3
        else:
            fragmentSize = self.bladeSpan
        return fragmentSize

    @Attribute
    def offAxisTranslation(self):
        if self.rotorIndex != 0:
            translation = 1 / 2 * self.fragmentSize
        else:
            translation = (
                self.fragmentSize * (2 / 3 - 1 / 2) + self.hubDiameter / 2
            ) * -1
        return translation

    @Attribute
    def riskVolumeSize(self):
        if self.rotorIndex != 0:
            riskVolumeSize = sqrt(3) * self.fragmentSize
        else:
            riskVolumeSize = self.fragmentSize
        return riskVolumeSize

    @Part
    def rotors(self):
        return EngineStageRotor(
            quantify=self.nRotors,
            position=translate(
                self.position, "z", (self.rotorThickness * 2) * child.index
            ),
            nBlades=self.nBladesPerRotor,
            bladeSpan=self.bladeSpan,
            bladeDepth=self.rotorThickness,
            rotorDiameter=self.outerDiameter,
            hubDiameter=self.hubDiameter,
        )


if __name__ == "__main__":
    from parapy.gui import display

    obj = EngineStage()
    display(obj)
