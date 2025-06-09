import math
from Coord_Geom.points import Point
from Coord_Geom.lines import Line

class Triangle:
    def __init__(self, v1 : Point, v2 : Point, v3 : Point):

        if Point.collinear(v1, v2, v3):
            print("Points are collinear, hence triangle is not possible")
            return
        self.a = v1
        self.b = v2
        self.c = v3

    def side_lengths(self):
        ab = math.hypot(self.a.x - self.b.x, self.a.y - self.b.y)
        bc = math.hypot(self.b.x - self.c.x, self.b.y - self.c.y)
        ca = math.hypot(self.c.x - self.a.x, self.c.y - self.a.y)
        return ab, bc, ca

    def angles(self):
        a, b, c = self.side_lengths()
        ang_a = math.degrees(math.acos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c)))
        ang_b = math.degrees(math.acos((a ** 2 + c ** 2 - b ** 2) / (2 * a * c)))
        ang_c = 180.0 - ang_a - ang_b
        return ang_a, ang_b, ang_c

    def perimeter(self):
        ab, bc, ca = self.side_lengths()
        return ab + bc + ca

    def area(self):
        ab, bc, ca = self.side_lengths()
        s = (ab + bc + ca) / 2
        return math.sqrt(s * (s - ab) * (s - bc) * (s - ca))

    def heights(self):
        area = self.area()
        a, b, c = self.side_lengths()
        h_a = (2 * area) / a
        h_b = (2 * area) / b
        h_c = (2 * area) / c
        return h_a, h_b, h_c

    def medians(self):
        a, b, c = self.side_lengths()
        m_a = 0.5 * math.sqrt(2 * b ** 2 + 2 * c ** 2 - a ** 2)
        m_b = 0.5 * math.sqrt(2 * a ** 2 + 2 * c ** 2 - b ** 2)
        m_c = 0.5 * math.sqrt(2 * a ** 2 + 2 * b ** 2 - c ** 2)
        return m_a, m_b, m_c

    def type_by_sides(self):
        ab, bc, ca = self.side_lengths()
        if math.isclose(ab, bc) and math.isclose(bc, ca):
            print("Equilateral triangle")
        elif ab == bc != ca or bc == ca != ab or ca == ab != bc:
            print("Isosceles triangle")
        else:
            print("Scalene triangle")

    def type_by_angles(self):
        ang_a, ang_b, ang_c = self.angles()
        max_angle = max(ang_a, ang_b, ang_c)

        if math.isclose(max_angle, 90.0, abs_tol=1e-5):
            return "Right"
        elif max_angle > 90.0:
            return "Obtuse"
        else:
            return "Acute"

    def centroid(self):
        return (self.a.x + self.b.x + self.c.x)/3 , (self.a.y + self.b.y + self.c.y)/3

    def incenter(self):
        a, b, c = self.side_lengths()

        px = (a * self.a.x + b * self.b.x + c * self.c.x) / (a + b + c)
        py = (a * self.a.y + b * self.b.y + c * self.c.y) / (a + b + c)

        return px, py

    def inradius(self):
        s = self.perimeter() / 2
        return self.area() / s

    def circumcenter(self):
        l1 = Line(self.a, self.b)
        l2 = Line(self.b, self.c)

        m1, c1 = l1.perpendicular_bisector()
        m2, c2 = l2.perpendicular_bisector()

        if m1 == float('inf'):
            x = c1.x
            y = m2 * (x - c2.x) + c2.y
        elif m2 == float('inf'):
            x = c2.x
            y = m1 * (x - c1.x) + c1.y
        else:
            x = (m1 * c1.x - m2 * c2.x + c2.y - c1.y) / (m1 - m2)
            y = m1 * (x - c1.x) + c1.y

        return x, y

    def circumradius(self):
        a, b, c = self.side_lengths()
        return (a * b * c) / (4 * self.area())

    def orthocenter(self):
        s1 = Line(self.a, self.b).perpendicular_slope()
        s2 = Line(self.b, self.c).perpendicular_slope()
        p1 = self.c
        p2 = self.a

        if s1 == float('inf'):
            x = p1.x
            y = s2 * (x - p2.x) + p2.y
        elif s2 == float('inf'):
            x = p2.x
            y = s1 * (x - p1.x) + p1.y
        else:
            x = (s1 * p1.x - s2 * p2.x + p2.y - p1.y) / (s1 - s2)
            y = s1 * (x - p1.x) + p1.y

        return x, y

    def contains_point(self, p):
        d1 = Point.determinant(p, self.a, self.b)
        d2 = Point.determinant(p, self.b, self.c)
        d3 = Point.determinant(p, self.c, self.a)

        has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
        has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)

        # If signs differ, point is outside
        return not (has_neg and has_pos)