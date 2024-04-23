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
from engine.engine_pylon import Pylon
from utilities.ref_frame import Frame



class Engine(GeomBase):
    length = Input(3.0)
    fan_diameter = Input(2.0)

    @Part
    def nacelle(self):
        return Nacelle(length=self.length,
                       fan_diameter=self.fan_diameter,
                       transparency=0.6)

    @Part
    def shaft(self):
        return EngineShaft(shaft_length = self.length * 0.9)

    @Part
    def blank_pylon(self):
        return Pylon(pass_down="length, fan_diameter")


if __name__ == '__main__':
    from parapy.gui import display
    obj = Engine()
    display(obj)