from parapy.geom import *
from parapy.core import *
from math import *

from parapy.geom import *
from parapy.core import *
from math import *


class ChannelBase(LoftedSolid):
    """Base class for channel geometries, representing a loft through circles."""

    ch_radius = Input(0.1)
    ch_sections = Input([100] * 7)
    ch_length = Input(2.0)
    transparency = 0.6

    axis = "x"  # Default axis, should be overridden in derived classes

    @Attribute
    def section_radius(self):
        """Section radius multiplied by the radius distribution through the length."""
        return [i * self.ch_radius / 100.0 for i in self.ch_sections]

    @Attribute
    def section_length(self):
        """Section length is determined by dividing the fuselage length by the number of fuselage sections."""
        return self.ch_length / (len(self.ch_sections) - 1)

    @Attribute
    def rotation_axis(self):
        """Rotation axis for the channel profile, to be defined in derived classes."""
        raise NotImplementedError("Derived class must define rotation_axis")

    @Attribute
    def translation_vector(self):
        """Translation vector for the channel profile, to be defined in derived classes."""
        raise NotImplementedError("Derived class must define translation_vector")

    @Part(in_tree=(__name__ == "__main__"))
    def profiles(self):
        return Circle(
            quantify=len(self.ch_sections),
            color="Black",
            radius=self.section_radius[child.index],
            position=translate(
                self.position.rotate90(self.rotation_axis),
                self.translation_vector,
                child.index * self.section_length,
            ),
        )


class ChannelX(ChannelBase):
    """
    Standard definition of a channel aligned with the x-axis
    """
    axis = "x"
    ch_length = Input(31.5)

    @Attribute
    def rotation_axis(self):
        return "y"

    @Attribute
    def translation_vector(self):
        return Vector(1, 0, 0)


class ChannelY(ChannelBase):
    """
    Standard definition of a channel aligned with the y-axis
    """
    axis = "y"

    @Attribute
    def rotation_axis(self):
        return "x"

    @Attribute
    def translation_vector(self):
        return Vector(0, 1, 0)


if __name__ == "__main__":
    from parapy.gui import display

    obj = ChannelVtail()
    display(obj)
