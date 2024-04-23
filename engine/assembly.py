from parapy.geom import *
from parapy.core import *

from engine.engine_full import Engine
from engine.aircraft_body import AircraftBody
from wing import Wing




class Assembly(GeomBase):
    wing_mount = False

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
            return Engine(position=translate(self.position.rotate90('y','z'),
                                            'x',self.y_pos_engine_wing,
                                            'y',self.z_pos_engine_wing,
                                            'z',self.x_pos_engine_wing)
                                            )  # circles are in XY plane, thus need rotation
        @Part
        def h_tail(self):
            return Wing(position=translate(self.position, 'x',40.5, 'y', 1.3, 'z', 0),
                        w_semi_span=4.5,
                        dihedral=0.5,
                        w_c_root=3.31,
                        w_c_tip =1.24,
                        sweep_TE = 15
                        )


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
    #
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


