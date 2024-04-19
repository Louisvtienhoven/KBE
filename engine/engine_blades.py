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
from math import *
import numpy as np

class EngineStageBlades(GeomBase):
    n_blades = Input()
    blade_height = Input()
    blade_depth = Input()
    stage_diameter = Input()

    @Attribute
    def tip_chord(self):
        outer_circum = pi * np.array(self.stage_diameter)
        return outer_circum / np.array(self.n_blades)

    @Attribute
    def angular_separation(self):
        return 2 * pi / np.array(self.n_blades) # rad

    @Part
    def stage_frame(self):
        return Frame(pos=self.position)

    @Part
    def blades(self):
        return Box(quantify=self.n_blades,
                   width=self.tip_chord,
                   height=self.blade_depth,
                   length=self.blade_height,
                   position=rotate(self.position,'z', child.index * self.angular_separation)
                   )



if __name__ == '__main__':
    from parapy.gui import display
    obj = EngineStageBlades()
    display(obj)
