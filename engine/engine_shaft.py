# -*- coding: utf-8 -*-

from parapy.geom import *
from parapy.core import *
from utilities.ref_frame import Frame
import numpy as np
from engine.engine_stages import EngineStage


class EngineShaft(GeomBase):
    # the number of stages on the shaft, default is 5: fan, LP-comp, HP-comp, HP-turb, LP-turb
    nStages = Input(5)
    shaftLength = Input(3.0)  # m

    stages_outer_diameter = Input([2.0, 0.8, 0.6, 1.0, 1.2])
    stages_hub_diameter = Input([0.5, 0.6, 0.4, 0.5, 0.5])
    stages_start_point = Input([0, 0.2, 0.4, 0.7, 0.8])

    rotors_per_stage = Input([1, 3, 7, 2, 7])
    blades_per_rotor = Input([18, 100, 100, 100, 100])

    transparency = Input(0.7)

    @Attribute
    def stages_thickness(self):
        """
        Determine the thickness of the stages of the engine in axial direction
        :return: list containing the axial thickness of each engine stage
        """
        return list(np.diff(np.append(self.stages_start_point, 1)) * self.shaftLength)

    @Part
    def shaft_frame(self):
        """
        The reference system of the shaft assembly
        :return: sequency of GeomBase.LineSegment
        """
        return Frame(pos=self.position)

    @Part
    def center_shaft(self):
        return Cylinder(
            radius=min(self.stages_hub_diameter) / 2,
            height=self.shaftLength,
            centered=False,
        )

    @Part
    def outer_stage_disks(self):
        """
        Disks based on the outer dimensions of the stages of the engine
        :return: sequence of GeomBase.Cylinder
        """
        return Cylinder(
            quantify=self.nStages,
            radius=self.stages_outer_diameter[child.index] / 2,
            position=translate(
                self.position,
                "z",
                self.stages_start_point[child.index] * self.shaftLength,
            ),
            height=self.stages_thickness[child.index],
            hidden=True,
        )

    @Part
    def inner_stage_disks(self):
        """
        Disks based on the size of the hub of each stage of the engine
        :return: sequence of GeomBase.Cylinder
        """
        return Cylinder(
            quantify=self.nStages,
            radius=self.stages_hub_diameter[child.index] / 2,
            position=translate(
                self.position,
                "z",
                self.stages_start_point[child.index] * self.shaftLength,
            ),
            height=self.stages_thickness[child.index],
            hidden=True,
        )

    @Part
    def stages_disks(self):
        """
        The substracted solid of [outer_stage_disks] and [inner_stage_disks] to model the size of the rotor
        :return: GeomBase.SubtractedSolid
        """
        return SubtractedSolid(
            quantify=self.nStages,
            shape_in=self.outer_stage_disks[child.index],
            tool=self.inner_stage_disks[child.index],
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
                self.stages_start_point[child.index] * self.shaftLength,
            ),
            map_down="stages_hub_diameter->hubDiameter,\
                            stages_outer_diameter->outerDiameter,\
                            stages_thickness->stageThickness,\
                            rotors_per_stage->nRotors, \
                            blades_per_rotor->nBladesPerRotor",
            rotorIndex=child.index,
        )


if __name__ == "__main__":
    from parapy.gui import display

    obj = EngineShaft()
    display(obj)
