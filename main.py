from parapy.geom import *
from parapy.core import *
from parapy.core.widgets import Dropdown
from parapy.exchange import STEPWriter

from assembly.config_t_tail import FuselageMounted
from assembly.config_conv import WingMounted

from fuselage.aircraft_body import AircraftBody

from wiring.EWIS import EWIS

from rotorburst_volumes.evaluate_risk_zones import RiskVolumeAnalysis

# import matlab.engine
# MATLAB_ENGINE = matlab.engine.start_matlab()


class MainAssembly(GeomBase):
    # the configuration of the aircraft: wing mounted or fuselage mounted engines
    aircraft_config = Input(
        True,
        widget=Dropdown([True, False], labels=["Wing Mounted", "Fuselage Mounted"]),
    )

    # the wiring configuriation of the fuselage: four channels or three channels along the length of the fuselage
    wiring_config = Input(
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

    @Part
    def structures(self):
        """
        The fuselage, wing and vertical tail models
        :return: GeomBase.AircraftBody object
        """
        return AircraftBody()

    @Part
    def wiring_configuration(self):
        """
        The configuration of the wiring based on [wiring_config]
        :return: EWIS object with parts for wing channels, fuselage channels and empennage channels
        """
        return EWIS(
            configuration=self.wiring_config,
            wing=self.structures.right_wing,
            h_tail=self.configuration.right_h_tail,
            v_tail=self.structures.v_tail,
            color="blue",
        )

    @Attribute
    def channelShapes(self):
        """
        Creates a list of all the shapes in [self.wiring] which can be used to determine intersection with a risk volume
        :return: list
        """
        channelShapes = []
        for child in self.wiring_configuration.children:
            for part in child.parts:
                if len(part.parts) == 0:
                    if part.TOPODIM == 3:  # only work with solids
                        channelShapes.append(part)
                else:  # nested parts
                    part_list = part.parts
                    for nested_part in part_list:
                        if nested_part.TOPODIM == 3:  # only work with solids
                            channelShapes.append(nested_part)
        return channelShapes

    @Part
    def pra_rotor_burst(self):
        """
        Internal analysis module to determine for which release angles per engine, per rotation direction,
        per engine stage- which channels are in the risk zone. The risk zones and channels that are hit
        can be visualised.
        :return: RiskVolumeAnalysis object with RiskVolume.LoftedSolid and GeomBase.FusedSolid as parts
        """
        return RiskVolumeAnalysis(pass_down="configuration",
                                  channel_shapes=self.channelShapes)

    # pathchanged = False
    # @Attribute
    # def make_table(self):
    #     if not self.pathchanged:
    #         # change matlab root directory to Q3D, so it can find the function
    #         MATLAB_ENGINE.cd(r'./matlab_files')
    #         self.pathchanged=True
    #
    #     return MATLAB_ENGINE.make_table()

    @action(label="Write to step file")
    def step_writer(self):
        """
        Module to write geometry to a .stp file
        :return: .stp file
        """
        return STEPWriter(
            nodes=[
                self.configuration.engines[0].nacelle.srf_nacelle,
                self.configuration.engines[0].shaft.stages_disks,
            ],
            filename="engine.step",
        )


if __name__ == "__main__":
    from parapy.gui import display

    obj = MainAssembly()
    display(obj)
