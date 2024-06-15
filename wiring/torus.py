from parapy.geom import *
from parapy.core import *
from math import *


class ChannelTor(GeomBase):
    lower_channel1 = Input()
    lower_channel2 = Input()

    upper_channels = Input([])

    @Input
    def angle1(self):
        dz = abs(self.position.z - self.lower_channel1.position.z)
        dy = abs(self.position.y - self.lower_channel1.position.y)

        return atan2(dy, dz)

    @Input
    def angle2(self):
        dz = abs(self.position.z - self.lower_channel2.position.z)
        dy = abs(self.position.y - self.lower_channel2.position.y)

        return atan2(dy, dz)

    @Attribute
    def major_radius(self):
        if len(self.upper_channels) == 1:
            # one channel in ceiling
            radius = sqrt(
                (self.upper_channels[0].position.z - self.position.z) ** 2
                + (self.upper_channels[0].position.y - self.position.y) ** 2
            )

        else:
            # two channels in ceiling
            z = max(
                [self.upper_channels[0].position.z, self.upper_channels[1].position.z]
            )
            y = max(
                [self.upper_channels[0].position.y, self.upper_channels[1].position.y]
            )
            radius = sqrt((self.position.z - z) ** 2 + (self.position.y - y) ** 2)

            def angle(channel):
                dz = abs(self.position.z - channel.position.z)
                dy = abs(self.position.y - channel.position.y)

                return atan2(dy, dz)

            self.angle1 = angle(self.upper_channels[0])
            self.angle2 = angle(self.upper_channels[1])

        return radius

    @Part
    def torus(self):
        return Torus(
            position=rotate(rotate90(self.position, "y"), "z", self.angle1),
            major_radius=self.major_radius,
            minor_radius=0.05,
            color="Blue",
            angle=2 * pi - (self.angle1 + self.angle2),
        )


if __name__ == "__main__":
    from parapy.gui import display

    obj = ChannelTor()
    display(obj)
