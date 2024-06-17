from parapy.geom import *
from parapy.core import *
from parapy.core.widgets import Dropdown

import tkinter.messagebox as tkmb
import numpy as np

from rotorburst_analysis.risk_volume import RiskVolume

import matlab.engine

MATLAB_ENGINE = matlab.engine.start_matlab()


class RiskVolumeAnalysis(GeomBase):
    wiring_config = Input()  # three or four channels

    # The tail configuration of the aircraft
    configuration = Input()

    # A sequence of Shape objects
    channel_shapes = Input()

    # float specifying the release angle of the fragment in degrees
    release_angle = Input(0.0)

    granularity = Input(5, label="Steps in angle for PRA")
    start_evaluation = Input(40, label="Start angle of evaluation")
    end_evaluation = Input(45, label="Stop angle of evaluation")

    # rotation direction of the engine (clockwise or counter clockwise)
    rotation_direction = Input(0, widget=Dropdown([1, 0], labels=["CW", "CCW"]))

    # angle at which the risk volume spreads as it propagates
    spread_angle = Input(5.0)

    # the index of the engine of interest, either "Left" (0) or "Right" (0)
    list_engine_sides = ["Left", "Right"]
    engine_index = Input(
        0, widget=Dropdown([0, 1], labels=list_engine_sides, autocompute=True)
    )

    # the index of the stage of interest of the engine
    list_engine_stages = ["Fan", "LP-comp", "HP-comp", "HP-turb", "LP-turb"]
    engine_stage_index = Input(
        0,
        widget=Dropdown([0, 1, 2, 3, 4], labels=list_engine_stages),
    )

    @Attribute
    def intersection_threshold(self):
        """
        Based on the wiring configuration, there is a standard number of intersecting shapes of the
        channels themselves.
        :return: int
        """
        if self.wiring_config == True:  # three channels
            if self.configuration == True:  # Wing mounted
                threshold = 73
            else:  # Fuselage mounted
                threshold = 61

        elif self.wiring_config == False:  # four channels
            if self.configuration == True:  # Wing mounted
                threshold = 128
            else:  # Fuselage mounted
                threshold = 110

        return threshold

    @action(label="Find critical release angles")
    def evaluate_risk_zones(self):
        """
        Loop over all angles between [self.start_evaluation] and [self.end_evaluation]
        :return: list of release angles that result in a channel being hit
        """
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
                engines=self.configuration.engines,
                rotation_direction=self.rotation_direction,
                spread_angle=self.spread_angle,
                engine_index=self.engine_index,
                engine_stage_index=self.engine_stage_index,
            )

            intersection = IntersectedShapes(
                shape_in=risk_volume_instances.risk_volume_shell,
                tool=self.channel_shapes,
            )

            if len(intersection.edges) > self.intersection_threshold:
                critical_orientation.append(orientation_range[idx])

        print("\n critical orientations")
        print(self.list_engine_stages[self.engine_stage_index], critical_orientation)

        tkmb.showinfo("Critical angles", str(critical_orientation))
        return critical_orientation

    @Part
    def threshold(self):
        return IntersectedShapes(
            shape_in=self.risk_volume_instance.risk_volume_shell,
            tool=self.channel_shapes,
            hidden=True,
        )

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
    def channels_hit(self):
        """
        Create a list of the channels which are hit in the displayed orientation
        :return: list
        """
        channels_hit = self.channel_in_risk_zone.tool
        channels_hit_names = []
        for channel in channels_hit:
            name = str(channel).split(".")[-1].split(" ")[0]
            channels_hit_names.append(name)

        return channels_hit_names

    @action(label="save critical orientation")
    def save_orientation(self):
        """
        Save the critical orientation that is being visualised in the GUI based on the engine stage.
        :return: pandas.DataFrame
        """
        import pandas as pd

        channels = self.channels_hit
        angles = self.release_angle
        overview = pd.DataFrame(index=channels, columns=[angles])
        overview.loc[:, angles] = True

        print(overview)

        overview.to_csv(
            f"wiring/saved_orientations/{self.list_engine_sides[self.engine_index]}/{self.list_engine_stages[self.engine_stage_index]}/{self.engine_stage_index}_{self.engine_index}_{angles}.csv"
        )

    pathchanged = False

    @action(label="create PRA overview")
    def make_table(self):
        """
        Create an external overview of the saved critical orientations per engine and per engine stage
        :return: MatLab uitable
        """
        dir = f"../wiring/saved_orientations/{self.list_engine_sides[self.engine_index]}/{self.list_engine_stages[self.engine_stage_index]}"

        if not self.pathchanged:
            # change matlab root directory to Q3D, so it can find the function
            MATLAB_ENGINE.cd(r"./matlab_files")
            self.pathchanged = True

        return MATLAB_ENGINE.make_table(dir)
