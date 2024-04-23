from parapy.geom import *
from parapy.core import *

from engine.engine_full import Engine
from fuselage.aircraft_body import AircraftBody
from fuselage.wing import Wing
from fuselage.channel import ChannelSweep, ChannelZ, ChannelX




class Assembly(GeomBase):
    wing_mount = True

    x_pos_engine_wing = Input(16.5)
    y_pos_engine_wing = Input(5)
    z_pos_engine_wing = Input(-2.15)

    y_pos_engine_fus = Input(3)
    z_pos_engine_fus = Input(1.)
    x_pos_engine_fus = Input(32)

    @Part
    def aircraftbody(self):
        return AircraftBody(position=self.position)

    #Wing mounted case
    if wing_mount:
        @Part
        def engine(self):
            return Engine(quantify=2,
                          position=translate(self.position.rotate90('y','z'),
                                            'x',self.y_pos_engine_wing,
                                            'y',self.z_pos_engine_wing*(-1)**child.index,
                                            'z',self.x_pos_engine_wing)
                                            )  # circles are in XY plane, thus need rotation
        @Part
        def h_tail(self):
            return Wing(position=translate(self.position, 'x',40.5, 'y', 1.3, 'z', 0),
                        w_semi_span=4.5,
                        dihedral=0.5,
                        w_c_root=3.31,
                        w_c_tip =1.24,
                        sweep_TE = 15,
                        transparency = 0.5

                        )

        @Part
        def channel_htail1(self):
            return ChannelSweep(ch_radius=.04, position=translate(self.position, 'x', 37.7, 'y', 1, 'z', 0),
                                color='Blue',
                                sweep_rad=0.8,
                                ch_length=4,
                                dihedral=0.15)

        @Part
        def channel_htail2(self):
            return MirroredShape(shape_in=self.channel11,
                                 reference_point=self.position,
                                 # Two vectors to define the mirror plane
                                 vector1=self.position.Vz,
                                 vector2=self.position.Vx,
                                 mesh_deflection=0.0001,
                                 color='Blue')

        @Part
        def channel_htail3(self):
            return ChannelSweep(ch_radius=.04, position=translate(self.position, 'x', 40, 'y', 1, 'z', 0.04),
                                color='Blue', sweep_rad=1.3, dihedral=0.4, ch_length=3.3)

        @Part
        def channel_htail4(self):
            return MirroredShape(shape_in=self.channel13,
                                 reference_point=self.position,
                                 # Two vectors to define the mirror plane
                                 vector1=self.position.Vz,
                                 vector2=self.position.Vx,
                                 mesh_deflection=0.0001,
                                 color='Blue')
        @Part
        def channel_htail5(self):
            return ChannelZ(ch_radius=.04, position=translate(self.position, 'x', 40, 'y', 1, 'z', 0.05),
                            ch_length=1,
                            color='Blue',
                            )



        @Part
        def channel_htail6(self):
            return MirroredShape(shape_in=self.channel_htail5,
                                 reference_point=self.position,
                                 # Two vectors to define the mirror plane
                                 vector1=self.position.Vz,
                                 vector2=self.position.Vx,
                                 mesh_deflection=0.0001,
                                 color='Blue')


        @Part
        def channel_htail7(self):
            return ChannelX(ch_radius=.02, position=translate(self.position, 'x', 38.9, 'y', 2.7, 'z', 0.23),
                            color='Blue',
                            ch_length=1.55
                            )

        @Part
        def channel_htail8(self):
            return MirroredShape(shape_in=self.channel7,
                                 reference_point=self.position,
                                 # Two vectors to define the mirror plane
                                 vector1=self.position.Vz,
                                 vector2=self.position.Vx,
                                 mesh_deflection=0.0001,
                                 color='Blue')




    #Fuselage mounted case
    elif wing_mount == False:
        @Part
        def engine(self):
            return Engine(position=translate(self.position.rotate90('y'),
                                            'x', -1*self.z_pos_engine_fus,
                                            'y', -1*self.y_pos_engine_fus,
                                            'z', self.x_pos_engine_fus,)
                                            )  # circles are in XY plane, thus need rotation

        @Part
        def h_tail(self):
            return Wing(position=translate(self.position, 'x',43., 'y', 0.1, 'z', 5.8),
                        w_semi_span=4.5,
                        dihedral=0.5,
                        w_c_root=2.5,
                        w_c_tip =1.24,
                        sweep_TE = 15
                        )


    # @Part
    # def mirrored_engine(self):
    #     return MirroredShape(shape_in=self.engine,
    #                          reference_point=self.position,
    #                          # Two vectors to define the mirror plane
    #                          vector1=self.position.Vz,
    #                          vector2=self.position.Vx,
    #                          mesh_deflection=0.0001,
    #                          )

    @Part
    def mirrored_h_tail(self):
        return MirroredShape(shape_in=self.h_tail,
                             reference_point=self.position,
                             # Two vectors to define the mirror plane
                             vector1=self.position.Vz,
                             vector2=self.position.Vx,
                             mesh_deflection=0.0001,
                             )


if __name__ == '__main__':
    from parapy.gui import display
    obj = Assembly()
    display(obj)


