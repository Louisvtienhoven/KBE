from parapy.geom import *
from parapy.core import *

from wiring.wing_channels import WingChannels


class VTailChannels(GeomBase):
    v_tail = Input()
    connector_spanwise_position = Input()

    @Attribute
    def front_connector_pos(self):
        """
        Determine the front location of the wing connector along the front spar channel
        :return: generic.positioning.Position
        """
        return (
            self.v_tail.front_spar_root_location
            + (
                self.v_tail.front_spar_tip_location
                - self.v_tail.front_spar_root_location
            )
            * self.connector_spanwise_position
        )

    @Attribute
    def aft_connector_pos(self):
        """
        Determine the aft location of the wing connector along the aft spar channel
        :return: generic.positioning.Position
        """
        return (
            self.v_tail.aft_spar_root_location
            + (self.v_tail.aft_spar_tip_location - self.v_tail.aft_spar_root_location)
            * self.connector_spanwise_position
        )

    @Part
    def connector(self):
        """
        Create a connector as pipesolid between the front and aft position of the connector
        :return: GeomBase.PipeSolid
        """
        return PipeSolid(
            LineSegment(start=self.front_connector_pos, end=self.aft_connector_pos),
            radius=0.07,
        )

    @Part
    def vtail_aftspar(self):
        """
        Create a channel as pipesolid along the aft spar of the vertical tail
        :return: GeomBase.PipeSolid
        """
        return PipeSolid(
            LineSegment(
                start=self.v_tail.aft_spar_root_location,
                end=self.v_tail.aft_spar_tip_location,
            ),
            radius=0.04,
            color="Blue",
        )

    @Part
    def vtail_frontspar(self):
        """
        Create a channel as pipesolid along the front spar of the vertical tail
        :return: GeomBase.PipeSolid
        """
        return PipeSolid(
            LineSegment(
                start=self.v_tail.front_spar_root_location,
                end=self.v_tail.front_spar_tip_location,
            ),
            radius=0.04,
            color="Blue",
        )


class EmpennageChannels(GeomBase):
    h_tail = Input()
    v_tail = Input()
    connector_spanwise_position = Input(0.8)

    @Part
    def h_tail_channels(self):
        """
        Create the channels in the horizontal tail plane based on the WingChannels class
        :return: WingChannels object
        """
        return WingChannels(wing=self.h_tail, pass_down="connector_spanwise_position")

    @Part
    def v_tail_channels(self):
        """
        Create the channels in the vertical tail plane based on the VTailChannels class
        :return: VTailChannels object
        """
        return VTailChannels(pass_down="connector_spanwise_position, v_tail")
