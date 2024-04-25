from parapy.geom import *
from parapy.core import *

from assembly.assembly_aircraft import Assembly
from fuselage.EWIS import Ewis
from assembly.config_conv import WingMounted
from assembly.config_t_tail import FuselageMounted

from assembly.assembly_aircraft import wing_mount

class RiskVolume(GeomBase):
    ewis = Ewis()

    if wing_mount:
        engine = WingMounted().engine
    else:
        engine = FuselageMounted().engine

    channel_y = ewis.lower_channel2.position.y
    channel_z = ewis.lower_channel2.position.z

    engine_shaft_location = engine[0].position
    engine_stage = engine[0].shaft.stages[0]
    radial_distance = ((engine_stage.stage_outer_diameter - engine_stage.stage_hub_diameter)\
        / 4 + engine_stage.stage_hub_diameter) / 2

    risk_volume_length = engine_stage.blade_depths
    risk_volume_width = engine_stage.blade_heights

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
        return Point(x=self.engine_shaft_location[0],
                        y=self.risk_volume_position[0][0],
                        z=self.risk_volume_position[0][1])

    @Attribute
    def risk_volume_end_point(self):
        return Point(x=self.engine_shaft_location[0],
              y=self.channel_y,
              z=self.channel_z)

    @Attribute
    def risk_volume_normal(self):
        vector = self.risk_volume_start_point - self.risk_volume_end_point
        return vector

    @Part
    def vertex(self):
        return LineSegment(start = self.risk_volume_start_point,
                           end = self.risk_volume_end_point)

    @Part
    def risk_volume_end_plane(self):
        return Plane(reference=self.risk_volume_end_point,
                     normal=self.risk_volume_normal)

    @Part
    def risk_volume_start_plane(self):
        return Plane(reference=self.risk_volume_start_point,
                     normal=-self.risk_volume_normal)

    @Part
    def risk_volume(self):
        return Box(width=self.risk_volume_width, length=self.risk_volume_length, height=self.vertex.length,
                   centered=False,
                   position=Position((self.risk_volume_start_point)
                                     ).rotate_to(self.risk_volume_start_plane.orientation).translate('x', -1* self.risk_volume_width/2),
                   color='red')


    @Part
    def ewis(self):
        return Ewis()

    @Part
    def assembly(self):
        return Assembly()

if __name__ == '__main__':
    from parapy.gui import display
    obj = RiskVolume()
    display(obj)