import os.path

_module_dir = os.path.dirname(__file__)
AIRFOIL_DIR = os.path.join(_module_dir, 'airfoil_library', '')

from .airfoil import Airfoil
from .movable import Movable
from .liftingsurface import LiftingSurface
from .fuselage import Fuselage
from .xfoil_analysis import XfoilAnalysis
from .aircraft import Aircraft

# ATTENTION! The order of the previous statements is important! For example, LiftingSurface cannot be imported before /
# Movable, because LiftingSurface uses Movable in one of its parts.
