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
from utilities.ref_frame import Frame
import numpy as np
from engine.engine_stages import EngineStage

class EngineShaft(GeomBase):
    nStages = Input(5)
    shaftLength = Input(3.0) # m

    stagesOuterDiameters = Input([2.0, 0.8, 0.6, 1.0, 1.2])
    stagesHubDiameters = Input([0.5, 0.6, 0.4, 0.5, 0.5])
    stagesStartPoint = Input([0, 0.2, 0.4, 0.7, 0.8])

    rotorsPerStage = Input([1, 3, 7, 2, 7])
    bladesPerRotor = Input([18, 100, 100, 100, 100])

    transparency = Input(0.7)

    @Attribute
    def stagesThickness(self):
        return list(np.diff(np.append(self.stagesStartPoint, 1)) * self.shaftLength)

    @Part
    def shaftFrame(self):
        return Frame(pos=self.position)

    @Part
    def centerShaft(self):
        return Cylinder(radius=min(self.stagesHubDiameters) / 2, height=self.shaftLength, centered=False)

    @Part
    def outerStageDisks(self):
        return Cylinder(quantify=self.nStages,
                        radius=self.stagesOuterDiameters[child.index] / 2,
                        position=translate(self.position, 'z', self.stagesStartPoint[child.index] * self.shaftLength),
                        height=self.stagesThickness[child.index],
                        hidden=True)

    @Part
    def innerStageDisks(self):
        return Cylinder(quantify=self.nStages,
                        radius=self.stagesHubDiameters[child.index] / 2,
                        position=translate(self.position, 'z', self.stagesStartPoint[child.index] * self.shaftLength),
                        height=self.stagesThickness[child.index],
                        hidden=True)

    @Part
    def stagesDisks(self):
        return SubtractedSolid(quantify=self.nStages,
                               shape_in = self.outerStageDisks[child.index],
                               tool = self.innerStageDisks[child.index],
                               color = 'red',
                               transparency=self.transparency)

    @Part
    def stages(self):
        return EngineStage(quantify=self.nStages,
                           position=translate(self.position, 'z',
                                              self.stagesStartPoint[child.index] * self.shaftLength),
                           map_down="stagesHubDiameters->hubDiameter,\
                            stagesOuterDiameters->outerDiameter,\
                            stagesThickness->stageThickness,\
                            rotorsPerStage->nRotors, \
                            bladesPerRotor->nBladesPerRotor")



if __name__ == '__main__':
    from parapy.gui import display
    obj = EngineShaft()
    display(obj)