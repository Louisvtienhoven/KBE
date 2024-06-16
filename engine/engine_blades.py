# -*- coding: utf-8 -*-

from parapy.geom import *
from parapy.core import *
from math import *
import numpy as np


class EngineStageRotor(GeomBase):
    # Number of blades per rotor
    nBlades = Input(18)
    # the span of a blade
    bladeSpan = Input(5)
    # the depth of the blade measured in the axial direction of the engine
    bladeDepth = Input(5)
    # the outer diameter of the rotor
    rotorDiameter = Input(10)
    # the diameter of the hub connecting the blades to the shaft
    hubDiameter = Input(2)

    @Attribute
    def bladeBoxWidth(self):
        """
        Determine the dimension of the tip of the blade along the outer circumference of the rotor
        :return: float
        """
        outer_circum = pi * np.array(self.rotorDiameter)
        return outer_circum / np.array(self.nBlades)

    @Attribute
    def angularSeparation(self):
        """
        Determine the angular separation of the blades of the rotor
        :return: float
        """
        return 2 * pi / np.array(self.nBlades)  # rad

    @Part
    def blades(self):
        """
        Model the blades as boxes placed on the hub
        :return: GeomBase.Box
        """
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
