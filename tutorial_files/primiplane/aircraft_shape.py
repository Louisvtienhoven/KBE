from math import radians
from parapy.geom import *
from parapy.core import *
from tutorial_files.primiplane import Fuselage, Wing


class Aircraft(GeomBase):
    fu_radius = Input(2.5)
    fu_sections = Input([10, 90, 100, 100, 100, 100, 100, 100, 100, 90, 10])
    fu_length = Input(50.65)
    airfoil_root = Input("whitcomb")
    airfoil_tip = Input("simm_airfoil")
    w_c_root = Input(6.0)  # length of root chord, float
    w_c_tip = Input(2.3)  # length of tip chord, float
    t_factor_root = Input(
        1
    )  # to reduce/increase the thickness of the airfoil from the .dat file
    t_factor_tip = Input(1)
    w_semi_span = Input(27.0)
    sweep = Input(20)  # at leading edge, in degrees
    twist = Input(
        -5
    )  # tip airfoil twist angle, measured around leading edge, in degrees
    wing_dihedral = Input(3)
    wing_position_fraction_long = Input(
        0.4
    )  # longitudinal position w.r.t. fuselage length. (% of fus length)
    wing_position_fraction_vrt = Input(
        0.8
    )  # vertical position w.r.t. to fus  (% of fus radius)
    vt_long = Input(
        0.8
    )  # longitudinal position of the vertical tail, as % of fus length
    vt_taper = Input(0.4)

    @Part
    def fuselage(self):
        return Fuselage(
            pass_down="fu_radius, fu_sections, fu_length",
            color="Green",
            mesh_deflection=0.0001,
        )

    @Part
    def right_wing(self):
        return Wing(
            pass_down="airfoil_root, airfoil_tip, w_c_root, w_c_tip,"
            "t_factor_root, t_factor_tip, w_semi_span, "
            "sweep, twist",
            position=rotate(
                translate(  # longitudinal and vertically translation w.r.t. fuselage
                    self.position,
                    "x",
                    self.wing_position_fraction_long * self.fu_length,
                    "z",
                    self.wing_position_fraction_vrt * -self.fu_radius,
                ),
                "x",
                radians(self.wing_dihedral),
            ),
            # wing dihedral applied by rigid rotation
            mesh_deflection=0.0001,
            mov_start=self.wing_mov_start,
            #: spanwise position of inboard section, as % of lifting surface span
            mov_end=self.wing_mov_end,
            #: spanwise position of outboard section, as % of lifting surface span
            h_c_fraction=self.wing_h_c_fraction,  # hinge position, as % of chord
            s_c_fraction1=self.wing_s_c_fraction1,  # frontspar position, as % of chord
            s_c_fraction2=self.wing_s_c_fraction2,  # back spar position, as % of chord
        )

    @Part
    def left_wing(self):
        return MirroredShape(
            shape_in=self.right_wing,
            reference_point=self.position,
            # Two vectors to define the mirror plane
            vector1=self.position.Vz,
            vector2=self.position.Vx,
            mesh_deflection=0.0001,
        )


if __name__ == "__main__":
    from parapy.gui import display

    obj = Aircraft(label="aircraft")
    display(obj)
