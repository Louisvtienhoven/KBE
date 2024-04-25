from parapy.geom import *
from parapy.core import *

from engine.engine_full import Engine
from fuselage.aircraft_body import AircraftBody
from fuselage.wing import Wing
from fuselage.channel import ChannelSweep, ChannelZ, ChannelX


from assembly.config_conv import WingMounted
from assembly.config_t_tail import FuselageMounted

#Conventional Layout -> for T-tail: wing_mount = False
wing_mount = True

class Assembly(GeomBase):
    @Part
    def aircraftbody(self):
        return AircraftBody(position=self.position)


    #Wing mounted case
    if wing_mount == True:
        @Part
        def wing_mount(self):
            return WingMounted(position=self.position)

    #Fuselage mounted case
    elif wing_mount == False:
        @Part
        def fuselage_mount(self):
            return FuselageMounted(position=self.position)

if __name__ == '__main__':
    from parapy.gui import display
    obj = Assembly()
    display(obj)


