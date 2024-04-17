

from parapy.geom import *
from parapy.core import *


class Channel(LoftedSolid):  # note the use of LoftedSolid as superclass. It means that every Fuselage instance /
    # can generated lofts. A required input for LoftedSolid is a list of profiles, thereby either /
    # an @Attribute or a @Part sequence called "profiles" must be present in the body of the class. /
    # Use 'Display node' in the root node of the object tree to visualise the (yellow) loft in the GUI graphical viewer

    """Fuselage geometry, a loft through circles."""

    #: fuselage radius
    #: :type: float
    ch_radius = Input(0.1)
    #: fuselage sections
    #: :type: collections.Sequence[float]
    ch_sections = Input([100, 100, 100, 100, 100, 100, 100,])
    #: fuselage length
    #: :type: float
    ch_length = Input(25.2)

    #positioning
    ch_position_x = Input(1)
    ch_position_y = Input(0)
    ch_position_z = Input(0)
    @Attribute
    def section_radius(self):
        """section radius multiplied by the radius distribution
        through the length. Note that the numbers are percentages.

        :rtype: collections.Sequence[float]
        """
        return [i * self.ch_radius / 100. for i in self.ch_sections]

    @Attribute
    def section_length(self):
        """section length is determined by dividing the fuselage
        length by the number of fuselage sections.

        :rtype: float
        """
        return self.ch_length / (len(self.ch_sections) - 1)

    @Part(in_tree=(__name__ == '__main__'))
    def profiles(self):
        return Circle(quantify=len(self.ch_sections), color="Black",
                      radius=self.section_radius[child.index],
                      # fuselage along the X axis, nose in XOY
                      position=translate(self.position.rotate90('y'),  # circles are in XY plane, thus need rotation
                                         Vector(1, 0, 0),
                                         child.index * self.section_length)
                      )
