from parapy.geom import *
from parapy.core import *

from wiring.fuselage_channels import ThreeChannels, FourChannels
from wiring.wing_channels import WingChannels
from wiring.empennage_channels import EmpennageChannels


class EWIS(GeomBase):
    configuration = Input()

    front_spar_root_pos = Input()
    aft_spar_root_pos = Input()
    front_spar_tip_pos = Input()
    aft_spar_tip_pos = Input()

    @Part
    def wing_channels(self):
        return WingChannels(
            pass_down="front_spar_root_pos, aft_spar_root_pos, front_spar_tip_pos, aft_spar_tip_pos"
        )

    @Part
    def empennage_channels(self):
        return EmpennageChannels()

    @Part
    def fuselage_channels(self):
        return DynamicType(
            type=ThreeChannels if self.configuration == True else FourChannels
        )


if __name__ == "__main__":
    from parapy.gui import display

    obj = FourChannels()
    display(obj)
