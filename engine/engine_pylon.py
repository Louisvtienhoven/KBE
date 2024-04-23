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
from engine_nacelle import Nacelle
from engine_shaft import EngineShaft
from utilities.ref_frame import Frame
from math import *

class Pylon(GeomBase):
    fan_diameter = Input(1.)
    length = Input(1.)

    @Attribute
    def pylon_height(self):
        return 1.5 * (self.fan_diameter/2)

    @Part
    def pylon_engine_mount(self):
        return Rectangle(position=rotate90(translate(self.position, 'z', self.length*1.2 / 2), 'x'),
                         width=0.1 * self.fan_diameter,
                         length=self.length,
                         centered=True)


    @Part
    def pylon_wing_mount(self):
        return Rectangle(position=rotate90(translate(self.position, 'y', self.pylon_height, 'z', self.length*1.2), 'x'),
                         width=0.1 * self.fan_diameter,
                         length=self.length,
                         centered=True)


    @Part
    def pylon(self):
        return RuledSolid(profile1=self.pylon_engine_mount,
                          profile2=self.pylon_wing_mount,
                          color='black')

if __name__ == '__main__':
    from parapy.gui import display
    obj = Pylon()
    display(obj)