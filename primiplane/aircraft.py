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

import os
from math import radians
from parapy.geom import *
from parapy.core import *

from primiplane import Fuselage, LiftingSurface, XfoilAnalysis

DIR = os.path.dirname(__file__)


class Aircraft(GeomBase):
    fu_radius = Input(2.5)
    fu_sections = Input([10, 90, 100, 100, 100, 100, 100, 100, 100, 90, 10])
    fu_length = Input(50.65)

    airfoil_root = Input("whitcomb")
    airfoil_tip = Input("simm_airfoil")
    w_c_root = Input(6.)  # length of root chord, float
    w_c_tip = Input(2.3)  # length of tip chord, float
    t_factor_root = Input(1)  # to reduce/increase the thickness of the airfoil from the .dat file
    t_factor_tip = Input(1)

    w_semi_span = Input(27.)
    sweep = Input(20)  # at leading edge, in degrees
    twist = Input(-5)  # tip airfoil twist angle, measured around leading edge, in degrees

    wing_dihedral = Input(3)
    wing_position_fraction_long = Input(0.4)  # longitudinal position w.r.t. fuselage length. (% of fus length)
    wing_position_fraction_vrt = Input(0.8)  # vertical position w.r.t. to fus  (% of fus radius)

    vt_long = Input(0.8)  # longitudinal position of the vertical tail, as % of fus length
    vt_taper = Input(0.4)

    # XFOIL analysis input
    reynolds_number = Input(20000000)
    alpha = Input((-5, 25, 1))
    cutting_plane_span_fraction = Input(0.5)
    flydir = Input(True)

    # movables
    wing_mov_start = Input(0.7)  #: spanwise position of movable inboard section, as % of lifting surface span
    wing_mov_end = Input(0.95)  #: spanwise position of movable outboard section, as % of lifting surface span
    wing_h_c_fraction = Input(0.8)  # movable hing position, as % of chord
    wing_s_c_fraction1 = Input(0.85)  # movable frontspar position, as % of chord
    wing_s_c_fraction2 = Input(0.9)  # movable backspar position, as % of chord

    vert_tail_mov_start = Input(0.7)  #: spanwise position of movable inboard section, as % of lifting surface span
    vert_tail_mov_end = Input(0.95)  #: spanwise position of movable outboard section, as % of lifting surface span
    vert_tail_h_c_fraction = Input(0.8)  # movable hing position, as % of chord
    vert_tail_s_c_fraction1 = Input(0.85)  # movable frontspar position, as % of chord
    vert_tail_s_c_fraction2 = Input(0.9)  # movable backspar position, as % of chord

    h_tail_mov_start = Input(0.7)  #: spanwise position of movable inboard section, as % of lifting surface span
    h_tail_mov_end = Input(0.95)  #: spanwise position of movable outboard section, as % of lifting surface span
    h_tail_h_c_fraction = Input(0.8)  # movable hing position, as % of chord
    h_tail_s_c_fraction1 = Input(0.85)  # movable frontspar position, as % of chord
    h_tail_s_c_fraction2 = Input(0.9)  # movable backspar position, as % of chord

    @Part
    def fuselage(self):
        return Fuselage(pass_down="fu_radius, fu_sections, fu_length",
                        color="Green",
                        mesh_deflection=0.0001
                        )

    @Part
    def right_wing(self):
        return LiftingSurface(pass_down="airfoil_root, airfoil_tip, w_c_root, w_c_tip,"
                                        "t_factor_root, t_factor_tip, w_semi_span, "
                                        "sweep, twist",
                              position=rotate(translate  # longitudinal and vertically translation w.r.t. fuselage
                                              (self.position,
                                               "x", self.wing_position_fraction_long * self.fu_length,
                                               "z", self.wing_position_fraction_vrt * - self.fu_radius),
                                              "x", radians(self.wing_dihedral)),
                              # wing dihedral applied by rigid rotation
                              mesh_deflection=0.0001,
                              mov_start=self.wing_mov_start,
                              #: spanwise position of inboard section, as % of lifting surface span
                              mov_end=self.wing_mov_end,
                              #: spanwise position of outboard section, as % of lifting surface span
                              h_c_fraction=self.wing_h_c_fraction,  # hinge position, as % of chord
                              s_c_fraction1=self.wing_s_c_fraction1,  # frontspar position, as % of chord
                              s_c_fraction2=self.wing_s_c_fraction2  # back spar position, as % of chord
                              )

    @Part
    def left_wing(self):
        return MirroredShape(shape_in=self.right_wing,
                             reference_point=self.position,
                             # Two vectors to define the mirror plane
                             vector1=self.position.Vz,
                             vector2=self.position.Vx,
                             mesh_deflection=0.0001)

    @Part
    def vert_tail(self):
        return LiftingSurface(
            w_c_root=self.w_c_root,
            w_c_tip=self.w_c_root * self.vt_taper,
            airfoil_root="simm_airfoil",
            airfoil_tip="simm_airfoil",
            t_factor_root=0.9 * self.t_factor_root,
            t_factor_tip=0.9 * self.t_factor_tip,
            w_semi_span=self.w_semi_span / 3,
            sweep=45,
            twist=0,
            position=rotate(translate
                            (self.position,
                             "x", self.vt_long * self.fu_length,
                             "z", self.fu_radius * 0.7),
                            "x", radians(90)),
            mesh_deflection=0.0001,
            mov_start=self.vert_tail_mov_start,  #: spanwise position of inboard section, as % of lifting surface span
            mov_end=self.vert_tail_mov_end,  #: spanwise position of outboard section, as % of lifting surface span
            h_c_fraction=self.vert_tail_h_c_fraction,  # hinge position, as % of chord
            s_c_fraction1=self.vert_tail_s_c_fraction1,  # frontspar position, as % of chord
            s_c_fraction2=self.vert_tail_s_c_fraction2
        )

    @Part
    def h_tail_right(self):
        return LiftingSurface(w_c_root=self.w_c_root / 1.5,
                              w_c_tip=self.w_c_tip / 2,
                              airfoil_root="simm_airfoil",
                              airfoil_tip="simm_airfoil",
                              t_factor_root=0.9 * self.t_factor_root,
                              t_factor_tip=0.9 * self.t_factor_tip,
                              w_semi_span=self.w_semi_span / 2.5,
                              sweep=self.sweep + 10,
                              twist=0,
                              position=rotate(translate
                                              (self.position, "x", self.fu_length - self.w_c_root),
                                              "x", radians(self.wing_dihedral + 5)),
                              mesh_deflection=0.0001,
                              mov_start=self.h_tail_mov_start,
                              #: spanwise position of inboard section, as % of lifting surface span
                              mov_end=self.h_tail_mov_end,
                              #: spanwise position of outboard section, as % of lifting surface span
                              h_c_fraction=self.h_tail_h_c_fraction,  # hinge position, as % of chord
                              s_c_fraction1=self.h_tail_s_c_fraction1,  # frontspar position, as % of chord
                              s_c_fraction2=self.h_tail_s_c_fraction2
                              )

    @Part
    def h_tail_left(self):
        return MirroredShape(shape_in=self.h_tail_right,
                             reference_point=self.position,
                             # Two vectors to define the mirror plane
                             vector1=self.position.Vz,
                             vector2=self.position.Vx,
                             mesh_deflection=0.0001)

    @Part
    def xfoil_analysis(self):
        return XfoilAnalysis(lifting_surface=self.right_wing,
                             cutting_plane_span_fraction=self.cutting_plane_span_fraction,
                             flydir=self.flydir,
                             reynolds_number=self.reynolds_number,
                             alpha=self.alpha)
