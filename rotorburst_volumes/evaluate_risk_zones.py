from parapy.geom import *
from parapy.core import *
from parapy.core.widgets import Dropdown

import tkinter as tk
import tkinter.messagebox as tkmb

import numpy as np

from rotorburst_volumes.risk_volume import RiskVolume



class RiskVolumeAnalysis(GeomBase):
    configuration = Input()
    aircraft_config = Input()
    channel_shapes = Input()

    release_angle = Input(0.)

    # rotation direction of the engine (clockwise or counter clockwise)
    rotation_direction = Input(0, widget=Dropdown([1, 0], labels=["CW", "CCW"]))

    # angle at which the risk volume spreads as it propagates
    spread_angle = Input(5.0)

    # the index of the engine of interest, either "Left" (0) or "Right" (0)
    engine_index = Input(
        0, widget=Dropdown([0, 1], labels=["Left", "Right"], autocompute=True)
    )

    # the index of the stage of interest of the engine
    engine_stage_index = Input(
        0,
        widget=Dropdown(
            [0, 1, 2, 3, 4], labels=["Fan", "LP-comp", "HP-comp", "HP-turb", "LP-turb"]
        ),
    )

    @Attribute(label='Find critical release angles')
    # @action(label='Find critical release angles')
    def evaluate_risk_zones(self):
        orientation_range = np.arange(0, 95, 5)

        critical_orientation = []
        for idx in range(len(orientation_range)):
            print("Evaluating risk zones for angle", orientation_range[idx], "deg \t progress = ",
                  round(idx / len(orientation_range) * 100), "%")

            risk_volume_instances = RiskVolume(risk_volume_orientation=orientation_range[idx],
                                               engines=self.configuration.engine,
                                               aircraft_config=self.aircraft_config,
                                               rotation_direction=self.rotation_direction,
                                               spread_angle=self.spread_angle,
                                               engine_index=self.engine_index,
                                               engine_stage_index=self.engine_stage_index)

            intersection = IntersectedShapes(shape_in=risk_volume_instances.risk_volume_shell,
                                             tool=self.channel_shapes)

            if len(intersection.edges) > 54:
                critical_orientation.append(orientation_range[idx])

        print('\n critical orientations')
        print(critical_orientation)

        @Attribute
        def critical_angles():
            return critical_orientation

        tkmb.showinfo("Critical angles", str(critical_orientation))
        return critical_orientation


    @Part
    def risk_volume_instance(self):
        return RiskVolume(
            risk_volume_orientation=self.release_angle,
            engines=self.configuration.engine,
            aircraft_config=self.aircraft_config,
            pass_down="rotation_direction, spread_angle, engine_index, engine_stage_index")


    @Part
    def intersected_shapes(self):
        return IntersectedShapes(quantify=len(self.channel_shapes),
                                 shape_in=self.channel_shapes[child.index],
                                 tool=self.risk_volume_instance.risk_volume_shell,
                                 hidden=True)


    @Attribute
    def intersected_channels(self):
        intersected_channels = []

        for intersection in self.intersected_shapes:
            if len(intersection.edges) > 0:
                parent_intersected_channel = intersection.on_face(intersection.edges[0]).on_solids[0]
                intersected_channels.append(parent_intersected_channel)

        return intersected_channels

    @Part
    def channel_in_risk_zone(self):
        """
        Create fused solids for the shapes in [channel_shapes] that intersect with a risk volume at the determined
        orientation corresponding to a stage of an engine
        :return: GeomBase.FusedSolid
        """
        return FusedSolid(quantify=len(self.intersected_channels),
                          shape_in=self.risk_volume_instance.risk_volume_shell,
                          tool=self.intersected_channels[child.index],
                          color="red")  # , keep_tool=True, color='red')

