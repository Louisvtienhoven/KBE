from parapy.geom import *
from parapy.core import *

from wiring.channel_definitions import ChannelY, ChannelX
from wiring.torus import ChannelTor


class FuselageChannels(GeomBase):
    lower_channel_zposition = Input(-1)
    upper_channel_zposition = Input(1.2)
    channels_ypostion = Input(1.05)

    h_tail = Input()
    v_tail = Input()

    tail_config = Input()

    @Part
    def lower_channel(self):
        return ChannelX(
            ch_radius=0.2,
            position=translate(
                self.position,
                "x",
                5.5,
                "y",
                self.channels_ypostion,
                "z",
                self.lower_channel_zposition,
            ),
            color="Blue",
        )

    @Part
    def lower_channel2(self):
        return MirroredShape(
            shape_in=self.lower_channel,
            reference_point=self.position,
            # Two vectors to define the mirror plane
            vector1=self.position.Vz,
            vector2=self.position.Vx,
            mesh_deflection=0.0001,
            color="Blue",
        )

    @Part
    def connectorY1(self):
        return ChannelY(
            ch_length=self.channels_ypostion * 2,
            ch_radius=0.1,
            position=translate(
                self.position,
                "x",
                7,
                "y",
                -1 * self.channels_ypostion,
                "z",
                self.lower_channel_zposition,
            ),
            color="Blue",
        )



class ThreeChannels(FuselageChannels):
    @Part
    def fuselage_connector(self):
        return ChannelTor(
            position=translate(self.position, "x", 10, "y", 0, "z", -0.2),
            lower_channel1=self.lower_channel,
            lower_channel2=self.lower_channel2,
            upper_channels=[self.upper_channel],
        )

    @Part
    def fuselage_connector2(self):
        return ChannelTor(
            position=translate(self.position, "x", self.v_tail.front_spar_root_location.point.x, "y", 0, "z", -0.2),
            lower_channel1=self.lower_channel,
            lower_channel2=self.lower_channel2,
            upper_channels=[self.upper_channel],
        )

    @Part
    def upper_channel(self):
        return ChannelX(
            ch_radius=0.1,
            position=translate(
                self.position, "x", 7, "y", 0, "z", self.upper_channel_zposition
            ),
            color="Blue",
            ch_length=33.2,
        )

    @Attribute
    def crv_tail_connector(self):
        return Arc3P(
            point1=self.h_tail.aft_spar_root_location.point,
            point3=self.h_tail.aft_spar_root_location.point.mirror(
                ref=self.position, axis1=self.position.Vx, axis2=self.position.Vz
            ),
            point2=self.upper_channel.position.translate(
                "x", self.upper_channel.ch_length
            ).point,
        )

    @Part
    def tail_connector(self):
        return PipeSolid(path=self.crv_tail_connector, radius=0.07, hidden=self.tail_config)


class FourChannels(FuselageChannels):

    @Part
    def upper_channel(self):
        return ChannelX(
            ch_radius=0.07,
            position=translate(
                self.position,
                "x",
                8,
                "y",
                self.channels_ypostion,
                "z",
                self.upper_channel_zposition,
            ),
            color="Blue",
            ch_length=29,
        )

    @Part
    def upper_channel2(self):
        return MirroredShape(
            shape_in=self.upper_channel,
            reference_point=self.position,
            # Two vectors to define the mirror plane
            vector1=self.position.Vz,
            vector2=self.position.Vx,
            mesh_deflection=0.0001,
            color="Blue",
        )

    @Attribute
    def crv_fuselage_connector(self):
        return Arc2P(
            start=Point(
                0, self.upper_channel.position.y, self.upper_channel.position.z
            ),
            end=Point(
                0, self.upper_channel2.position.y, self.upper_channel2.position.z
            ),
            center=self.position.point,
        )

    @Attribute
    def crv_fuselage_connector2(self):
        return Arc2P(
            start=Point(
                0, self.lower_channel.position.y, self.lower_channel.position.z
            ),
            end=Point(0, self.upper_channel.position.y, self.upper_channel.position.z),
            center=translate(self.position, "z", 0.1),
        )

    @Part
    def fuselage_connector1(self):
        return PipeSolid(
            path=TranslatedCurve(
                curve_in=self.crv_fuselage_connector2, displacement=Vector(10, 0, 0)
            ),
            radius=0.05,
        )

    @Part
    def fuselage_connector2(self):
        return MirroredShape(
            shape_in=self.fuselage_connector1,
            reference_point=self.position,
            vector1=self.position.Vx,
            vector2=self.position.Vz,
        )

    @Part
    def fuselage_connector_ceiling1(self):
        return PipeSolid(
            path=TranslatedCurve(
                curve_in=self.crv_fuselage_connector, displacement=Vector(10, 0, 0)
            ),
            radius=0.05,
        )

    @Part
    def fuselage_connector3(self):
        return PipeSolid(
            path=TranslatedCurve(
                curve_in=self.crv_fuselage_connector2,
                displacement=Vector(self.v_tail.front_spar_root_location.point.x-5, 0, 0)
            ),
            radius=0.05,
        )

    @Part
    def fuselage_connector4(self):
        return MirroredShape(
            shape_in=self.fuselage_connector3,
            reference_point=self.position,
            vector1=self.position.Vx,
            vector2=self.position.Vz,
        )

    @Part
    def fuselage_connector_ceiling2(self):
        return PipeSolid(
            path=TranslatedCurve(
                curve_in=self.crv_fuselage_connector,
                displacement=Vector(self.v_tail.front_spar_root_location.point.x-5, 0, 0)
            ),
            radius=0.05,
        )

    @Attribute
    def crv_tail_connector(self):
        return Arc3P(
            point1=self.h_tail.aft_spar_root_location.point,
            point3=self.h_tail.aft_spar_root_location.point.mirror(
                ref=self.position, axis1=self.position.Vx, axis2=self.position.Vz
            ),
            point2=self.v_tail.aft_spar_root_location.point,
        )

    @Part
    def tail_connector(self):
        return PipeSolid(path=self.crv_tail_connector, radius=0.07, hidden=self.tail_config)

    @Attribute
    def crv_vtail_connector(self):
        point1 = Point(x=self.v_tail.front_spar_root_location.point.x,
                       y=self.upper_channel.position.y,
                       z=self.upper_channel.position.z)

        point2 = Point(x=self.v_tail.front_spar_root_location.point.x,
                       y=self.upper_channel2.position.y,
                       z=self.upper_channel2.position.z)

        return LineSegment(start=point2, end=point1)

    @Part
    def vtail_connector(self):
        return PipeSolid(path=self.crv_vtail_connector, radius=0.07)

    @Attribute
    def crv_vtail_connector_top(self):
        point1 = self.v_tail.aft_spar_root_location
        point2 = translate(self.upper_channel.position, 'x', self.upper_channel.ch_length)
        return LineSegment(start=point1, end=point2)

    @Part
    def vtail_connector_top1(self):
        return PipeSolid(path=self.crv_vtail_connector_top, radius=0.07)

    @Part
    def vtail_connector_top2(self):
        return MirroredShape(shape_in=self.vtail_connector_top1,
                             reference_point=self.position,
                             vector1=self.position.Vx,
                             vector2=self.position.Vz,
                             )