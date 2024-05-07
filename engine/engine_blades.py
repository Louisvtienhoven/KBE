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
from math import *
import numpy as np


class EngineStageRotor(GeomBase):
    nBlades = Input(18)
    bladeSpan = Input(5)
    bladeDepth = Input(5)
    rotorDiameter = Input(10)
    hubDiameter = Input(2)

    @Attribute
    def bladeBoxWidth(self):
        outer_circum = pi * np.array(self.rotorDiameter)
        return outer_circum / np.array(self.nBlades)

    @Attribute
    def angularSeparation(self):
        return 2 * pi / np.array(self.nBlades)  # rad

    @Part
    def blades(self):
        return Box(
            quantify=self.nBlades,
            width=self.bladeSpan,
            height=self.bladeDepth,
            length=self.bladeBoxWidth,
            position=translate(
                rotate(self.position, "z", angle=child.index * self.angularSeparation),
                "x",
                self.hubDiameter / 2,
            ),
            hidden=True,
        )


if __name__ == "__main__":
    from parapy.gui import display

    obj = EngineStageRotor()
    display(obj)
