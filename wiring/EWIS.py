from parapy.geom import *
from parapy.core import *

from wiring.fuselage_channels import ThreeChannels, FourChannels
from wiring.wing_channels import WingChannels
from wiring.empennage_channels import EmpennageChannels


class EWIS(GeomBase):
    # The wiring configuration, either three or four channels along the length of the fuselage
    #: type: Bool
    configuration = Input()

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

    @Part
    def wing_channels(self):
        """
        Create the channels in the wing along the front and aft spar and the wing connector as a part
        :return: WingChannels object with GeomBase.PipeSolid as parts
        """
        return WingChannels(
            pass_down="front_spar_root_pos, aft_spar_root_pos, front_spar_tip_pos, aft_spar_tip_pos"
        )

    @Part
    def empennage_channels(self):
        """
        Create the channels in the empennage as parts
        :return: EmpennageChannels object with ChannelVtail and ChannelX as part types
        """
        return EmpennageChannels()

    @Part
    def fuselage_channels(self):
        """
        Create the channels in the fuselage as parts
        :return: ThreeChannels or Fourchannels object with GeomBase.PipeSolids as parts
        """
        return DynamicType(
            type=ThreeChannels if self.configuration == True else FourChannels
        )


if __name__ == "__main__":
    from parapy.gui import display

    obj = FourChannels()
    display(obj)
