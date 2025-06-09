import math

class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def quadrant(self):
        if self.x == 0 or self.y == 0:
            print("Axis")
        elif self.x > 0 and self.y > 0:
            print("Quadrant I")
        elif self.x < 0 and self.y > 0:
            print("Quadrant II")
        elif self.x < 0 and self.y < 0:
            print("Quadrant III")
        else:
            print("Quadrant IV")

    def distance_to(self, other):
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)

    def dist_origin(self):
        return math.sqrt((self.x - 0) ** 2 + (self.y - 0) ** 2)

    def midpoint(self, other):
        return Point((self.x + other.x)/2, (self.y + other.y)/2)

    def collinear(self, other, next):
        dx1 = self.x - other.x
        dx2 = self.x - next.x
        dy1 = self.y - other.y
        dy2 = self.y - next.y
        if dx1 == 0 and dx2 == 0:
            return True  # vertical line
        if dx1 == 0 or dx2 == 0:
            return False
        return (dy1 / dx1) == (dy2 / dx2)

    def reflect_x(self):
        return Point(self.x, -self.y)

    def reflect_y(self):
        return Point(-self.x, self.y)

    def reflect_o(self):
        return Point(-self.x, -self.y)

    def angle_with(self, other):
        """
        Returns the angle in degrees between this point and another,
        with respect to the origin (0, 0), treating points as vectors.
        """
        dot = self.x * other.x + self.y * other.y
        mag_self = math.sqrt(self.x**2 + self.y**2)
        mag_other = math.sqrt(other.x**2 + other.y**2)

        if mag_self == 0 or mag_other == 0:
            raise ValueError("Cannot compute angle with a zero vector.")

        cos_theta = dot / (mag_self * mag_other)

        # Clamp cos_theta to avoid math domain error due to floating-point
        cos_theta = max(-1.0, min(1.0, cos_theta))

        angle_rad = math.acos(cos_theta)
        angle_deg = math.degrees(angle_rad)
        return angle_deg

    def x_inclination(self):
        angle_rad = math.atan2(self.y, self.x)
        angle_deg = math.degrees(angle_rad)
        return angle_deg

    def y_inclination(self):
        angle_rad = math.atan2(-self.x, self.y)
        angle_deg = math.degrees(angle_rad)
        return angle_deg

    def determinant(self, other, next):
        return (other.x - self.x) * (next.y - self.y) - (next.x - self.x) * (other.y - self.y)

    def rotate(self, angle_deg, around_origin=True, center=None):
        angle_rad = math.radians(angle_deg)
        cos_a = math.cos(angle_rad)
        sin_a = math.sin(angle_rad)
        cx, cy = (0, 0)

        if not around_origin and center:
            cx, cy = center.x, center.y

        x_shifted = self.x - cx
        y_shifted = self.y - cy

        x_rot = x_shifted * cos_a - y_shifted * sin_a + cx
        y_rot = x_shifted * sin_a + y_shifted * cos_a + cy

        return Point(x_rot, y_rot)