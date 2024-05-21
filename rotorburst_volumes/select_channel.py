from parapy.geom import *
from parapy.core import *
from math import pi
from parapy.core.widgets import Dropdown, ObjectPicker

from wiring.EWIS import EWIS
from assembly.config_conv import WingMounted
from assembly.config_t_tail import FuselageMounted

from assembly.assembly_aircraft import wing_mount


class RiskVolume(GeomBase):

    rotation = Input(0.0)

    if wing_mount:
        engines = WingMounted().engines

        @Part
        def assembly(self):
            return WingMounted()

    else:
        engines = FuselageMounted().engine

        @Part
        def assembly(self):
            return FuselageMounted()

    number_of_engines = list(range(engines.quantify))
    engine_index = Input(
        0,
        widget=Dropdown(number_of_engines, labels=["Left", "Right"], autocompute=True),
    )

    number_of_stages = list(range(engines[0].shaft.stages.quantify))
    engine_stage_index = Input(
        0,
        widget=Dropdown(
            number_of_stages, labels=["Fan", "LP-comp", "HP-comp", "HP-turb", "LP-turb"]
        ),
    )

    @Part
    def ewis(self):
        return EWIS()

    selected_channel = Input(widget=ObjectPicker(multiple=False, ask_confirmation=True))

    @Attribute
    def channel_y(self):
        return self.selected_channel.position.y

    @Attribute
    def channel_z(self):
        return self.selected_channel.position.z

    @Attribute
    def engine_shaft_location(self):
        return self.engines[self.engine_index].position

    @Attribute
    def engine_stage(self):
        return self.engines[self.engine_index].shaft.stages[self.engine_stage_index]

    @Attribute
    def radial_distance(self):
        return (
            (self.engine_stage.outerDiameter - self.engine_stage.hubDiameter) / 2
            + self.engine_stage.hubDiameter
        ) / 2

    @Attribute
    def risk_volume_length(self):
        return self.engine_stage.rotor_thickness

    @Attribute
    def risk_volume_width(self):
        return self.engine_stage.blade_span

    @Attribute
    def risk_volume_position(self):
        (Py, Pz) = (self.channel_y, self.channel_z)
        (Cy, Cz) = (self.engine_shaft_location.y, self.engine_shaft_location.z)

        a = self.radial_distance

        from math import sqrt, acos, atan2, sin, cos

        b = sqrt((Py - Cy) ** 2 + (Pz - Cz) ** 2)  # hypot() also works here
        th = acos(a / b)  # angle theta
        d = atan2(Pz - Cz, Py - Cy)  # direction angle of point P from C
        d1 = d + th  # direction angle of point T1 from C
        d2 = d - th  # direction angle of point T2 from C

        T1y = Cy + a * cos(d1)
        T1z = Cz + a * sin(d1)
        T2y = Cy + a * cos(d2)
        T2z = Cz + a * sin(d2)

        return (T1y, T1z), (T2y, T2z)

    @Attribute
    def risk_volume_start_point(self):
        return Point(
            x=self.engine_stage.position[0],
            y=self.risk_volume_position[0][0],
            z=self.risk_volume_position[0][1],
        )

    @Attribute
    def risk_volume_end_point(self):
        return Point(
            x=self.engine_stage.position[0], y=self.channel_y, z=self.channel_z
        )

    @Attribute
    def risk_volume_normal(self):
        vector = self.risk_volume_start_point - self.risk_volume_end_point
        return vector

    @Part
    def vertex(self):
        return LineSegment(
            start=self.risk_volume_start_point,
            end=self.risk_volume_end_point,
            hidden=True,
        )

    @Part
    def risk_volume_start_plane(self):
        return Plane(
            reference=self.risk_volume_start_point,
            normal=-self.risk_volume_normal,
            hidden=True,
        )

    # @Attribute
    # def direction(self):
    #
    #     return self.vertex.direction_vector

    @Part
    def risk_volume(self):
        return Box(
            width=self.risk_volume_width,
            length=self.risk_volume_length,
            height=self.vertex.length * 5,
            centered=False,
            position=Position((self.risk_volume_start_point))
            .rotate_to(self.risk_volume_start_plane.orientation)
            .rotate("y", self.rotation * pi / 180)
            .translate("x", -1 * self.risk_volume_width / 2),
            color="red",
        )


if __name__ == "__main__":
    from parapy.gui import display

    obj = RiskVolume()
    display(obj)
