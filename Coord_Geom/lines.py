import math
from Coord_Geom.points import Point

class Line:
    def __init__(self, p1: Point, p2: Point):
        self.p1 = p1
        self.p2 = p2

    def length(self):
        return math.hypot(self.p2.x - self.p1.x, self.p2.y - self.p1.y)

    def midpoint(self):
        return Point((self.p1.x + self.p2.x)/2, (self.p1.y + self.p2.y)/2)

    def slope(self):
        dx = self.p2.x - self.p1.x
        dy = self.p2.y - self.p1.y
        if dx == 0:
            return float('inf') if dy >= 0 else float('-inf')
        return dy / dx

    def equation(self):
        m = self.slope()
        c = self.p1.y - m * self.p1.x
        return m, c  # y = mx + c

    def evaluate(self, x):
        m, c = self.equation()
        if m == float('inf') or m == float('-inf'):
            raise ValueError("Cannot evaluate vertical line at x = {}".format(x))
        return m * x + c

    def evaluate_y(self, y):
        m, c = self.equation()
        if m == 0:
            raise ValueError("Cannot evaluate horizontal line at y = {}".format(y))
        return (y - c) / m

    def perpendicular_slope(self):
        m = self.slope()
        if m == 0:
            return float('inf')  # Perpendicular to horizontal line is vertical
        elif m == float('inf') or m == float('-inf'):
            return 0.0  # Perpendicular to vertical line is horizontal
        else:
            return -1 / m

    def perpendicular_bisector(self):
        m = self.perpendicular_slope()
        p = self.midpoint()
        return m, p

    def is_perpendicular(self, other):
        return math.isclose(self.slope() * other.slope(), -1.0, rel_tol=1e-9)

    def is_parallel(self, other):
        return math.isclose(self.slope(), other.slope(), rel_tol=1e-9)

    def point_on_line(self, point : Point):
        dx = self.p2.x - self.p1.x
        dy = self.p2.y - self.p1.y

        if dx == 0:
            # Vertical line: x must match
            return math.isclose(point.x, self.p1.x, rel_tol=1e-9)
        else:
            # Compute expected y using line equation
            m, c = self.equation()
            y_expected = m * point.x + c
            return math.isclose(point.y, y_expected, rel_tol=1e-9)

    def angle_with_x_axis(self):
        m = self.slope()

        if m == float('inf'):
            return 90.0
        elif m == float('-inf'):
            return -90.0

        angle_rad = math.atan(m)
        angle_deg = math.degrees(angle_rad)
        return angle_deg

    def distance_from_point(self, point: Point):
        x0, y0 = point.x, point.y
        x1, y1 = self.p1.x, self.p1.y
        x2, y2 = self.p2.x, self.p2.y

        numerator = abs((y2 - y1) * x0 - (x2 - x1) * y0 + x2 * y1 - y2 * x1)
        denominator = math.hypot(y2 - y1, x2 - x1)

        return numerator / denominator if denominator != 0 else 0.0

    def reflect_point(self, point: Point) -> Point:
        x1, y1 = self.p1.x, self.p1.y
        x2, y2 = self.p2.x, self.p2.y
        x0, y0 = point.x, point.y

        dx = x2 - x1
        dy = y2 - y1

        if dx == dy == 0:
            raise ValueError("Line must be defined by two distinct points.")

        # Calculate the reflection using vector projection
        a = dy
        b = -dx
        c = dx * y1 - dy * x1

        d = (a * x0 + b * y0 + c) / (a**2 + b**2)

        x_reflect = x0 - 2 * a * d
        y_reflect = y0 - 2 * b * d

        return Point(x_reflect, y_reflect)

    def altitude(self, a: Point):
        slope = self.perpendicular_slope()
        return slope, a

    def project_point(self, point: Point) -> Point:
        dx = self.p2.x - self.p1.x
        dy = self.p2.y - self.p1.y
        if dx == dy == 0:
            raise ValueError("Invalid line")

        # Vector from p1 to point
        px = point.x - self.p1.x
        py = point.y - self.p1.y

        # Projection scalar
        dot = dx * px + dy * py
        len_sq = dx ** 2 + dy ** 2
        scale = dot / len_sq

        proj_x = self.p1.x + scale * dx
        proj_y = self.p1.y + scale * dy

        return Point(proj_x, proj_y)