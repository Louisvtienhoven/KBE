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

from parapy.geom import *
from parapy.core import *
from ref_frame import Frame

class Nacelle(ThickShell):
    length = Input(3.0)       # m
    fan_diameter = Input(2.0) # m
    bypass_ratio = Input(10.) # -
    thickness = Input(0.01)   # m

    @Attribute
    def max_diameter(self):
        return self.fan_diameter * 1.1

    @Attribute
    def max_diameter_position(self):
        return self.length * 0.2 # at 20% of total length

    @Part
    def nacelle_frame(self):
        return Frame(pos=self.position)  # this helps visualizing the wing local reference frame

    @Part
    def crv_intake(self):
        return Circle(radius=self.fan_diameter/2, position=self.position)

    @Part
    def crv_max_diameter(self):
        return Circle(radius=self.max_diameter/2, position=self.position.translate('z',self.max_diameter_position))

    @Part
    def crv_outlet(self):
        return Circle(radius=self.fan_diameter*0.9/2, position=self.position.translate('z',self.length))

    @Part
    def srf_nacelle(self):
        return LoftedShell(profiles=[self.crv_intake, self.crv_max_diameter, self.crv_outlet])

    @Part
    def shell_nacelle(self):
        return ThickShell(built_from=self.srf_nacelle, offset=self.thickness)

if __name__ == '__main__':
    from parapy.gui import display
    obj = Nacelle()
    display(obj)