import matplotlib.pyplot as plt
import math
from Coord_Geom.points import Point
from Coord_Geom.lines import Line
from Coord_Geom.triangles import Triangle
from Coord_Geom.circles import Circle
from Coord_Geom.parabolas import Parabola
from Coord_Geom.ellipses import Ellipse
from Coord_Geom.hyperbolas import Hyperbola

# ---------- General Setup Utilities ----------

def prepare_plot(title="Plot"):
    plt.figure(figsize=(7, 7))
    plt.title(title)
    plt.grid(True)
    plt.gca().set_aspect('equal')

def finish_plot():
    plt.grid()
    plt.legend()
    plt.show()

def plot_point(p: Point, label='', color='red', size=50):
    plt.scatter(p.x, p.y, c=color, s=size, label=label)
    if label:
        plt.text(p.x + 0.2, p.y + 0.2, label, fontsize=10)

# ---------- Line ----------

def plot_line(line, label=None, bounds=(-10, 10), color='blue'):
    try:
        x_vals = list(bounds)
        y_vals = [line.evaluate(x) for x in x_vals]
        if label:
            plt.plot(x_vals, y_vals, color=color, label=label)
        else:
            plt.plot(x_vals, y_vals, color=color)
    except ValueError:
        if label:
            plt.axvline(x=line.p1.x, color=color, label=label)
        else:
            plt.axvline(x=line.p1.x, color=color)

# ---------- Circle ----------

def plot_circle(circle : Circle, show_center=True, show_radius=True, label=''):
    theta = [math.radians(i) for i in range(361)]
    xs = [circle.center.x + circle.radius * math.cos(t) for t in theta]
    ys = [circle.center.y + circle.radius * math.sin(t) for t in theta]
    plt.plot(xs, ys, label=label)

    if show_center:
        plot_point(circle.center, label='Center', color='black')

    if show_radius:
        edge = Point(circle.center.x + circle.radius, circle.center.y)
        plt.plot([circle.center.x, edge.x], [circle.center.y, edge.y], 'g--')

# ---------- Triangle ----------

def plot_triangle(triangle : Triangle, label_vertices=True):
    pts = [triangle.a, triangle.b, triangle.c, triangle.a]
    xs = [p.x for p in pts]
    ys = [p.y for p in pts]
    plt.plot(xs, ys, 'purple', label="Triangle")

    if label_vertices:
        for i, p in enumerate([triangle.a, triangle.b, triangle.c]):
            plot_point(p, label=chr(65 + i))  # A, B, C

# ---------- Parabola ----------

def plot_parabola(parabola : Parabola, range_val=(-10, 10), label='Parabola'):
    vals = [v / 10 for v in range(int(range_val[0]*10), int(range_val[1]*10))]
    xs, ys = [], []

    for val in vals:
        try:
            if parabola.orientation == 'v':
                xs.append(val)
                ys.append(parabola.evaluate(val))
            else:
                ys.append(val)
                xs.append(parabola.evaluate(val))
        except:
            continue

    plt.plot(xs, ys, label=label)
    plot_point(parabola.vertex(), label="Vertex", color='green')
    plot_point(parabola.focus(), label="Focus", color='blue')

# ---------- Ellipse ----------

def plot_ellipse(ellipse : Ellipse, show_foci=True, label='Ellipse'):
    theta = [math.radians(i) for i in range(361)]

    # Handle orientation
    if ellipse.orientation == 'horizontal':
        xs = [ellipse.h + ellipse.a * math.cos(t) for t in theta]
        ys = [ellipse.k + ellipse.b * math.sin(t) for t in theta]
    else:
        xs = [ellipse.h + ellipse.b * math.cos(t) for t in theta]
        ys = [ellipse.k + ellipse.a * math.sin(t) for t in theta]

    plt.plot(xs, ys, label=label)

    if show_foci:
        f1, f2 = ellipse.foci()
        plot_point(f1, label='F1', color='green')
        plot_point(f2, label='F2', color='green')

# ---------- Hyperbola ----------

def plot_hyperbola(hyperbola : Hyperbola, range_val=(-10, 10), show_foci=True, label='Hyperbola'):
    vals = [v / 10 for v in range(int(range_val[0] * 10), int(range_val[1] * 10))]
    branch1, branch2 = [], []

    for val in vals:
        try:
            a1, a2 = hyperbola.evaluate(val)
            if hyperbola.orientation == 'h':
                branch1.append((val, a1))  # x, +y
                branch2.append((val, a2))  # x, -y
            else:
                branch1.append((a1, val))  # +x, y
                branch2.append((a2, val))  # -x, y
        except ValueError:
            continue

    if branch1:
        x1, y1 = zip(*branch1)
        plt.plot(x1, y1, label=label)
    if branch2:
        x2, y2 = zip(*branch2)
        plt.plot(x2, y2, linestyle='--')

    if show_foci:
        f1, f2 = hyperbola.foci()
        plot_point(f1, label='F1', color='green')
        plot_point(f2, label='F2', color='green')