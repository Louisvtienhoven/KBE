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
    n_stages = Input(5)
    shaft_length = Input(3.0) # m

    stage_outer_diameters = Input([2.0, 0.8, 0.6, 1.0, 1.2])
    stage_hub_diameters = Input([0.5, 0.6, 0.4, 0.5, 0.5])
    stages_start_point = Input([0, 0.2, 0.4, 0.7, 0.8])

    rotors_per_stage = Input([1,3,7,2,7])
    blades_per_stage = Input([18,100,100,100,100])

    transparency = Input(0.7)

    @Attribute
    def stages_heights(self):
        return list(np.diff(np.append(self.stages_start_point, 1)) * self.shaft_length)

    @Part
    def shaft_frame(self):
        return Frame(pos=self.position)

    @Part
    def center_shaft(self):
        return Cylinder(radius=min(self.stage_hub_diameters)/2, height=self.shaft_length, centered=False)

    @Part
    def outer_stage_disks(self):
        return Cylinder(quantify=self.n_stages,
                        radius=self.stage_outer_diameters[child.index] / 2,
                        position=translate(self.position, 'z', self.stages_start_point[child.index] * self.shaft_length),
                        height=self.stages_heights[child.index],
                        hidden=True)

    @Part
    def inner_stage_disks(self):
        return Cylinder(quantify=self.n_stages,
                        radius=self.stage_hub_diameters[child.index] / 2,
                        position=translate(self.position, 'z', self.stages_start_point[child.index] * self.shaft_length),
                        height=self.stages_heights[child.index],
                        hidden=True)

    @Part
    def stages_disks(self):
        return SubtractedSolid(quantify=self.n_stages,
                               shape_in = self.outer_stage_disks[child.index],
                               tool = self.inner_stage_disks[child.index],
                               color = 'red',
                               transparency=self.transparency)

    @Part
    def stages(self):
        return EngineStage(quantify=self.n_stages,
                           position=translate(self.position, 'z',
                                              self.stages_start_point[child.index] * self.shaft_length),
                           map_down="blades_per_stage->n_blades_per_stage,\
                            stage_hub_diameters->stage_hub_diameter,\
                            stage_outer_diameters->stage_outer_diameter,\
                            stages_heights->stage_depth,\
                            rotors_per_stage->n_rotors")


if __name__ == '__main__':
    from parapy.gui import display
    obj = EngineShaft()
    display(obj)