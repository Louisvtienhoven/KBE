from parapy.geom import *
from parapy.core import *

from engine.engine_full import Engine
from fuselage.aircraft_body import AircraftBody
from fuselage.wing import Wing
from fuselage.channel import ChannelSweep, ChannelZ, ChannelX

from engine.engine_pylon import Pylon

from config_conv import WingMounted
from config_t_tail import FuselageMounted



class Assembly(GeomBase):
    wing_mount = False

    @Part
    def aircraftbody(self):
        return AircraftBody(position=self.position)

    #Wing mounted case
    if wing_mount:
        @Part
        def wing_mount_layout(self):
            return WingMounted(position=self.position)

    #Fuselage mounted case
    elif wing_mount == False:
        @Part
        def fuselage_mount_layout(self):
            return FuselageMounted(position=self.position)



if __name__ == '__main__':
    from parapy.gui import display
    obj = Assembly()
    display(obj)


