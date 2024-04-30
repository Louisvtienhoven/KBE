from parapy.geom import *
from parapy.core import *

from fuselage.aircraft_body import AircraftBody

from assembly.config_conv import WingMounted
from assembly.config_t_tail import FuselageMounted


class Assembly(GeomBase):
    wing_mount = Input(True)

    @Part
    def aircraftbody(self):
        return AircraftBody(position=self.position)

    # @Part
    # def configuration(self):
    #     if self.wing_mount == True:
    #         return WingMounted()
    #     else:
    #         return FuselageMounted()

    # #Wing mounted case
    # if wing_mount == True:
    #     @Part
    #     def configuration(self):
    #         return WingMounted(position=self.position)
    #
    # #Fuselage mounted case
    # elif wing_mount == False:
    #     @Part
    #     def configuration(self):
    #         return FuselageMounted(position=self.position)

if __name__ == '__main__':
    from parapy.gui import display
    obj = Assembly()
    display(obj)


