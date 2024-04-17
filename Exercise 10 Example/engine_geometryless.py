from parapy.core import Base, Input, Attribute, Part
from math import pi


class Engine(Base):
    #: :type: float
    radius = Input(2)
    #: :type: float
    length = Input(2)

    @Attribute
    def volume(radius, length):
        """Consider engine shape as a cylinder
        :return: float
        """
        return pi * (radius ** 2) * length

    @Part
    def nacelle(self):
        return Nacelle()


class Nacelle(Base):
    """A nacelle"""

    @Attribute
    def volume(self):
        """
        :rtype: float
        """
        return 1.1


if __name__ == '__main__':
    from parapy.gui import display
    obj = Engine(radius = 10, length = 20, label="engine_and_nacelle")
    display(obj)