from parapy.core import Base, Input, Attribute, Part
from math import pi


class Fuselage(Base):
    #: :type: float
    radius = Input()

    #: :type: float
    length = Input()

    @Attribute
    def volume(self):
        """Consider fuselage shape as a cylinder
        :return: float
        """
        return pi * (self.radius**2) * self.length


if __name__ == "__main__":
    from parapy.gui import display

    obj = Fuselage(radius=30, length=200, label="fuselage")
    display(obj)
