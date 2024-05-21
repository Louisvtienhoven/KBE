from parapy.geom import *
from parapy.core import *


class WingChannels(GeomBase):
    front_spar_tip_pos = Input()
    front_spar_root_pos = Input()
    aft_spar_tip_pos = Input()
    aft_spar_root_pos = Input()

    connector_spanwise_position = Input(0.75)

    @Attribute
    def wing_connector_segment(self):
        return self.front_connector_pos - self.aft_connector_pos

    @Attribute
    def front_spar_vector(self):
        return self.front_spar_tip_pos - self.front_spar_root_pos

    @Attribute
    def aft_spar_vector(self):
        return self.aft_spar_tip_pos - self.aft_spar_root_pos

    @Attribute
    def front_connector_pos(self):
        return (
            self.front_spar_root_pos
            + self.front_spar_vector * self.connector_spanwise_position
        )

    @Attribute
    def aft_connector_pos(self):
        return (
            self.aft_spar_root_pos
            + self.aft_spar_vector * self.connector_spanwise_position
        )

    @Part
    def connector_segment(self):
        return LineSegment(
            start=self.front_connector_pos.point, end=self.aft_connector_pos
        )

    @Part
    def right_connector(self):
        return PipeSolid(path=self.connector_segment, radius=0.07)

    @Part
    def left_connector(self):
        return MirroredShape(
            shape_in=self.right_connector,
            reference_point=self.position,
            vector1=self.position.Vx,
            vector2=self.position.Vz,
        )

    @Part
    def front_spar(self):
        return LineSegment(
            start=self.front_spar_root_pos.point,
            end=self.front_spar_tip_pos.point,
            hidden=True,
        )

    @Part
    def aft_spar(self):
        return LineSegment(
            start=self.aft_spar_root_pos.point,
            end=self.aft_spar_tip_pos.point,
            hidden=True,
        )

    @Part
    def right_front_spar_channel(self):
        return PipeSolid(path=self.front_spar, radius=0.07)

    @Part
    def right_aft_spar_channel(self):
        return PipeSolid(path=self.aft_spar, radius=0.07)

    @Part
    def left_front_spar_channel(self):
        return MirroredShape(
            shape_in=self.right_front_spar_channel,
            reference_point=self.position,
            vector1=self.position.Vx,
            vector2=self.position.Vz,
        )

    @Part
    def left_aft_spar_channel(self):
        return MirroredShape(
            shape_in=self.right_aft_spar_channel,
            reference_point=self.position,
            vector1=self.position.Vx,
            vector2=self.position.Vz,
        )
