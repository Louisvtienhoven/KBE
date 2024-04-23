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

class EngineStageRotors(GeomBase):
    n_rotors = Input(3)

    n_blades = Input()
    blade_height = Input()
    blade_depth = Input()
    stage_diameter = Input()
    hub_diameter = Input()


    @Part
    def rotors(self):
        return EngineStageBlades(quantify = self.n_rotors,
                                 position=translate(self.position, 'z', self.blade_depth * 2))

class EngineStageBlades(EngineStageRotors):
    n_blades = Input()
    blade_height = Input()
    blade_depth = Input()
    stage_diameter = Input()
    hub_diameter = Input()

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
                   ))




if __name__ == '__main__':
    from parapy.gui import display
    obj = EngineStageBlades()
    display(obj)
