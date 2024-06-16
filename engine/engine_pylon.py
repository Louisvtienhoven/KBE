# -*- coding: utf-8 -*-

from parapy.geom import *
from parapy.core import *


class Pylon(LoftedSolid):
    fan_diameter = Input(2.0)
    length = Input(3.0)

    @Input
    def pylon_height(self):
        """
        The height of the pylon, measured from its mounting point to the shaft of the engine
        :return: float
        """
        return 1.5 * (self.fan_diameter / 2)

    @Attribute
    def profiles(self):
        """
        Create the profiles of the pylon between which a lofted solid can be made
        :return: sequence of GeomBase.Rectangle
        """
        return [self.pylon_engine_mount, self.pylon_wing_mount]

    @Part
    def pylon_engine_mount(self):
        """
        Define the mounting point of the pylon at the engine shaft as a rectangle
        :return: GeomBase.Rectangle
        """
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
        """
        Define the mounting point of the pylon to the wing or fuselage as a rectangle
        :return: GeomBase.Rectangle
        """
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
