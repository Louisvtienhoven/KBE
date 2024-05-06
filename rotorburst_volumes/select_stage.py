from parapy.geom import *
from parapy.core import *
from math import pi
from parapy.core.widgets import Dropdown, ObjectPicker, PyField

# from assembly.config_t_tail import FuselageMounted
# from assembly.config_conv import WingMounted
from main import Main


class RiskVolumePerStage(GeomBase):
    engines = Main().configuration.engine

    risk_volume_height = Input(10.0)
    risk_volume_orientation = Input(90.0)

    rotation_direction = Input(0, widget=Dropdown([0, 1], labels=["CW", "CCW"]))

    number_of_engines = list(range(engines.quantify))
    engine_index = Input(
        0,
        widget=Dropdown(number_of_engines, labels=["Left", "Right"], autocompute=True),
    )

    number_of_stages = list(range(engines[0].shaft.stages.quantify))
    engine_stage_index = Input(
        0,
        widget=Dropdown(
            number_of_stages, labels=["Fan", "LP-comp", "HP-comp", "HP-turb", "LP-turb"]
        ),
    )

    @Attribute
    def engine_shaft_location(self):
        return self.engines[self.engine_index].position

    @Attribute
    def engine_stage(self):
        return self.engines[self.engine_index].shaft.stages[self.engine_stage_index]

    @Attribute
    def risk_volume_length(self):
        return self.engine_stage.rotorThickness

    @Attribute
    def risk_volume_width(self):
        return self.engine_stage.bladeSpan

    @Part
    def risk_volume_CW_turning(self):
        return Box(
            quantify=self.engine_stage.rotors.quantify,
            width=self.risk_volume_height,
            length=self.engine_stage.bladeSpan,
            height=self.engine_stage.rotorThickness,
            position=translate(
                rotate(
                    self.engine_stage.position,
                    "z",
                    angle=self.risk_volume_orientation,
                    deg=True,
                ),
                "y",
                self.engine_stage.hubDiameter / 2,
                "z",
                child.index * self.engine_stage.rotorThickness * 2,
            ),
            color="red",
        )

    @Part
    def risk_volume_CCW_turning(self):
        return Box(
            quantify=self.engine_stage.rotors.quantify,
            width=self.risk_volume_height,
            length=self.engine_stage.bladeSpan,
            height=self.engine_stage.rotorThickness,
            position=translate(
                rotate(
                    translate(self.engine_stage.position, "x", self.risk_volume_height),
                    "z",
                    angle=self.risk_volume_orientation,
                    deg=True,
                ),
                "y",
                self.engine_stage.hubDiameter / 2,
                "z",
                child.index * self.engine_stage.rotorThickness * 2,
            ),
            color="red",
        )


if __name__ == "__main__":
    from parapy.gui import display

    obj = RiskVolumePerStage()
    display(obj)
