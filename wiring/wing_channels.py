from parapy.geom import *
from parapy.core import *

class WingChannels(GeomBase):
    front_spar_tip_pos = Input(Position(Point(0, 0, 0)))
    front_spar_root_pos = Input(Position(Point(1, 0, 0)))
    aft_spar_tip_pos = Input(Position(Point(0, 1, 0)))
    aft_spar_root_pos = Input(Position(Point(1, 1, 0)))

    @Attribute
    def front_spar_plane_normal(self):
        return self.front_spar_tip_pos - self.front_spar_root_pos

    @Attribute
    def aft_spar_plane_normal(self):
        return self.aft_spar_tip_pos - self.aft_spar_root_pos

    @Part
    def front_spar(self):
        return LineSegment(
            start=self.front_spar_root_pos.point, end=self.front_spar_tip_pos.point
        )

    @Part
    def aft_spar(self):
        return LineSegment(
            start=self.aft_spar_root_pos.point, end=self.aft_spar_tip_pos.point
        )

    @Part
    def right_front_spar_channel(self):
        return PipeSolid(path=self.front_spar, radius=0.07)

    @Part
    def right_aft_spar_channel(self):
        return PipeSolid(path=self.aft_spar, radius=0.07)

    @Part
    def left_front_spar_channel(self):
        return MirroredShape(shape_in=self.right_front_spar_channel,
                             reference_point = self.position,
                             vector1=self.position.Vx,
                             vector2=self.position.Vz)

    @Part
    def left_aft_spar_channel(self):
        return MirroredShape(shape_in=self.right_aft_spar_channel,
                             reference_point = self.position,
                             vector1=self.position.Vx,
                             vector2=self.position.Vz)


if __name__ == "__main__":
    from parapy.gui import display

    obj = WingChannels()
    display(obj)

