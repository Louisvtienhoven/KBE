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
    def rotors(self):
        return EngineStageRotor(quantify=self.n_rotors,
                                position=translate(self.position, 'z', (self.blade_depths * 2) * child.index),
                                n_blades=self.n_blades_per_stage,
                                blade_height=self.blade_heights,
                                blade_depth=self.blade_depths,
                                stage_diameter=self.stage_outer_diameter,
                                hub_diameter=self.stage_hub_diameter)

if __name__ == '__main__':
    from parapy.gui import display
    obj = EngineStage()
    display(obj)