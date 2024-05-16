    #
    # @Part
    # def lower_channel(self):
    #     return ChannelX(
    #         ch_radius=0.2,
    #         position=translate(
    #             self.position,
    #             "x",
    #             5,
    #             "y",
    #             self.channels_ypostion,
    #             "z",
    #             self.lower_channel_zposition,
    #         ),
    #         color="Blue",
    #     )
    #
    # @Part
    # def lower_channel2(self):
    #     return MirroredShape(
    #         shape_in=self.lower_channel,
    #         reference_point=self.position,
    #         # Two vectors to define the mirror plane
    #         vector1=self.position.Vz,
    #         vector2=self.position.Vx,
    #         mesh_deflection=0.0001,
    #         color="Blue",
    #     )
    #
    # @Part
    # def connectorY1(self):
    #     return ChannelY(
    #         ch_length=self.channels_ypostion * 2,
    #         ch_radius=0.1,
    #         position=translate(
    #             self.position,
    #             "x",
    #             7,
    #             "y",
    #             -1 * self.channels_ypostion,
    #             "z",
    #             self.lower_channel_zposition,
    #             ),
    #         color="Blue",
    #     )
    #
    # @Part
    # def connectorY2(self):
    #     return ChannelY(
    #         ch_length=2,
    #         ch_radius=0.04,
    #         position=translate(
    #             self.position,
    #             "x",
    #             40,
    #             "y",
    #             -1 * self.channels_ypostion,
    #             "z",
    #             self.upper_channel_zposition,
    #             ),
    #         color="Blue",
    #     )
