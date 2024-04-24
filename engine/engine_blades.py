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

class EngineStageRotor(GeomBase):
    n_blades = Input(18)
    blade_height = Input(5)
    blade_depth = Input(5)
    stage_diameter = Input(10)
    hub_diameter = Input(2)

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
                   width=self.blade_height,
                   height=self.blade_depth,
                   length=self.tip_chord,
                   position=translate(rotate(self.position,'z', angle=child.index * self.angular_separation),
                                      'x', self.hub_diameter /2
                   ),
                   hidden=True)


if __name__ == '__main__':
    from parapy.gui import display
    obj = EngineStageRotor()
    display(obj)
