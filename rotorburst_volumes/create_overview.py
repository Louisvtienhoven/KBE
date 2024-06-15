from parapy.geom import *
from parapy.core import *

from rotorburst_volumes.risk_volume import RiskVolume


class RotorBurstOverview(GeomBase):
    risk_volume_release_angle = Input()
    configuration = Input()
    channel_shapes = Input()

    engine_index = Input()
    engine_stage_index = Input()
    rotation_direction = Input()
    spread_angle = Input()

    @Part
    def critical_risk_volume(self):
        return RiskVolume(
            risk_volume_orientation=self.risk_volume_release_angle,
            engines=self.configuration.engines,
            rotation_direction=self.rotation_direction,
            spread_angle=self.spread_angle,
            engine_index=self.engine_index,
            engine_stage_index=self.engine_stage_index,
        )

    @Part
    def intersected_shapes_for_risk_vol_instance(self):
        return IntersectedShapes(
                    quantify=len(self.channel_shapes),
                    shape_in=self.channel_shapes[child.index],
                    tool=self.risk_volume_instance.risk_volume_shell,
                    # hidden=True,
                )

    @Attribute
    def intersected_channels_for_risk_vol_instance(self):
        intersected_channels_for_risk_vol_instance = []
        for intersection in self.intersected_shapes_for_risk_vol_instance:
            if len(intersection.edges) > 0:
                parent_intersected_channel = intersection.on_face(
                    intersection.edges[0]
                ).on_solids[0]
                intersected_channels_for_risk_vol_instance.append(parent_intersected_channel)

        print(intersected_channels_for_risk_vol_instance, 'Check')

    # @Attribute
    # def pra_overview(self):
    #     channels_hit = self.channel_in_risk_zone.tool
    #     channels_hit_names = []
    #     for channel in channels_hit:
    #         name = str(channel).split(".")[-1].split(" ")[0]
    #         channels_hit_names.append(name)
    #
    #     return channels_hit_names
