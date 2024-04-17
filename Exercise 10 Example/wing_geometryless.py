# Copyright (C) 2016 ParaPy Holding B.V.
#
# This file is subject to the terms and conditions defined in
# the license agreement that you have received with this source code
#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY
# KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS FOR A PARTICULAR
# PURPOSE.


from parapy.core import Base, Input, Attribute


class Wing(Base):
    #: wing span
    b = Input(5.0)

    #: root chord
    c_root = Input(1.0)

    #: tip chord
    c_tip = Input(1.0)

    @Attribute
    def c_average(self):
        """Averages the root and tip chord"""
        return (self.c_root + self.c_tip) / 2.

    @Attribute
    def taper(self):
        """Calculates the taper by diving tip chord by root chord"""
        return self.c_tip / self.c_root

    @Attribute
    def area(self):
        """Calculates planform surface area by considering planform wing as
        a trapezoidal"""
        return (self.c_root + self.c_tip) * 0.5 * self.b

    @Attribute
    def ar(self):
        """Aspect ratio"""
        return self.b ** 2 / self.area


if __name__ == '__main__':
    from parapy.gui import display

    obj = Wing(b=10., c_root=3.0, c_tip=2.0,
               label="wing")
    display(obj)







