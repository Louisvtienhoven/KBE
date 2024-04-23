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

import os.path
from parapy.geom import *
from parapy.core import *
from tutorial_files.primiplane import AIRFOIL_DIR


class Airfoil(FittedCurve):  # note the use of FittedCurve as superclass
    chord = Input(1.)
    airfoil_name = Input("whitcomb")
    thickness_factor = Input(1.)
    mesh_deflection = Input(0.0001)
    tolerance = 0.0001

    @Attribute
    def points(self):  # required input to the FittedCurve superclass
        if self.airfoil_name.endswith('.dat'):  # check whether the airfoil name string includes .dat already
            airfoil_file = self.airfoil_name
        else:
            airfoil_file = self.airfoil_name + '.dat'
        file_path = os.path.join(AIRFOIL_DIR, airfoil_file)
        with open(file_path, 'r') as f:
            point_lst = []
            for line in f:
                x, z = line.split(' ', 1)  # the cartesian coordinates are directly interpreted as X and Z coordinates
                point_lst.append(self.position.translate(
                    "x", float(x) * self.chord,  # the x points are scaled according to the airfoil chord length
                    "z", float(z) * self.chord * self.thickness_factor))  # the y points are scaled according to the /
                # thickness factor
        return point_lst


if __name__ == '__main__':
    from parapy.gui import display

    obj = Airfoil(label="airfoil")
    display(obj)