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
    def rotor_thickness(self):
        """
        The axial dimension of a rotor element of an engine stage
        :return: float
        """
        return self.stageThickness / (self.nRotors * 2)

    @Attribute
    def blade_span(self):
        """
        Calculate the span of a blade element of a rotor
        :return:
        """
        return (self.outerDiameter - self.hubDiameter) / 2

    @Attribute
    def offAxisTranslation(self):
        """
        Determine the location of the loci of the c.g. of the risk volume per engine stage. This location affects
        the translation of the risk volume in an radial direction of the engine shaft.
        :return:
        """
        if self.rotorIndex != 0:
            # translation for third-rotor fragment
            translation = 1 / 2 * (self.hubDiameter / 2 + self.blade_span / 3)
        else:
            # translation for fan blade fragment
            translation = (
                                  self.blade_span * (2 / 3 - 1 / 2) + self.hubDiameter / 2
            ) * -1
        return translation

    @Attribute
    def risk_volume_size(self):
        """
        Determine the size of the risk volume in radial direction corresponding to CS25
        :return:
        """
        if self.rotorIndex != 0:
            # fan blade fragment
            fragment_size = self.hubDiameter / 2 + self.blade_span / 3
            riskVolumeSize = sqrt(3) * fragment_size
        else:
            # third-rotor fragment
            riskVolumeSize = self.blade_span
        return riskVolumeSize

    @Part
    def rotors(self):
        """
        Model the rotors of each engine stage
        :return: EngineStageRotor object
        """
        return EngineStageRotor(
            quantify=self.nRotors,
            position=translate(
                self.position, "z", (self.rotor_thickness * 2) * child.index
            ),
            nBlades=self.nBladesPerRotor,
            bladeSpan=self.blade_span,
            bladeDepth=self.rotor_thickness,
            rotorDiameter=self.outerDiameter,
            hubDiameter=self.hubDiameter,
        )


if __name__ == "__main__":
    from parapy.gui import display

    obj = EngineStage()
    display(obj)
