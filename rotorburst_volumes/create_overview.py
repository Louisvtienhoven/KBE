from parapy.geom import *
from parapy.core import *

from rotorburst_volumes.risk_volume import RiskVolume


class RotorBurstOverview(GeomBase):
    critical_angles = Input([])
    configuration = Input()
    channel_shapes = Input()

    engine_index = Input()
    engine_stage_index = Input()
    rotation_direction = Input()
    spread_angle = Input()

    @action
    def create_overview(self):
        overview = []
        for release_angle in self.critical_angles:
            critical_risk_volume = RiskVolume(
                risk_volume_orientation=release_angle,
                engines=self.configuration.engine,
                rotation_direction=self.rotation_direction,
                spread_angle=self.spread_angle,
                engine_index=self.engine_index,
                engine_stage_index=self.engine_stage_index,
            )

            intersected_shapes = FusedSolid(
                shape_in=critical_risk_volume.risk_volume_shell,
                tool=self.channel_shapes,
            )

            intersected_channels = []

            for intersection in intersected_shapes:
                if len(intersection.edges) > 0:
                    parent_intersected_channel = intersection.on_face(
                        intersection.edges[0]
                    ).on_solids[0]
                    intersected_channels.append(parent_intersected_channel)
            overview.append(intersected_shapes)
        print(overview)

    # @Attribute
    # def pra_overview(self):
    #     channels_hit = self.channel_in_risk_zone.tool
    #     channels_hit_names = []
    #     for channel in channels_hit:
    #         name = str(channel).split(".")[-1].split(" ")[0]
    #         channels_hit_names.append(name)
    #
    #     return channels_hit_names
