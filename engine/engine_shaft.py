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
from math import *
from engine_stage import EngineStage

class EngineShaft(GeomBase):
    n_stages = Input(5)
    shaft_length = Input(3.0) # m
    stage_outer_diameters = Input([2.0, 0.8, 0.6, 1.0, 1.2])
    stage_hub_diameters = Input([0.5, 0.6, 0.4, 0.5, 0.5])
    stages_start_point = Input([0, 0.2, 0.4, 0.7, 0.8])

    @Attribute
    def stages_heights(self):
        return list(np.diff(np.append(self.stages_start_point, 1)))

    @Attribute
    def stages_blade_height(self):
        return self.stage_outer_diameters - self.stage_hub_diameters

    @Part
    def shaft_frame(self):
        return Frame(pos=self.position)

    @Part
    def center_shaft(self):
        return Cylinder(radius=min(self.stages_hub_diameters)/2, height=self.shaft_length, centered=False)

    @Part
    def outer_stage_disks(self):
        return Cylinder(quantify=self.n_stages,
                        radius=self.stage_outer_diameters[child.index] / 2,
                        position=translate(self.position, 'z', self.stages_start_point[child.index] * self.shaft_length),
                        height=self.stages_heights[child.index] * self.shaft_length,
                        color='blue',
                        transparency=0.8,
                        hidden=True)

    @Part
    def inner_stage_disks(self):
        return Cylinder(quantify=self.n_stages,
                        radius=self.stage_hub_diameters[child.index] / 2,
                        position=translate(self.position, 'z', self.stages_start_point[child.index] * self.shaft_length),
                        height=self.stages_heights[child.index] * self.shaft_length,
                        color='red',
                        transparency=0.8,
                        hidden=True)

    @Part
    def stages_layout(self):
        return SubtractedSolid(quantify=self.n_stages,
                               shape_in = self.outer_stage_disks[child.index],
                               tool = self.inner_stage_disks[child.index],
                               color = 'red',
                               transparency=0.8)

if __name__ == '__main__':
    from parapy.gui import display
    obj = EngineShaft()
    display(obj)