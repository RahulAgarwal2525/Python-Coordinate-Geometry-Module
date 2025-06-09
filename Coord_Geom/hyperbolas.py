import math
from scipy.optimize import minimize
import numpy as np
from Coord_Geom.points import Point

class Hyperbola:
    def __init__(self, a, b, h=0, k=0, orientation="h"):
        self.a = a
        self.b = b
        self.h = h
        self.k = k
        self.orientation = orientation.lower()

    def eccentricity(self):
        return math.sqrt(1 + (self.b ** 2) / (self.a ** 2))

    def foci(self):
        c = math.sqrt(self.a ** 2 + self.b ** 2)
        if self.orientation == "h":
            return (self.h + c, self.k), Point(self.h - c, self.k)
        else:
            return (self.h, self.k + c), Point(self.h, self.k - c)

    def vertices(self):
        if self.orientation == "h":
            return (self.h + self.a, self.k), Point(self.h - self.a, self.k)
        else:
            return (self.h, self.k + self.a), Point(self.h, self.k - self.a)

    def evaluate(self, val):
        # For horizontal: val = x → return ±y
        # For vertical: val = y → return ±x
        if self.orientation == 'h':
            dx = val - self.h
            term = (dx ** 2) / (self.a ** 2) - 1
            if term < 0:
                raise ValueError("Input outside real domain (no real y exists).")
            dy = self.b * math.sqrt(term)
            return self.k + dy, self.k - dy  # two y-values
        else:
            dy = val - self.k
            term = (dy ** 2) / (self.a ** 2) - 1
            if term < 0:
                raise ValueError("Input outside real domain (no real x exists).")
            dx = self.b * math.sqrt(term)
            return self.h + dx, self.h - dx  # two x-values

    def latus_rectum_length(self):
        return (2 * self.b ** 2) / self.a

    def latus_rectum_endpoints(self):
        c = math.sqrt(self.a ** 2 + self.b ** 2)
        l = self.latus_rectum_length() / 2

        if self.orientation == "h":
            foci = [(self.h + c, self.k), (self.h - c, self.k)]
            return [
                (Point(f[0], f[1] + l), Point(f[0], f[1] - l)) for f in foci
            ]
        else:
            foci = [(self.h, self.k + c), (self.h, self.k - c)]
            return [
                (Point(f[0] + l, f[1]), Point(f[0] - l, f[1])) for f in foci
            ]

    def transverse_axis_length(self):
        return 2 * self.a

    def conjugate_axis_length(self):
        return 2 * self.b

    def asymptotes(self):
        if self.orientation == "h":
            slope = self.b / self.a
        else:
            slope = self.a / self.b

        return (
            f"y = {self.k} + {slope}(x - {self.h})",
            f"y = {self.k} - {slope}(x - {self.h})"
        )

    def angle_between_asymptotes(self, degrees=True):
        if self.orientation == "h":
            ratio = self.b / self.a
        else:
            ratio = self.a / self.b

        angle_rad = 2 * math.atan(ratio)
        return math.degrees(angle_rad) if degrees else angle_rad

    def is_on_hyperbola(self, p: Point):
        x = p.x - self.h
        y = p.y - self.k
        if self.orientation == "h":
            lhs = (x ** 2) / (self.a ** 2) - (y ** 2) / (self.b ** 2)
        else:
            lhs = (y ** 2) / (self.a ** 2) - (x ** 2) / (self.b ** 2)
        return math.isclose(lhs, 1, rel_tol=1e-9)

    def distance_to_hyperbola(self, p):
        def objective(t):
            point_on_hyperbola = self.parametric_point(math.degrees(t[0]))
            return math.hypot(point_on_hyperbola.x - p.x, point_on_hyperbola.y - p.y)

        result = minimize(objective, np.array([0.0]))
        min_t = math.degrees(result.x[0])
        nearest_point = self.parametric_point(min_t)
        min_distance = objective(result.x)

        return min_distance, nearest_point

    def distance_to_focus(self, p: Point):
        f1, f2 = self.foci()
        d1 = math.hypot(p.x - f1.x, p.y - f1.y)
        d2 = math.hypot(p.x - f2.x, p.y - f2.y)
        return d1, d2

    def parametric_point(self, t_degrees):
        t = math.radians(t_degrees)
        sec_t = 1 / math.cos(t)
        tan_t = math.tan(t)

        if self.orientation == "h":
            x = self.h + self.a * sec_t
            y = self.k + self.b * tan_t
        else:
            x = self.h + self.b * tan_t
            y = self.k + self.a * sec_t

        return Point(x, y)

    def conjugate_hyperbola(self):
        if self.orientation == "h":
            return f"(y - {self.k})^2/{self.b ** 2} - (x - {self.h})^2/{self.a ** 2} = 1"
        else:
            return f"(x - {self.h})^2/{self.b ** 2} - (y - {self.k})^2/{self.a ** 2} = 1"

    def tangent_slope_at_point(self, p):
        dx = p.x - self.h
        dy = p.y - self.k
        if self.orientation == "h":
            if dx == 0:
                return float('inf')
            return (self.b ** 2 * dy) / (self.a ** 2 * dx)
        else:
            if dy == 0:
                return float('inf')
            return (self.a ** 2 * dx) / (self.b ** 2 * dy)

    def tangent_line_equation(self, p):
        m = self.tangent_slope_at_point(p)
        if m == float('inf'):
            return f"x = {p.x}"
        c = p.y - m * p.x
        return f"y = {m}x + {c}"

    def normal_slope_at_point(self, p):
        m = self.tangent_slope_at_point(p)
        if m == 0:
            return float('inf')
        if m == float('inf'):
            return 0
        return -1 / m

    def normal_line_equation(self, p):
        m = self.normal_slope_at_point(p)
        if m == float('inf'):
            return f"x = {p.x}"
        c = p.y - m * p.x
        return f"y = {m}x + {c}"

    def conic_form_equation(self):
        if self.orientation == "h":
            return f"(x - {self.h})²/{self.a ** 2} - (y - {self.k})²/{self.b ** 2} = 1"
        else:
            return f"(y - {self.k})²/{self.a ** 2} - (x - {self.h})²/{self.b ** 2} = 1"

    def intersects_with_line(self, line, samples=1000):
        intersections = []

        for i in range(samples + 1):
            t = i / samples
            x = line.p1.x + t * (line.p2.x - line.p1.x)
            y = line.p1.y + t * (line.p2.y - line.p1.y)

            dx = x - self.h
            dy = y - self.k

            if self.orientation == "horizontal":
                val = (dx ** 2) / self.a ** 2 - (dy ** 2) / self.b ** 2
            else:
                val = (dy ** 2) / self.a ** 2 - (dx ** 2) / self.b ** 2

            if math.isclose(val, 1, rel_tol=1e-2):  # Some tolerance
                intersections.append(Point(x, y))

        return intersections

    def reflect_point_across_hyperbola(self, p):
        _, nearest = self.distance_to_hyperbola(p)
        m = self.normal_slope_at_point(nearest)

        if m == float('inf'):
            x_reflected = 2 * nearest.x - p.x
            y_reflected = p.y
        elif m == 0:
            x_reflected = p.x
            y_reflected = 2 * nearest.y - p.y
        else:
            # Equation of the normal line: y = m*x + c
            c = nearest.y - m * nearest.x
            d = (p.x + (p.y - c) * m) / (1 + m ** 2)
            x_reflected = 2 * d - p.x
            y_reflected = 2 * d * m - p.y + 2 * c

        return x_reflected, y_reflected
