import math

from Coord_Geom.lines import Line
from Coord_Geom.points import Point

class Parabola:
    def __init__(self, a: float, b: float, c: float, orientation='v'):
        self.a = a
        self.b = b
        self.c = c
        self.orientation = orientation.lower()

    def evaluate(self, x):
        return self.a * x ** 2 + self.b * x + self.c

    def vertex(self):
        if self.orientation == 'v':
            x = -self.b / (2 * self.a)
            y = self.evaluate(x)
        else:
            y = -self.b / (2 * self.a)
            x = self.evaluate(y)
        return x, y

    def focus(self):
        vx, vy = self.vertex()
        if self.orientation == 'v':
            return Point(vx, vy + 1 / (4 * self.a))
        else:
            return Point(vx + 1 / (4 * self.a), vy)

    def focal_length(self):
        return 1 / (4 * abs(self.a))

    def directrix(self):
        vx, vy = self.vertex()
        if self.orientation == 'v':
            return vy - 1 / (4 * self.a)
        else:
            return vx - 1 / (4 * self.a)

    def focus_directrix_form(self):
        vx, vy = self.vertex()
        if self.orientation == 'v':
            return f"(x - {vx})² = {4 * self.a}(y - {vy})"
        else:
            return f"(y - {vy})² = {4 * self.a}(x - {vx})"

    def focus_directrix_distance_property(self, p: Point):
        if not self.is_point_on_parabola(p):
            return False

        focus = self.focus()
        d1 = math.hypot(p.x - focus.x, p.y - focus.y)

        if self.orientation == 'v':
            d2 = abs(p.y - self.directrix())
        else:
            d2 = abs(p.x - self.directrix())

        return math.isclose(d1, d2, rel_tol=1e-9)

    def axis_of_symmetry(self):
        return -self.b / (2 * self.a)

    def direction(self):
        if self.orientation == 'v':
            return "up" if self.a > 0 else "down"
        else:
            return "right" if self.a > 0 else "left"

    def discriminant(self):
        return self.b ** 2 - 4 * self.a * self.c

    def latus_rectum_length(self):
        return 1 / abs(self.a)

    def roots(self):
        discriminant = self.discriminant()
        if discriminant > 0:
            r1 = (-self.b + math.sqrt(discriminant)) / (2 * self.a)
            r2 = (-self.b - math.sqrt(discriminant)) / (2 * self.a)
            return r1, r2
        elif discriminant == 0:
            r = -self.b / (2 * self.a)
            return r, r
        else:
            real = -self.b / (2 * self.a)
            imag = math.sqrt(-discriminant) / (2 * self.a)
            return complex(real, imag), complex(real, -imag)

    def is_point_on_parabola(self, point):
        if self.orientation == 'v':
            return math.isclose(point.y, self.evaluate(point.x), abs_tol=1e-9)
        else:
            return math.isclose(point.x, self.evaluate(point.y), abs_tol=1e-9)

    def tangent_slope_at_point(self, p):
        if not self.is_point_on_parabola(p):
            raise ValueError("Point not on the parabola")

        if self.orientation == 'v':
            return 2 * self.a * p.x + self.b
        else:
            return 1 / (2 * self.a * p.y + self.b) if (2 * self.a * p.y + self.b) != 0 else float('inf')

    def tangent_line_at_point(self, p):
        m = self.tangent_slope_at_point(p)
        c = p.y - m * p.x
        return f"y = {m}x + {c}"

    def normal_line_at_point(self, p):
        m = self.tangent_slope_at_point(p)
        if m == 0:
            return f"x = {p.x}"
        elif math.isinf(m):
            return f"y = {p.y}"
        else:
            m_perp = -1 / m
            c = p.y - m_perp * p.x
            return f"y = {m_perp}x + {c}"

    def mirror_point_across_axis(self, p):
        if self.orientation == 'v':
            axis_x = self.axis_of_symmetry()
            mirrored_x = 2 * axis_x - p.x
            return Point(mirrored_x, p.y)
        else:
            axis_y = self.axis_of_symmetry()  # which is y = -b/2a for horizontal
            mirrored_y = 2 * axis_y - p.y
            return Point(p.x, mirrored_y)

    def parametric_point(self, t_degrees):
        t = math.radians(t_degrees)
        if self.orientation == 'v':
            x = math.degrees(t)
            y = self.evaluate(x)
        else:
            y = math.degrees(t)
            x = self.evaluate(y)
        return Point(x, y)

    def intersection_with_line(self, line : Line):
        m, c = line.equation()  # y = mx + c

        points = []

        if self.orientation == 'v':
            # Parabola: y = ax^2 + bx + c
            # Line: y = mx + c  → ax^2 + bx + c = mx + c
            # → ax^2 + (b - m)x + (c - c) = 0
            A = self.a
            B = self.b - m
            C = self.c - c

            D = B ** 2 - 4 * A * C

            if D < 0:
                return []  # No real intersection
            elif math.isclose(D, 0):
                x = -B / (2 * A)
                y = line.evaluate(x)
                points.append(Point(x, y))
            else:
                sqrt_D = math.sqrt(D)
                x1 = (-B + sqrt_D) / (2 * A)
                x2 = (-B - sqrt_D) / (2 * A)
                points.append(Point(x1, line.evaluate(x1)))
                points.append(Point(x2, line.evaluate(x2)))

        else:  # orientation == 'h'
            # Parabola: x = ay^2 + by + c
            # Line: y = mx + c → x = a y^2 + b y + c = (y - c)/m
            # Multiply both sides by m: m x = a y^2 + b y + c → x = (a y^2 + b y + c)/m

            # Invert line: x = (y - c) / m
            if m == 0:
                return []  # horizontal line can't intersect horizontal parabola (constant y)

            # Sub x = (y - c) / m into x = ay^2 + by + c
            # ay^2 + by + c = (y - c)/m → ay^2 + (b - 1/m)y + (c + c/m) = 0
            A = self.a
            B = self.b - 1 / m
            C = self.c - c / m

            D = B ** 2 - 4 * A * C

            if D < 0:
                return []
            elif math.isclose(D, 0):
                y = -B / (2 * A)
                x = self.evaluate(y)
                points.append(Point(x, y))
            else:
                sqrt_D = math.sqrt(D)
                y1 = (-B + sqrt_D) / (2 * A)
                y2 = (-B - sqrt_D) / (2 * A)
                points.append(Point(line.evaluate_y(y1), y1))
                points.append(Point(line.evaluate_y(y2), y2))

        return points
