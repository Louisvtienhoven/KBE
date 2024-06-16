import numpy as np
from parapy.geom import *
from parapy.core import *


class RiskVolume(GeomBase):
    engines = Input()

    # rotation direction of the engine (clockwise or counter clockwise)
    rotation_direction = Input()
    # height of the risk volume from start to end plane
    risk_volume_height = Input(10.0)

    # orientation of the risk volume with 0-deg along the +z axis
    risk_volume_orientation = Input(0.0)

    # angle at which the risk volume spreads as it propagates
    spread_angle = Input()  # 5.0)

    # the index of the engine of interest, either "Left" (0) or "Right" (0)
    engine_index = Input()

    # the index of the stage of interest of the engine
    engine_stage_index = Input()  #


    @Attribute
    def engine_stage(self):
        """
        Select which engine of the model is used as the base for the rotor burst analysis
        :return: Engine object
        """
        return self.engines[self.engine_index].shaft.stages[self.engine_stage_index]

    @Attribute
    def risk_volume_position(self):
        """
        Determine the position of the risk volume based on the corresponding engine stage.
        The orientation of the risk volume aligns with the reference system in the GUI with an orientation of
        0 deg upwards, in accordance with CS25
        :return: GeomBase.Position object
        """
        return Position(
            self.engine_stage.position,
            orientation=Orientation(
                x=Vector(1, 0, 0), y=Vector(0, 1, 0), z=Vector(0, 0, 1)
            ),
        )

    @Part
    def risk_volume_plane(self):
        """
        The start plane of the risk volume, corresponding to the engine stage that is analysed. The normal of the plane
        is in the positive z-direction. The Position of the plane is translated to comply with the centroid of a
        third-disk fragment, in compliance with CS25
        :return: GeomBase.Rectangle
        """
        return Rectangle(
            width=self.engine_stage.stageThickness,
            length=self.engine_stage.risk_volume_size,
            position=translate(
                rotate(
                    self.risk_volume_position,
                    "x",
                    angle=self.risk_volume_orientation,
                    deg=True,
                ),
                "x",
                self.engine_stage.stageThickness / 2,
                "y",
                self.engine_stage.offAxisTranslation
                - self.engine_stage.risk_volume_size / 2,
                "y",
                -(2**self.rotation_direction)
                * self.rotation_direction
                * (
                    self.engine_stage.offAxisTranslation
                    - self.engine_stage.risk_volume_size / 2
                ),
            ),
        )

    @Part
    def risk_volume_spread_plane(self):
        """
        The spread angle of the risk volume from the engine stage outwards. A default of +/- 5 deg has been selected.
        With this spread angle, the plane at a predetermined offset form [risk_volume_plane] is defined.
        :return: GeomBase.Rectangle
        """
        return Rectangle(
            width=self.engine_stage.stageThickness
            + 2 * np.tan(np.deg2rad(self.spread_angle)) * self.risk_volume_height,
            length=self.engine_stage.risk_volume_size,
            position=translate(
                self.risk_volume_plane.position, "z", self.risk_volume_height
            ),
        )

    @Part
    def risk_volume_shell(self):
        """
        Lofted shell to visualise the risk zone per stage of interest per engine of interest
        :return: GeomBase.LoftedSolid
        """
        return LoftedSolid(
            profiles=[self.risk_volume_plane, self.risk_volume_spread_plane],
            color="red",
            transparency=0.8,
        )
