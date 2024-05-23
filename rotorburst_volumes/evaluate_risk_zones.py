from parapy.geom import *
from parapy.core import *
from parapy.core.widgets import Dropdown

import tkinter.messagebox as tkmb

import numpy as np

from rotorburst_volumes.risk_volume import RiskVolume
from rotorburst_volumes.create_overview import RotorBurstOverview


class RiskVolumeAnalysis(GeomBase):
    configuration = Input()
    channel_shapes = Input()

    release_angle = Input(0.0)

    granularity = Input(5, label="Steps in angle for PRA")
    start_evaluation = Input(40, label="Start angle of evaluation")
    end_evaluation = Input(45, label="Stop angle of evaluation")

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

    #@Attribute(label="Find critical release angles")
    @action(label='Find critical release angles')
    def evaluate_risk_zones(self):
        orientation_range = np.arange(
            self.start_evaluation,
            self.end_evaluation + self.granularity,
            self.granularity,
        )

        critical_orientation = []
        for idx in range(len(orientation_range)):
            print(
                "Evaluating risk zones for angle",
                orientation_range[idx],
                "deg \t progress = ",
                round(idx / len(orientation_range) * 100),
                "%",
            )

            risk_volume_instances = RiskVolume(
                risk_volume_orientation=orientation_range[idx],
                engines=self.configuration.engine,
                rotation_direction=self.rotation_direction,
                spread_angle=self.spread_angle,
                engine_index=self.engine_index,
                engine_stage_index=self.engine_stage_index,
            )

            intersection = IntersectedShapes(
                shape_in=risk_volume_instances.risk_volume_shell,
                tool=self.channel_shapes,
            )

            if len(intersection.edges) > 53:
                # TODO: implement on_face method
                critical_orientation.append(orientation_range[idx])

        print("\n critical orientations")
        print(critical_orientation)

        @Attribute
        def critical_angles():
            return critical_orientation

        tkmb.showinfo("Critical angles", str(critical_orientation))
        return critical_orientation

    @Part
    def risk_volume_instance(self):
        """
        Visualize the risk zone for the selected engine stage for the desired release angle
        :return: RiskVolume object with a LoftedSolid as part
        """
        return RiskVolume(
            risk_volume_orientation=self.release_angle,
            engines=self.configuration.engines,
            pass_down="rotation_direction, spread_angle, engine_index, engine_stage_index",
        )

    @Part
    def intersected_shapes(self):
        """
        Create intersected shapes between the channels and risk_volume_instance to see which channels are hit
        :return: GeomBase.IntersectedShapes
        """
        return IntersectedShapes(
            quantify=len(self.channel_shapes),
            shape_in=self.channel_shapes[child.index],
            tool=self.risk_volume_instance.risk_volume_shell,
            # hidden=True,
        )

    @Attribute
    def intersected_channels(self):
        """
        Determine which channels are hit by the risk_volume_instance
        :return: list of GeomBase.Solids
        """
        intersected_channels = []

        for intersection in self.intersected_shapes:
            if len(intersection.edges) > 0:
                parent_intersected_channel = intersection.on_face(
                    intersection.edges[0]
                ).on_solids[0]
                intersected_channels.append(parent_intersected_channel)

        return intersected_channels

    @Part
    def channel_in_risk_zone(self):
        """
        Create fused solids for the shapes in [channel_shapes] that intersect with a risk volume at the determined
        orientation corresponding to a stage of an engine
        :return: GeomBase.FusedSolid
        """
        return FusedSolid(
            shape_in=self.risk_volume_instance.risk_volume_shell,
            tool=self.intersected_channels,
            color="red",
        )  # raises runtime error when no intersection

    @Attribute
    def pra_overview(self):
        channels_hit = self.channel_in_risk_zone.tool
        channels_hit_names = []
        for channel in channels_hit:
            name = str(channel).split(".")[-1].split(" ")[0]
            channels_hit_names.append(name)

        return channels_hit_names

    @Part
    def overview(self):
        return RotorBurstOverview(
            pass_down="configuration, channel_shapes, rotation_direction, spread_angle,engine_index, engine_stage_index",
            critical_angles=self.evaluate_risk_zones,
        )
