"""
coord_geom - A Coordinate Geometry Toolkit
This package provides tools for:
- Point operations (distance, midpoint, etc.)
- Line calculations (slope, equations)
- Circle equations and visualizations
- Parabola and ellipse geometry
"""

# Import core classes/functions from submodules
from Coord_Geom.points import Point
from Coord_Geom.lines import Line
from Coord_Geom.triangles import Triangle
from Coord_Geom.circles import Circle
from Coord_Geom.parabolas import Parabola
from Coord_Geom.ellipses import Ellipse
from Coord_Geom.hyperbolas import Hyperbola
from .plot_utils import *

# (Optional) Set version
__version__ = "0.1.0"

