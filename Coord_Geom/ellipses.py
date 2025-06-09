import math
from Coord_Geom.points import Point

class Ellipse:
    def __init__(self, a, b, h=0, k=0, orientation='h'):
        self.a = a  # semi-major axis
        self.b = b  # semi-minor axis
        self.h = h  # center x
        self.k = k  # center y
        self.orientation = orientation.lower()

    def equation(self):
        h, k = self.h, self.k
        return f"((x - {h})² / {self.a**2}) + ((y - {k})² / {self.b**2}) = 1"

    def center(self):
        return self.h, self.k

    def eccentricity(self):
        return math.sqrt(1 - (self.b ** 2) / (self.a ** 2))

    def foci(self):
        c = math.sqrt(abs(self.a ** 2 - self.b ** 2))
        if self.orientation == 'h':
            return (self.h - c, self.k), Point(self.h + c, self.k)
        else:
            return (self.h, self.k - c), Point(self.h, self.k + c)

    def vertices(self):
        if self.orientation == 'h':
            return (self.h - self.a, self.k), Point(self.h + self.a, self.k)
        else:
            return (self.h, self.k - self.a), Point(self.h, self.k + self.a)

    def co_vertices(self):
        if self.orientation == 'h':
            return (self.h, self.k - self.b), Point(self.h, self.k + self.b)
        else:
            return (self.h - self.b, self.k), Point(self.h + self.b, self.k)

    def area(self):
        return math.pi * self.a * self.b

    def perimeter_approx(self):
        a, b = self.a, self.b
        return math.pi * (3 * (a + b) - math.sqrt((3 * a + b) * (a + 3 * b)))

    def is_point_on_ellipse(self, p):
        x = p.x - self.h
        y = p.y - self.k
        if self.orientation == 'h':
            return math.isclose((x ** 2 / self.a ** 2) + (y ** 2 / self.b ** 2), 1, abs_tol=1e-9)
        else:
            return math.isclose((x ** 2 / self.b ** 2) + (y ** 2 / self.a ** 2), 1, abs_tol=1e-9)

    def get_y_given_x(self, x):
        x_shifted = x - self.h
        if self.orientation == 'h':
            inside = 1 - (x_shifted ** 2) / (self.a ** 2)
            if inside < 0:
                return None  # x is outside the ellipse
            y_val = self.b * math.sqrt(inside)
            return self.k + y_val, self.k - y_val
        else:
            inside = (self.a ** 2) * (1 - ((x_shifted ** 2) / (self.b ** 2)))
            if inside < 0:
                return None
            y_val = math.sqrt(inside)
            return self.k + y_val, self.k - y_val

    def get_x_given_y(self, y):
        y_shifted = y - self.k
        if self.orientation == 'v':
            inside = 1 - (y_shifted ** 2) / (self.a ** 2)
            if inside < 0:
                return None
            x_val = self.b * math.sqrt(inside)
            return self.h + x_val, self.h - x_val
        else:
            inside = (self.a ** 2) * (1 - ((y_shifted ** 2) / (self.b ** 2)))
            if inside < 0:
                return None
            x_val = math.sqrt(inside)
            return self.h + x_val, self.h - x_val

    def tangent_slope_at_point(self, p: Point):
        x = p.x - self.h
        y = p.y - self.k
        if self.orientation == 'h':
            denominator = self.a ** 2 * y
            if denominator == 0:
                return float('inf')
            return -(self.b ** 2 * x) / denominator
        else:
            denominator = self.b ** 2 * x
            if denominator == 0:
                return float('inf')
            return -(self.a ** 2 * y) / denominator

    def tangent_line_equation(self, p: Point):
        dx = p.x - self.h
        dy = p.y - self.k

        if self.orientation == 'h':
            denominator = self.a ** 2 * dy
            if denominator == 0:
                return f"x = {p.x}"  # vertical tangent
            slope = -(self.b ** 2 * dx) / denominator
        else:
            denominator = self.b ** 2 * dx
            if denominator == 0:
                return f"y = {p.y}"  # horizontal tangent
            slope = -(self.a ** 2 * dy) / denominator

        intercept = p.y - slope * p.x
        return f"y = {slope}x + {intercept}"

    def normal_slope_at_point(self, p: Point):
        dx = p.x - self.h
        dy = p.y - self.k

        if self.orientation == 'h':
            denominator = self.b ** 2 * dx
            if denominator == 0:
                return float('inf')  # vertical normal line
            return (self.a ** 2 * dy) / denominator
        else:
            denominator = self.a ** 2 * dy
            if denominator == 0:
                return float('inf')  # horizontal normal line
            return (self.b ** 2 * dx) / denominator

    def normal_line_equation(self, p: Point):
        m = self.normal_slope_at_point(p)
        if m == float('inf'):
            return f"x = {p.x}"
        else:
            c = p.y - m * p.x
            return f"y = {m}x + {c}"

    def is_inside(self, p):
        x = p.x - self.h
        y = p.y - self.k
        if self.orientation == 'h':
            return (x ** 2) / (self.a ** 2) + (y ** 2) / (self.b ** 2) < 1
        else:
            return (x ** 2) / (self.b ** 2) + (y ** 2) / (self.a ** 2) < 1

    def reflect_point_across_center(self, p):
        dx = self.h - p.x
        dy = self.k - p.y
        return self.h + dx, self.k + dy

    def axis_of_symmetry(self):
        if self.orientation == 'h':
            return f"y = {self.k}"
        else:
            return f"x = {self.h}"

    def parametric_point(self, t_degrees):
        t = math.radians(t_degrees)  # Convert degrees to radians
        x = self.h + self.a * math.cos(t)
        y = self.k + self.b * math.sin(t)
        return x, y