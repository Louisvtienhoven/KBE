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
from engine.engine_blades import EngineStageRotors
from utilities.ref_frame import Frame
from math import *
import numpy as np

class EngineStage(GeomBase):
    n_stages = Input(5)
    stage_outer_diameter = Input(2.0)
    stage_hub_diameter = Input(0.5)
    stage_depth = Input(0.2)
    n_rotors = Input(1)
    n_blades_per_stage = Input(18)

    @Attribute
    def blade_depths(self):
        return self.stage_depth / (self.n_rotors * 2)

    @Attribute
    def blade_heights(self):
        return (self.stage_outer_diameter - self.stage_hub_diameter) / 2

    @Part
    def blades(self):
        return EngineStageRotors(quantify=self.n_rotors,
                                 map_down="n_blades_per_stage->n_blades,\
                                 blade_heights->blade_height,\
                                 blade_depths->blade_depth,\
                                 stage_outer_diameter->stage_diameter,\
                                 stage_hub_diameter->hub_diameter")

if __name__ == '__main__':
    from parapy.gui import display
    obj = EngineStage()
    display(obj)