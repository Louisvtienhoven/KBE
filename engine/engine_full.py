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
    # the outer length of the engine
    length = Input(3.0)

    # the size of the fan, determining for size of the nacelle
    fanDiameter = Input(2.0)

    @Part
    def nacelle(self):
        """
        Create the nacelle around the shaft and engine stages
        :return: GeomBase.Nacelle object
        """
        return Nacelle(
            length=self.length, fan_diameter=self.fanDiameter, transparency=0.6
        )

    @Part
    def shaft(self):
        """
        Create the layout of all engine stages around a central shaft
        :return:
        """
        return EngineShaft(shaftLength=self.length * 0.9)


if __name__ == "__main__":
    from parapy.gui import display

    obj = Engine()
    display(obj)
