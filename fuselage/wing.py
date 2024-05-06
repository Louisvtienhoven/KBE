from math import radians, tan
from parapy.geom import *
from parapy.core import *
from utilities.ref_frame import Frame


class Wing(LoftedSolid):
    """Basic wing geometry: a loft between root and tip airfoil"""

    w_c_root = Input(6.0)  # wing root chord
    w_c_tip = Input(2.3)  # wing tip chord
    w_semi_span = Input(10.0)  # wing semi-span
    sweep_TE = Input(
        25.0
    )  # sweep angle, in degrees. Defined at the wing trailing edge (TE)
    dihedral = Input(1.0)

    front_spar_chord_pos = Input(0.2)
    aft_spar_chord_pos = Input(0.75)

    @Attribute
    def pts(self):
        """Extract airfoil coordinates from a data file and create a list of 3D points"""
        if __name__ != "__main__":
            dir = "./fuselage/whitcomb.dat"

        else:
            dir = "./whitcomb.dat"

        with open(dir, "r") as f:
            points = []
            for line in f:
                x, y = line.split(" ", 1)  # separator = " "; max number of split = 1
                # Convert the strings to numbers and make 3D points for the FittedCurve class
                points.append(Point(float(x), float(y)))
                # Note that the points are imported in the X-Y plane. A rotation below (line 79) could be avoided if
                # points were imported in the X-Z plane, e.g. points.append(Point(float(x), 0, float(y)))
        return points

    @Part
    def wing_frame(self):
        return Frame(
            pos=self.position
        )  # this helps visualizing the wing local reference frame

    @Part
    def airfoil_from_3D_points(
        self,
    ):  # this curve is on the X-Y plane, with TE = (1, 0, 0) and LE = (0, 0, 0)
        return FittedCurve(points=self.pts, mesh_deflection=0.0001)

    @Part
    def crv1_repositioned(
        self,
    ):  # ***************THIS WON'T WORK!!! ************* a curve built from 3D points /
        # cannot be moved. It stays nailed to its 3D points!
        return FittedCurve(
            points=self.pts,
            position=translate(
                rotate(XOY, "x", 90, deg=True),
                "x",
                self.position.x - 1,
                "y",
                self.position.y,
                "z",
                self.position.z,
            ),
            color="red",
        )

    # TransformedCurve is making a carbon copy of the fitted curve, which can be moved (rotated and translated) /
    # from one position to another. /
    # In this case we want to position the fitted curve copy in the x-z plane of the wing reference system, with its /
    # TE in the origin (location) of this reference system. This requires a rotation and a few translations.
    @Part
    def root_section_unscaled(self):
        return TransformedCurve(
            curve_in=self.airfoil_from_3D_points,
            # the curve to be repositioned
            from_position=rotate(translate(XOY, "x", 1), "x", -90, deg=True),
            # Can be thought of as moving a frame to the position on the curve from which you want to move it. It will
            # now be at the trailing edge and with X-Z plane aligned with curve plane.
            to_position=self.position,  # The wing relative reference system
            hidden=False,
        )

    @Part  # for the wing tip we use the same type of airfoil used for the wing root. We use again TransformedCurve
    def tip_section_unscaled(self):
        return TransformedCurve(
            curve_in=self.root_section_unscaled,
            # the curve to be repositioned
            from_position=self.root_section_unscaled.position,
            to_position=translate(
                self.root_section_unscaled.position,  # to_position, i.e. the wing tip section
                "y",
                self.w_semi_span,
                "x",
                self.w_semi_span * tan(radians(self.sweep_TE)),
                "z",
                self.dihedral,
            ),  # the sweep is applied
            hidden=True,
        )

    @Part
    def root_section(
        self,
    ):  # the ScaledCurve primitive allows scaling a given curve. Here it is used to scale /
        # the unit chord airfoil generated from the .dat file according to their actual chord length
        return ScaledCurve(
            curve_in=self.root_section_unscaled,
            reference_point=self.root_section_unscaled.start,  # this point (the curve TE in this case) / is kept fixed during scaling
            # Can also use "self.position.point" - This extracts the (x,y,z) origin of the wing class position.
            factor=self.w_c_root,  # uniform scaling
            mesh_deflection=0.0001,
        )

    @Attribute
    def front_spar_root_location(self):
        return Position(
            translate(
                self.root_section_unscaled.start,
                "x",
                (1 - self.front_spar_chord_pos) * -self.w_c_root,
                "z",
                0.01 * self.w_c_root,
            )
        )

    @Attribute
    def aft_spar_root_location(self):
        return Position(
            translate(
                self.root_section.position,
                "x",
                (1 - self.aft_spar_chord_pos) * -self.w_c_root,
                "z",
                0.02 * self.w_c_root,
            )
        )

    @Attribute
    def front_spar_tip_location(self):
        return Position(
            translate(
                self.tip_section_unscaled.start,
                "x",
                (1 - self.front_spar_chord_pos) * -self.w_c_tip,
                "z",
                0.01 * self.w_c_tip,
            )
        )

    @Attribute
    def aft_spar_tip_location(self):
        return Position(
            translate(
                self.tip_section.position,
                "x",
                (1 - self.aft_spar_chord_pos) * -self.w_c_tip,
                "z",
                0.02 * self.w_c_tip,
            )
        )

    @Part
    def tip_section(self):
        return ScaledCurve(
            curve_in=self.tip_section_unscaled,
            reference_point=self.tip_section_unscaled.start,
            factor=self.w_c_tip,
        )

    @Part
    def wing_loft_solid(self):  # generate a surface
        return LoftedSolid(
            profiles=[self.root_section, self.tip_section], mesh_deflection=0.0001
        )

    @Attribute
    def profiles(self):
        return [self.root_section, self.tip_section]

    # @Attribute
    # def front_spar_plane_normal(self):
    #     return self.front_spar_tip_location - self.front_spar_root_location
    #
    # @Attribute
    # def aft_spar_plane_normal(self):
    #     return self.aft_spar_tip_location - self.aft_spar_root_location
    #
    # @Part
    # def front_spar(self):
    #     return LineSegment(start = self.front_spar_root_location.point, end = self.front_spar_tip_location.point)
    #
    # @Part
    # def aft_spar(self):
    #     return LineSegment(start = self.aft_spar_root_location.point, end = self.aft_spar_tip_location.point)
    #
    # @Part
    # def front_spar_channel(self):
    #     return PipeSolid(path=self.front_spar, radius=.07)
    #
    # @Part
    # def aft_spar_channel(self):
    #     return PipeSolid(path=self.aft_spar, radius=.07)


if __name__ == "__main__":
    from parapy.gui import display

    obj = Wing()
    display(obj)
