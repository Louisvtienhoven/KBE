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
    # the number of stages on the shaft, default is 5: fan, LP-comp, HP-comp, HP-turb, LP-turb
    nStages = Input(5)
    shaftLength = Input(3.0)  # m


    stagesOuterDiameters = Input([2.0, 0.8, 0.6, 1.0, 1.2])
    stagesHubDiameters = Input([0.5, 0.6, 0.4, 0.5, 0.5])
    stagesStartPoint = Input([0, 0.2, 0.4, 0.7, 0.8])

    rotorsPerStage = Input([1, 3, 7, 2, 7])
    bladesPerRotor = Input([18, 100, 100, 100, 100])

    transparency = Input(0.7)

    @Attribute
    def stages_thickness(self):
        """
        Determine the thickness of the stages of the engine in axial direction
        :return: list containing the axial thickness of each engine stage
        """
        return list(np.diff(np.append(self.stagesStartPoint, 1)) * self.shaftLength)

    @Part
    def shaft_frame(self):
        """
        The reference system of the shaft assembly
        :return: sequency of GeomBase.LineSegment
        """
        return Frame(pos=self.position)

    @Part
    def centerShaft(self):
        return Cylinder(
            radius=min(self.stagesHubDiameters) / 2,
            height=self.shaftLength,
            centered=False,
        )

    @Part
    def outerStageDisks(self):
        """
        Disks based on the outer dimensions of the stages of the engine
        :return: sequence of GeomBase.Cylinder
        """
        return Cylinder(
            quantify=self.nStages,
            radius=self.stagesOuterDiameters[child.index] / 2,
            position=translate(
                self.position,
                "z",
                self.stagesStartPoint[child.index] * self.shaftLength,
            ),
            height=self.stages_thickness[child.index],
            hidden=True,
        )

    @Part
    def innerStageDisks(self):
        """
        Disks based on the size of the hub of each stage of the engine
        :return: sequence of GeomBase.Cylinder
        """
        return Cylinder(
            quantify=self.nStages,
            radius=self.stagesHubDiameters[child.index] / 2,
            position=translate(
                self.position,
                "z",
                self.stagesStartPoint[child.index] * self.shaftLength,
            ),
            height=self.stages_thickness[child.index],
            hidden=True,
        )

    @Part
    def stagesDisks(self):
        """
        The substracted solid of [outer_stage_disks] and [inner_stage_disks] to model the size of the rotor
        :return: GeomBase.SubtractedSolid
        """
        return SubtractedSolid(
            quantify=self.nStages,
            shape_in=self.outerStageDisks[child.index],
            tool=self.innerStageDisks[child.index],
            color="red",
            transparency=self.transparency,
        )

    @Part
    def stages(self):
        """
        Model the stages of the engine with properties to determine the size of the corresponding risk volumes
        :return: EngineStage object
        """
        return EngineStage(
            quantify=self.nStages,
            position=translate(
                self.position,
                "z",
                self.stagesStartPoint[child.index] * self.shaftLength,
            ),
            map_down="stagesHubDiameters->hubDiameter,\
                            stagesOuterDiameters->outerDiameter,\
                            stagesThickness->stageThickness,\
                            rotorsPerStage->nRotors, \
                            bladesPerRotor->nBladesPerRotor",
            rotorIndex=child.index,
        )


if __name__ == "__main__":
    from parapy.gui import display

    obj = EngineShaft()
    display(obj)
