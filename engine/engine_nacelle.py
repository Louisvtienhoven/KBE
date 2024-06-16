# -*- coding: utf-8 -*-

from parapy.geom import *
from parapy.core import *
from utilities.ref_frame import Frame


class Nacelle(ThickShell):
    length = Input(3.0)  # m
    fan_diameter = Input(2.0)  # m
    thickness = Input(0.01)  # m

    @Input
    def max_diameter(self):
        """
        Determine the max diameter of the nacelle based on the diameter of the fan
        :return: float
        """
        return self.fan_diameter * 1.1

    @Input
    def max_diameter_position(self):
        """
        Determine the position of the maximum diameter of the nacelle
        :return: float
        """
        return self.length * 0.2  # at 20% of total length

    @Part
    def nacelle_frame(self):
        """
        Model the reference frame of the nacelle
        :return: GeomBase.Frame
        """
        return Frame(
            pos=self.position
        )  # this helps visualizing the wing local reference frame

    @Part
    def crv_intake(self):
        """
        Create a circle representing the intake of the nacelle
        :return: GeomBase.Circle
        """
        return Circle(radius=self.fan_diameter / 2, position=self.position)

    @Part
    def crv_max_diameter(self):
        """
        Create a circle representing the maximum diameter of the nacelle
        :return: GeomBase.Circle
        """
        return Circle(
            radius=self.max_diameter / 2,
            position=self.position.translate("z", self.max_diameter_position),
        )

    @Part
    def crv_outlet(self):
        """
        Create a circle representing the outlet of the nacelle
        :return: GeomBase.Circle
        """
        return Circle(
            radius=self.fan_diameter * 0.9 / 2,
            position=self.position.translate("z", self.length),
        )

    @Part
    def srf_nacelle(self):
        """
        Model the nacelle as a lofted shell
        :return: GeomBase.LoftedShell
        """
        return LoftedShell(
            profiles=[self.crv_intake, self.crv_max_diameter, self.crv_outlet]
        )

    @Attribute
    def built_from(self):
        return self.srf_nacelle

    @Attribute
    def offset(self):
        return self.thickness


if __name__ == "__main__":
    from parapy.gui import display

    obj = Nacelle()
    display(obj)
