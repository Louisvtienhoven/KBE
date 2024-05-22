from parapy.geom import *
from parapy.core import *


class WingChannels(GeomBase):
    # The position of the root location of the front spar
    #: type: generic.positioning.Position
    front_spar_root_pos = Input()

    # The position of the root location of the aft spar
    #: type: generic.positioning.Position
    aft_spar_root_pos = Input()

    # The position of the tip location of the front spar
    #: type: generic.positioning.Position
    front_spar_tip_pos = Input()

    # The position of the tip location of the aft spar
    #: type: generic.positioning.Position
    aft_spar_tip_pos = Input()

    # The spanwise position of the connector between the front and aft spar channels
    #: type: float
    connector_spanwise_position = Input(0.75)

    @Attribute
    def wing_connector_segment(self):
        """
        Create a vector between the front and aft position of the wing connector
        :return: generic.positioning.Vector
        """
        return self.front_connector_pos - self.aft_connector_pos

    @Attribute
    def front_spar_vector(self):
        """
        Create a vector from the root to the tip position of the front spar
        :return: generic.positioning.Vector
        """
        return self.front_spar_tip_pos - self.front_spar_root_pos

    @Attribute
    def aft_spar_vector(self):
        """
        Create a vector from the root to the tip position of the aft spar
        :return: generic.positioning.Vector
        """
        return self.aft_spar_tip_pos - self.aft_spar_root_pos

    @Attribute
    def front_connector_pos(self):
        """
        Determine the front location of the wing connector along the front spar channel
        :return: generic.positioning.Position
        """
        return (
            self.front_spar_root_pos
            + self.front_spar_vector * self.connector_spanwise_position
        )

    @Attribute
    def aft_connector_pos(self):
        """
        Determine the aft location of the wing connector along the aft spar channel
        :return: generic.positioning.Position
        """
        return (
            self.aft_spar_root_pos
            + self.aft_spar_vector * self.connector_spanwise_position
        )

    @Part
    def connector_segment(self):
        """
        Create a LineSegment for the connector to base a PipeSolid on
        :return: LineSegment
        """
        return LineSegment(
            start=self.front_connector_pos.point, end=self.aft_connector_pos
        )

    @Part
    def right_connector(self):
        """
        Create the connector in the right wing as a part
        :return: PipeSolid
        """
        return PipeSolid(path=self.connector_segment, radius=0.07)

    @Part
    def left_connector(self):
        """
        Create the connector in the left wing as a part as a mirrored shape of right_connector, mirrored in the xz-plane
        :return: MirroredShape(PipeSolid)
        """
        return MirroredShape(
            shape_in=self.right_connector,
            reference_point=self.position,
            vector1=self.position.Vx,
            vector2=self.position.Vz,
        )

    @Part
    def front_spar(self):
        """
        Create a line segment for the front spar to base a channel as PipeSolid on
        :return: LineSegment
        """
        return LineSegment(
            start=self.front_spar_root_pos.point,
            end=self.front_spar_tip_pos.point,
            hidden=True,
        )

    @Part
    def aft_spar(self):
        """
        Create a line segment for the aft spar to base a channel as PipeSolid on
        :return: LineSegment
        """
        return LineSegment(
            start=self.aft_spar_root_pos.point,
            end=self.aft_spar_tip_pos.point,
            hidden=True,
        )

    @Part
    def right_front_spar_channel(self):
        """
        Create the front spar channel in the right wing as a part
        :return: PipeSolid
        """
        return PipeSolid(path=self.front_spar, radius=0.07)

    @Part
    def right_aft_spar_channel(self):
        """
        Create the aft spar channel in the right wing as a part
        :return: PipeSolid
        """
        return PipeSolid(path=self.aft_spar, radius=0.07)

    @Part
    def left_front_spar_channel(self):
        """
        Create the front spar channel in the left wing as a part, mirrored in the xz-plane
        :return: MirroredShape(PipeSolid)
        """
        return MirroredShape(
            shape_in=self.right_front_spar_channel,
            reference_point=self.position,
            vector1=self.position.Vx,
            vector2=self.position.Vz,
        )

    @Part
    def left_aft_spar_channel(self):
        """
        Create the aft spar channel in the left wing as a part, mirrored in the xz-plane
        :return: MirroredShape(PipeSolid)
        """
        return MirroredShape(
            shape_in=self.right_aft_spar_channel,
            reference_point=self.position,
            vector1=self.position.Vx,
            vector2=self.position.Vz,
        )
