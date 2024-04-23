#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2016 ParaPy Holding B.V.
#
# This file is subject to the terms and conditions defined in
# the license agreement that you have received with this source code
#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY
# KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS FOR A PARTICULAR
# PURPOSE.

from parapy.geom import *
from parapy.core import *


class Fuselage(LoftedSolid):  # note the use of LoftedSolid as superclass. It means that every Fuselage instance /
    # can generated lofts. A required input for LoftedSolid is a list of profiles, thereby either /
    # an @Attribute or a @Part sequence called "profiles" must be present in the body of the class. /
    # Use 'Display node' in the root node of the object tree to visualise the (yellow) loft in the GUI graphical viewer

    """Fuselage geometry, a loft through circles."""

    #: fuselage radius
    #: :type: float
    fu_radius = Input(2.5)
    #: fuselage sections
    #: :type: collections.Sequence[float]
    fu_sections = Input([10, 90, 100, 100, 100, 100, 100, 100, 100, 90, 10])
    #: fuselage length
    #: :type: float
    fu_length = Input(42.)

    @Attribute
    def section_radius(self):
        """section radius multiplied by the radius distribution
        through the length. Note that the numbers are percentages.

        :rtype: collections.Sequence[float]
        """
        return [i * self.fu_radius / 100. for i in self.fu_sections]

    @Attribute
    def section_length(self):
        """section length is determined by dividing the fuselage
        length by the number of fuselage sections.

        :rtype: float
        """
        return self.fu_length / (len(self.fu_sections) - 1)

    @Part(in_tree=(__name__ == '__main__'))
    def profiles(self):
        return Circle(quantify=len(self.fu_sections), color="Black",
                      radius=self.section_radius[child.index],
                      # fuselage along the X axis, nose in XOY
                      position=translate(self.position.rotate90('y'),  # circles are in XY plane, thus need rotation
                                         Vector(1, 0, 0),
                                         child.index * self.section_length)
                      )


if __name__ == '__main__':
    from parapy.gui import display
    obj = Fuselage(label="fuselage", mesh_deflection=0.0001)
    display(obj)
