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

from math import radians, tan
from parapy.geom import *
from parapy.core import *
from ref_frame import Frame


class Aircraft (GeomBase):
    @Part
    def aircraft_frame(self):
        return Frame(pos=self.position)  # this helps visualizing the aircraft reference frame, /
        # which, in this case, is the same as the global reference frame XOY)

    @Part
    def right_wing(self):
        return Wing(position=translate(self.position, 'x', 25, 'y', 2, 'z', 0))  # the wing is defined in a different /
        # reference system than its parent aircraft


    @Part
    def left_wing(self):
        return MirroredShape(shape_in=self.right_wing,
                             reference_point=self.position,
                             # Two vectors to define the mirror plane
                             vector1=self.position.Vz,
                             vector2=self.position.Vx,
                             mesh_deflection=0.0001)

    @Part
    def fuselage(self):
        return Fuselage(position=translate(self.position, 'x'))


class Wing(LoftedSolid):
    """Basic wing geometry: a loft between root and tip airfoil"""
    w_c_root = Input(6.)  # wing root chord
    w_c_tip = Input(2.3)  # wing tip chord
    w_semi_span = Input(10.)  # wing semi-span
    sweep_TE = Input(20)  # sweep angle, in degrees. Defined at the wing trailing edge (TE)

    @Attribute
    def pts(self):
        """ Extract airfoil coordinates from a data file and create a list of 3D points"""
        with open('whitcomb.dat', 'r') as f:
            points = []
            for line in f:
                x, y = line.split(' ', 1)  # separator = " "; max number of split = 1
                # Convert the strings to numbers and make 3D points for the FittedCurve class
                points.append(Point(float(x), float(y)))
                # Note that the points are imported in the X-Y plane. A rotation below (line 79) could be avoided if
                # points were imported in the X-Z plane, e.g. points.append(Point(float(x), 0, float(y)))
        return points

    @Part
    def wing_frame(self):
        return Frame(pos=self.position)  # this helps visualizing the wing local reference frame

    @Part
    def airfoil_from_3D_points(self):  # this curve is on the X-Y plane, with TE = (1, 0, 0) and LE = (0, 0, 0)
        return FittedCurve(points=self.pts,
                           mesh_deflection=0.0001)

    @Part
    def crv1_repositioned(self):  # ***************THIS WON'T WORK!!! ************* a curve built from 3D points /
        # cannot be moved. It stays nailed to its 3D points!
        return FittedCurve(points=self.pts,
                           position=translate(rotate(XOY, 'x', 90, deg=True),
                                              'x', self.position.x - 1,
                                              'y', self.position.y,
                                              'z', self.position.z),
                           color="red")

    # TransformedCurve is making a carbon copy of the fitted curve, which can be moved (rotated and translated) /
    # from one position to another. /
    # In this case we want to position the fitted curve copy in the x-z plane of the wing reference system, with its /
    # TE in the origin (location) of this reference system. This requires a rotation and a few translations.
    @Part
    def root_section_unscaled(self):
        return TransformedCurve(
            curve_in=self.airfoil_from_3D_points,
            # the curve to be repositioned
            from_position=rotate(translate(XOY, 'x', 1), 'x', -90, deg=True),
            # Can be thought of as moving a frame to the position on the curve from which you want to move it. It will
            # now be at the trailing edge and with X-Z plane aligned with curve plane.
            to_position=self.position,  # The wing relative reference system
            hidden=False
        )

    @Part  # for the wing tip we use the same type of airfoil used for the wing root. We use again TransformedCurve
    def tip_section_unscaled(self):
        return TransformedCurve(
            curve_in=self.root_section_unscaled,
            # the curve to be repositioned
            from_position=self.root_section_unscaled.position,
            to_position=translate(self.root_section_unscaled.position,  # to_position, i.e. the wing tip section
                                  'y', self.w_semi_span,
                                  'x', self.w_semi_span * tan(radians(self.sweep_TE))
                                  ),  # the sweep is applied
            hidden=True
        )

    @Part
    def root_section(self):  # the ScaledCurve primitive allows scaling a given curve. Here it is used to scale /
        # the unit chord airfoil generated from the .dat file according to their actual chord length
        return ScaledCurve(
            curve_in=self.root_section_unscaled,
            reference_point=self.root_section_unscaled.start,  # this point (the curve TE in this case) / is kept fixed during scaling
            # Can also use "self.position.point" - This extracts the (x,y,z) origin of the wing class position.
            factor=self.w_c_root,  # uniform scaling
            mesh_deflection=0.0001
        )

    @Part
    def tip_section(self):
        return ScaledCurve(
            curve_in=self.tip_section_unscaled,
            reference_point=self.tip_section_unscaled.start,
            factor=self.w_c_tip
        )

    @Part
    def wing_loft_solid(self):  # generate a surface
        return LoftedSolid(
            profiles=[self.root_section, self.tip_section],
            mesh_deflection=0.0001
        )

    @Attribute
    def profiles(self):
        return [self.root_section, self.tip_section]

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

    obj = Aircraft(label="aircraft")
    display(obj)
