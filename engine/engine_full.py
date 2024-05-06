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
from engine.engine_nacelle import Nacelle
from engine.engine_shaft import EngineShaft


class Engine(GeomBase):
    length = Input(3.0)
    fanDiameter = Input(2.0)

    @Part
    def nacelle(self):
        return Nacelle(
            length=self.length, fan_diameter=self.fanDiameter, transparency=0.6
        )

    @Part
    def shaft(self):
        return EngineShaft(shaftLength=self.length * 0.9)


if __name__ == "__main__":
    from parapy.gui import display

    obj = Engine()
    display(obj)
