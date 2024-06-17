from parapy.geom import *
from parapy.core import *


class Fuselage(LoftedShell):  # """Fuselage geometry, a loft through circles."""
    # fuselage radius
    fu_radius = Input(3.95 / 2)

    #: fuselage sections
    fu_sections = Input([10, 80, 90, 95, 100, 100, 100, 100, 95, 80, 10])

    #: fuselage length
    fu_length = Input(44.51)

    #: transparency of the LoftedShell in the GUI
    transparency = Input(0.8)

    @Attribute
    def section_radius(self):
        """section radius multiplied by the radius distribution
        through the length. Note that the numbers are percentages.

        :rtype: collections.Sequence[float]
        """
        return [i * self.fu_radius / 100.0 for i in self.fu_sections]

    @Attribute
    def section_length(self):
        """section length is determined by dividing the fuselage
        length by the number of fuselage sections.

        :rtype: float
        """
        return self.fu_length / (len(self.fu_sections) - 1)

    @Part(in_tree=(__name__ == "__main__"))
    def profiles(self):
        """
        The sections of the fuselage modelled as circles
        :param self:
        :return: GeomBase.Circle
        """
        return Circle(
            quantify=len(self.fu_sections),
            color="Black",
            radius=self.section_radius[child.index],
            # fuselage along the X axis, nose in XOY
            position=translate(
                self.position.rotate90(
                    "y"
                ),  # circles are in XY plane, thus need rotation
                Vector(1, 0, 0),
                child.index * self.section_length,
            ),
        )


if __name__ == "__main__":
    from parapy.gui import display

    obj = Fuselage()
    display(obj)
