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


class Pylon(LoftedSolid):
    fan_diameter = Input(2.0)
    length = Input(3.0)

    @Input
    def pylon_height(self):
        return 1.5 * (self.fan_diameter / 2)

    @Attribute
    def profiles(self):
        return [self.pylon_engine_mount, self.pylon_wing_mount]

    @Part
    def pylon_engine_mount(self):
        return Rectangle(
            position=rotate90(
                translate(self.position, "z", self.length * 1.2 / 2), "x"
            ),
            width=0.1 * self.fan_diameter,
            length=self.length,
            centered=True,
        )

    @Part
    def pylon_wing_mount(self):
        return Rectangle(
            position=rotate90(
                translate(
                    self.position, "y", self.pylon_height, "z", self.length * 1.6
                ),
                "x",
            ),
            width=0.1 * self.fan_diameter,
            length=self.length,
            centered=True,
        )

    @Part
    def pylon(self):
        return LoftedSolid(
            profiles=[self.pylon_engine_mount, self.pylon_wing_mount], color="black"
        )


if __name__ == "__main__":
    from parapy.gui import display

    obj = Pylon()
    display(obj)
