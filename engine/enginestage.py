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

class EngineStage(GeomBase):
    n_blades = Input(10)
    hub_diameter = Input(0.2) # m
    outer_diameter = Input(2.0) # m
    hub_thickness = Input(0.2) # m

    @Attribute
    def tip_chord(self):
        outer_circum = pi * self.outer_diameter
        return outer_circum / self.n_blades

    @Attribute
    def root_chord(self):
        return self.hub_thickness

    @Attribute
    def angular_separation(self):
        return 2 * pi / self.n_blades # rad

    @Part
    def stage_frame(self):
        return Frame(position=self.position)

    @Part
    def blades(self):
        return Box(quantify=self.n_blades,
                   width=self.root_chord,
                   height=self.root_chord,
                   length=(self.outer_diameter - self.hub_diameter)/2,
                   position=rotate(self.position, 'z', child.index * self.angular_separation))

if __name__ == '__main__':
    from parapy.gui import display
    obj = EngineStage()
    display(obj)
