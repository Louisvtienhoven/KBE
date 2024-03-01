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

from parapy.core import Base, Input, Attribute, Part

from wing_geometryless import Wing
from fuselage_geometryless import Fuselage
from engine_geometryless import Engine


class Aircraft(Base):
    """Basic aircraft class example for demonstrative purposes of some core
    language features.
    """

    #: number of passengers
    #: :type: int
    npax = Input(200)

    #: fuselage radius
    #: :type: float
    f_radius = Input(3)

    #: fuselage length
    #: :type: float
    f_length = Input(60)

    #: engine radius
    #: :type: float
    e_radius = Input(1.5)

    #: engine length
    #: :type: float
    e_length = Input(2)

    #: number of engines
    #: :type: int
    n_of_engines = Input(4)

    #: Wing span
    #: :type: float
    span = Input(4)

    #: Wing root chord
    #: :type: float
    c_root = Input(4)

    #: Wing tip chord
    #: :type: float
    c_tip = Input(4)

    @Attribute
    def engines_volume(self):
        """The engines part is a sequence of engines: self.engines.volume
        will therefore not work. You must add an index to your call
        in order to extract a volume: self.engines[0].volume. In order to
        obtain all the volumes, you can use a for-loop or list comprehension
        to loop through each engine object of the sequence.

        :rtype: float
        """
        list_of_volumes = [engine.volume for engine in self.propulsion_sys]
        return sum(list_of_volumes)
        # return sum(list_of_volumes)

    @Attribute
    def volume(self):
        """Volume of the whole aircraft.
        :rtype: float
        """
        return self.fuselage.volume + self.engines_volume

    @Part
    def fuselage(self):
        return Fuselage(radius=self.f_radius,
                        length=self.f_length)

    @Part
    def propulsion_sys(self):
        return Engine(quantify=self.n_of_engines,
                      radius=self.e_radius,
                      length=self.e_length,
                      label="engine")

    @Part
    def wing(self):
        return Wing(b=self.span, c_root=self.c_root,
                    c_tip=self.c_tip,
                    label="main_wing")

# this below is a method. As such, it will not be visible in the property grid /
    # of parapy GUI. It will be treated as an internal function

    def lift(self, cl, v, rho):
        """Determines the lift of the wing

        :param float cl: lift coefficient
        :param float v: speed in m / s
        :param float rho: density in kg / m^3
        :param float area: planform area of the wing in m^2
        :rtype: float
        """
        return 0.5 * cl * rho * v **2 * self.wing.area


# when the module is run as the main program, the interpreter /
# kind of inserts this at the top of the module: __name__ = "__main__ /
# on the other hand, when a file is imported, it is like the interpreter puts
# on top of the imported file the following
# __name__ = "name_of_the importing_module"

if __name__ == '__main__':
    # Lift of wing at different lift coefficients
    cl_lst = [0.1, 0.3, 0.5]
    obj = Aircraft(npax=200,
                   f_radius=3, f_length=60,
                   e_radius=1.5, e_length=2, n_of_engines=4,
                   span=10.0, c_root=3, c_tip=2,
                   label="my_aircraft")  # Instantiate aircraft object
    for cl in cl_lst:
        print(obj.lift(cl, 120, 1.225))

    from parapy.gui import display
    display(obj)

