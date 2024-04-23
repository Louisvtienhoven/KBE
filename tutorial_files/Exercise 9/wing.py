from parapy.core import *

class Wing(Base):
    chord_root = input(3.0)
    chord_tip = input(2)
    span = input(10)

    @Attribute
    def area(self):
        return (self.chord_root + self.chord_tip) * 0.5 * self.span

    @Attribute
    def ar(self):
        """Aspect ratio"""
        return self.span ** 2 / self.area

    @Attribute
    def taper(self):
        """Calculates the taper by diving tip chord by root chord"""
        return self.chord_tip / self.chord_root
