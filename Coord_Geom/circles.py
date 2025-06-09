import math
from Coord_Geom.points import Point
from Coord_Geom.lines import Line

class Circle:
    def __init__(self, center: Point, radius: float):
        self.center = center
        self.radius = radius

    def diameter(self):
        return 2 * self.radius

    def equation(self):
        h, k = self.center.x, self.center.y
        r = self.radius
        return f"(x - {h})² + (y - {k})² = {r**2}"

    def circumference(self):
        return 2 * math.pi * self.radius

    def area(self):
        return math.pi * self.radius ** 2

    def contains_point(self, p: Point):
        distance = math.hypot(self.center.x - p.x, self.center.y - p.y)
        if distance < self.radius:
            return "Inside"
        elif distance == self.radius:
            return "On"
        else:
            return "Outside"

    def distance_from_point(self, p: Point):
        return math.hypot(self.center.x - p.x, self.center.y - p.y)

    def tangent_from_point(self, p: Point):
        status = self.contains_point(p)

        if status == "Inside":
            raise ValueError("No tangent exists — point lies inside the circle.")
        if status == "On":
            # Single tangent at that point: perpendicular to radius
            line = Line(self.center, p)
            m = line.perpendicular_slope()
            c = p.y - m * p.x
            return [(m, c)]
        else:  # Outside the circle
            # Two tangents exist — return slopes of both tangents
            d = self.distance_from_point(p)
            r = self.radius
            l = math.sqrt(d ** 2 - r ** 2)

            # Vector from center to point
            dx = p.x - self.center.x
            dy = p.y - self.center.y

            # Unit direction vector from center to point
            ux = dx / d
            uy = dy / d

            # Rotate vector by ±θ = arcsin(r / d) to get directions of tangents
            theta = math.asin(r / d)

            tangents = []
            for angle in [theta, -theta]:
                cos_a = math.cos(angle)
                sin_a = math.sin(angle)
                tx = ux * cos_a - uy * sin_a
                ty = ux * sin_a + uy * cos_a

                # Tangent direction from external point
                m = ty / tx if tx != 0 else float('inf')
                c = p.y - m * p.x if m != float('inf') else None
                tangents.append((m, c))

            return tangents  # Two tangents (slope, intercept)

    def point_on_circumference(self, angle_deg):
        angle_rad = math.radians(angle_deg)
        x = self.center.x + self.radius * math.cos(angle_rad)
        y = self.center.y + self.radius * math.sin(angle_rad)
        return x, y

    def intersects_line(self, line1: Line):
        x = line1.distance_from_point(self.center)
        if x < self.radius:
            return True
        else:
            return False

    def intersects_circle(self, other: 'Circle'):
        d = self.distance_from_point(other.center)
        return abs(self.radius - other.radius) <= d <= (self.radius + other.radius)

    def is_tangent_to(self, other: 'Circle'):
        d = self.distance_from_point(other.center)
        return d == abs(self.radius - other.radius) or d == (self.radius + other.radius)

    def translate(self, dx: float, dy: float):
        self.center.x += dx
        self.center.y += dy

    def arc_length(self, angle_deg):
        return (angle_deg / 360) * self.circumference()

    def sector_area(self, angle_deg):
        return (angle_deg / 360) * self.area()

    def chord_length(self, angle_deg):
        angle_rad = math.radians(angle_deg)
        return 2 * self.radius * math.sin(angle_rad / 2)

    def mirror_point(self, p: Point):
        dx = self.center.x - p.x
        dy = self.center.y - p.y
        return Point(self.center.x + dx, self.center.y + dy)

