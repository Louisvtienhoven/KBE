from parapy.geom import *
from parapy.core import *
from parapy.core.widgets import Dropdown
from parapy.exchange import STEPWriter

from assembly.config_t_tail import FuselageMounted
from assembly.config_conv import WingMounted
from fuselage.aircraft_body import AircraftBody

from fuselage.EWIS import WingChannel4
from fuselage.EWISB import WingChannel3
from rotorburst_volumes.evaluate_risk_zones import RiskVolumeAnalysis

# import matlab.engine
# MATLAB_ENGINE = matlab.engine.start_matlab()


class MainAssembly(GeomBase):
    # the configuration of the aircraft: wing mounted or fuselage mounted engines
    aircraft_config = Input(
        True,
        widget=Dropdown([True, False], labels=["Wing Mounted", "Fuselage Mounted"]),
    )

    wiringConfig = Input(
        True,
        widget=Dropdown([True, False], labels=["3 Channel Option", "4 Channel Option"]),
    )

    @Part
    def configuration(self):
        """
        The configuration of the aircraft based on [aircraft_config]
        :return: WingMounted or FuselageMounted objects with corresponding empenage layout and engine placement
        """
        return DynamicType(
            type=WingMounted if self.aircraft_config == True else FuselageMounted
        )

    # @Part
    # def wiring(self):
    #     """
    #     The layout of the channels in both the wing and fuselage
    #     :return: GeomBase.Ewis object
    #     """
    #     return WingChannel(
    #         front_spar_root_pos=self.structures.right_wing.front_spar_root_location,
    #         aft_spar_root_pos=self.structures.right_wing.aft_spar_root_location,
    #         front_spar_tip_pos=self.structures.right_wing.front_spar_tip_location,
    #         aft_spar_tip_pos=self.structures.right_wing.aft_spar_tip_location,
    #         color="blue",
    #     )

    @Part
    def wiring_configuration(self):
        return DynamicType(type=WingChannel3 if self.wiringConfig == True else WingChannel4)

    @Part
    def structures(self):
        """
        The fuselage, wing and vertical tail models
        :return: GeomBase.AircraftBody object
        """
        return AircraftBody()

    @Attribute
    def channel_shapes(self):
        """
        Creates a list of all the shapes in [self.wiring] which can be used to determine intersection with a risk volume
        :return: list
        """
        channelShapes = []
        for part in self.wiring.children:
            if part.TOPOLEVEL == 2:  # Only work with Solids
                channelShapes.append(part)
        return channelShapes

    @Part
    def pra_rotor_burst(self):
        return RiskVolumeAnalysis(
            pass_down="configuration, aircraft_config, channel_shapes"
        )

    # pathchanged = False
    # @Attribute
    # def make_table(self):
    #     if not self.pathchanged:
    #         # change matlab root directory to Q3D, so it can find the function
    #         MATLAB_ENGINE.cd(r'./matlab_files')
    #         self.pathchanged=True
    #
    #     return MATLAB_ENGINE.make_table()

    @Part
    def step_writer(self):
        return STEPWriter(
            nodes=[
                self.configuration.engine[0].nacelle.srf_nacelle,
                self.configuration.engine[0].shaft.stages_disks,
            ],
            filename="engine.step",
        )


if __name__ == "__main__":
    from parapy.gui import display

    obj = MainAssembly()
    display(obj)