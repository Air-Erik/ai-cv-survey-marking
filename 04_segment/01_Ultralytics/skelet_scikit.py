import skgeom as sg
from skgeom.draw import draw

import matplotlib.pyplot as plt

def draw_skeleton(polygon, skeleton, show_time=False):
    draw(polygon)

    for h in skeleton.halfedges:
        if h.is_bisector:
            p1 = h.vertex.point
            p2 = h.opposite.vertex.point
            plt.plot([p1.x(), p2.x()], [p1.y(), p2.y()], 'r-', lw=2)

    if show_time:
        for v in skeleton.vertices:
            plt.gcf().gca().add_artist(plt.Circle(
                (v.point.x(), v.point.y()),
                v.time, color='blue', fill=False))
poly = sg.random_polygon(seed=1)
skel = sg.skeleton.create_interior_straight_skeleton(poly)
draw_skeleton(poly, skel)
