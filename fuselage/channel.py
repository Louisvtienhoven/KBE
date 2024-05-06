from parapy.geom import *
from parapy.core import *
from math import *


class ChannelX(
    LoftedSolid
):  # note the use of LoftedSolid as superclass. It means that every Fuselage instance /
    # can generated lofts. A required input for LoftedSolid is a list of profiles, thereby either /
    # an @Attribute or a @Part sequence called "profiles" must be present in the body of the class. /
    # Use 'Display node' in the root node of the object tree to visualise the (yellow) loft in the GUI graphical viewer

    """Fuselage geometry, a loft through circles."""

    #: fuselage radius
    #: :type: float
    transparency = 0.6
    ch_radius = Input(0.1)
    #: fuselage sections
    #: :type: collections.Sequence[float]
    ch_sections = Input(
        [
            100,
            100,
            100,
            100,
            100,
            100,
            100,
        ]
    )
    #: fuselage length
    #: :type: float
    ch_length = Input(32)

    direction = Input(True)

    # #positioning
    # ch_position_x = Input(1)
    # ch_position_y = Input(0)
    # ch_position_z = Input(0)
    @Attribute
    def yz_position(self):
        return self.position[1], self.position[2]

    @Attribute
    def section_radius(self):
        """section radius multiplied by the radius distribution
        through the length. Note that the numbers are percentages.

        :rtype: collections.Sequence[float]
        """
        return [i * self.ch_radius / 100.0 for i in self.ch_sections]

    @Attribute
    def section_length(self):
        """section length is determined by dividing the fuselage
        length by the number of fuselage sections.

        :rtype: float
        """
        return self.ch_length / (len(self.ch_sections) - 1)

    @Part(in_tree=(__name__ == "__main__"))
    def profiles(self):
        return Circle(
            quantify=len(self.ch_sections),
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


class ChannelY(
    LoftedSolid
):  # note the use of LoftedSolid as superclass. It means that every Fuselage instance /
    # can generated lofts. A required input for LoftedSolid is a list of profiles, thereby either /
    # an @Attribute or a @Part sequence called "profiles" must be present in the body of the class. /
    # Use 'Display node' in the root node of the object tree to visualise the (yellow) loft in the GUI graphical viewer

    """Fuselage geometry, a loft through circles."""

    #: fuselage radius
    #: :type: float
    transparency = 0.6
    ch_radius = Input(0.1)
    #: fuselage sections
    #: :type: collections.Sequence[float]
    ch_sections = Input(
        [
            100,
            100,
            100,
            100,
            100,
            100,
            100,
        ]
    )
    #: fuselage length
    #: :type: float
    ch_length = Input(2)

    # #positioning
    # ch_position_x = Input(1)
    # ch_position_y = Input(0)
    # ch_position_z = Input(0)
    @Attribute
    def section_radius(self):
        """section radius multiplied by the radius distribution
        through the length. Note that the numbers are percentages.

        :rtype: collections.Sequence[float]
        """
        return [i * self.ch_radius / 100.0 for i in self.ch_sections]

    @Attribute
    def section_length(self):
        """section length is determined by dividing the fuselage
        length by the number of fuselage sections.

        :rtype: float
        """
        return self.ch_length / (len(self.ch_sections) - 1)

    @Part(in_tree=(__name__ == "__main__"))
    def profiles(self):
        return Circle(
            quantify=len(self.ch_sections),
            color="Black",
            radius=self.section_radius[child.index],
            # fuselage along the X axis, nose in XOY
            position=translate(
                self.position.rotate90(
                    "x"
                ),  # circles are in XY plane, thus need rotation
                Vector(0, 1, 0),
                child.index * self.section_length,
            ),
        )


class ChannelZ(
    LoftedSolid
):  # note the use of LoftedSolid as superclass. It means that every Fuselage instance /
    # can generated lofts. A required input for LoftedSolid is a list of profiles, thereby either /
    # an @Attribute or a @Part sequence called "profiles" must be present in the body of the class. /
    # Use 'Display node' in the root node of the object tree to visualise the (yellow) loft in the GUI graphical viewer

    """Fuselage geometry, a loft through circles."""

    #: fuselage radius
    #: :type: float
    ch_radius = Input(0.1)
    #: fuselage sections
    #: :type: collections.Sequence[float]
    ch_sections = Input(
        [
            100,
            100,
            100,
            100,
            100,
            100,
            100,
        ]
    )
    #: fuselage length
    #: :type: float
    ch_length = Input(2.0)
    transparency = 0.6

    # #positioning
    # ch_position_x = Input(1)
    # ch_position_y = Input(0)
    # ch_position_z = Input(0)
    @Attribute
    def section_radius(self):
        """section radius multiplied by the radius distribution
        through the length. Note that the numbers are percentages.

        :rtype: collections.Sequence[float]
        """
        return [i * self.ch_radius / 100.0 for i in self.ch_sections]

    @Attribute
    def section_length(self):
        """section length is determined by dividing the fuselage
        length by the number of fuselage sections.

        :rtype: float
        """
        return self.ch_length / (len(self.ch_sections) - 1)

    @Part(in_tree=(__name__ == "__main__"))
    def profiles(self):
        return Circle(
            quantify=len(self.ch_sections),
            color="Black",
            radius=self.section_radius[child.index],
            # fuselage along the X axis, nose in XOY
            position=translate(
                self.position.rotate90(
                    "z"
                ),  # circles are in XY plane, thus need rotation
                Vector(0, 0, 1),
                child.index * self.section_length,
            ),
        )


class ChannelSweep(
    LoftedShell
):  # note the use of LoftedSolid as superclass. It means that every Fuselage instance /
    # can generated lofts. A required input for LoftedSolid is a list of profiles, thereby either /
    # an @Attribute or a @Part sequence called "profiles" must be present in the body of the class. /
    # Use 'Display node' in the root node of the object tree to visualise the (yellow) loft in the GUI graphical viewer

    """Fuselage geometry, a loft through circles."""

    #: fuselage radius
    #: :type: float
    ch_radius = Input(0.1)
    #: fuselage sections
    #: :type: collections.Sequence[float]
    ch_sections = Input(
        [
            100,
            100,
            100,
            100,
            100,
            100,
            100,
        ]
    )
    #: fuselage length
    #: :type: float
    ch_length = Input(12)

    # sweep_deg = 36.
    # sweep_rad = sweep_deg * (pi / 180)

    sweep_rad = Input(0.6283)
    dihedral = Input(0.06)

    # #positioning
    # ch_position_x = Input(1)
    # ch_position_y = Input(0)
    # ch_position_z = Input(0)
    @Attribute
    def section_radius(self):
        """section radius multiplied by the radius distribution
        through the length. Note that the numbers are percentages.

        :rtype: collections.Sequence[float]
        """
        return [i * self.ch_radius / 100.0 for i in self.ch_sections]

    @Attribute
    def section_length(self):
        """section length is determined by dividing the fuselage
        length by the number of fuselage sections.

        :rtype: float
        """
        return self.ch_length / (len(self.ch_sections) - 1)

    @Part(in_tree=(__name__ == "__main__"))
    def profiles(self):
        return Circle(
            quantify=len(self.ch_sections),
            color="Black",
            radius=self.section_radius[child.index],
            # fuselage along the X axis, nose in XOY
            position=translate(
                self.position.rotate90(
                    "y"
                ),  # circles are in XY plane, thus need rotation
                Vector(sin(self.sweep_rad), tan(self.sweep_rad), self.dihedral),
                child.index * self.section_length,
            ),
        )


class ChannelVtail(
    LoftedSolid
):  # note the use of LoftedSolid as superclass. It means that every Fuselage instance /
    # can generated lofts. A required input for LoftedSolid is a list of profiles, thereby either /
    # an @Attribute or a @Part sequence called "profiles" must be present in the body of the class. /
    # Use 'Display node' in the root node of the object tree to visualise the (yellow) loft in the GUI graphical viewer

    """Fuselage geometry, a loft through circles."""

    #: fuselage radius
    #: :type: float
    ch_radius = Input(0.1)
    #: fuselage sections
    #: :type: collections.Sequence[float]
    ch_sections = Input(
        [
            100,
            100,
            100,
            100,
            100,
            100,
            100,
        ]
    )
    #: fuselage length
    #: :type: float
    ch_length = Input(12)
    transparency = 0.6

    # sweep_deg = 36.
    # sweep_rad = sweep_deg * (pi / 180)

    sweep_rad = Input(0.6283)
    dihedral = Input(0.06)

    # #positioning
    # ch_position_x = Input(1)
    # ch_position_y = Input(0)
    # ch_position_z = Input(0)
    @Attribute
    def section_radius(self):
        """section radius multiplied by the radius distribution
        through the length. Note that the numbers are percentages.

        :rtype: collections.Sequence[float]
        """
        return [i * self.ch_radius / 100.0 for i in self.ch_sections]

    @Attribute
    def section_length(self):
        """section length is determined by dividing the fuselage
        length by the number of fuselage sections.

        :rtype: float
        """
        return self.ch_length / (len(self.ch_sections) - 1)

    @Part(in_tree=(__name__ == "__main__"))
    def profiles(self):
        return Circle(
            quantify=len(self.ch_sections),
            color="Black",
            radius=self.section_radius[child.index],
            # fuselage along the X axis, nose in XOY
            position=translate(
                self.position.rotate90(
                    "x"
                ),  # circles are in XY plane, thus need rotation
                Vector(sin(self.sweep_rad), 0, tan(self.sweep_rad)),
                child.index * self.section_length,
            ),
        )


if __name__ == "__main__":
    from parapy.gui import display

    obj = ChannelVtail()
    display(obj)
