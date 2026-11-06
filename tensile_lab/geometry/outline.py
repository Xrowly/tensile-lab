import math
from .arc import arc_points
from .tangency import solve_two_radius_angle, solve_single_radius_angle
from .symmetry import mirror_y, dedupe


def build_two_radius_outline(dims, arc_segments=32):
    L        = float(dims["overall_length"])
    w_end    = float(dims["end_width"])
    L_narrow = float(dims["narrow_length"])
    w_narrow = float(dims["narrow_width"])
    r1       = float(dims["radius_e"])
    r2       = float(dims["radius_f"])

    if L <= L_narrow:
        raise ValueError("overall_length must exceed narrow_length")
    if w_end <= w_narrow:
        raise ValueError("end_width must exceed narrow_width")

    h     = (w_end - w_narrow) / 2.0
    alpha = solve_two_radius_angle(r1, r2, h)

    quadrant = [(0.0, w_narrow / 2.0), (L_narrow / 2.0, w_narrow / 2.0)]
    seg = max(6, int(arc_segments))

    c1 = (L_narrow / 2.0, w_narrow / 2.0 + r1)
    a1 = arc_points(c1, r1, -math.pi / 2.0, -math.pi / 2.0 + alpha, seg)
    quadrant.extend(a1[1:])

    jx, jy = a1[-1]
    c2 = (jx + r2 * math.sin(alpha), jy - r2 * math.cos(alpha))
    a2 = arc_points(c2, r2, math.pi / 2.0 + alpha, math.pi / 2.0, seg)
    quadrant.extend(a2[1:])

    quadrant.append((L / 2.0, w_end / 2.0))
    return _close_outline(quadrant)


def build_single_radius_outline(dims, arc_segments=32):
    L        = float(dims["overall_length"])
    w_end    = float(dims["end_width"])
    L_narrow = float(dims["narrow_length"])
    w_narrow = float(dims["narrow_width"])
    r        = float(dims["radius"])

    if L <= L_narrow:
        raise ValueError("overall_length must exceed narrow_length")
    if w_end <= w_narrow:
        raise ValueError("end_width must exceed narrow_width")

    h     = (w_end - w_narrow) / 2.0
    alpha = solve_single_radius_angle(r, h)

    quadrant = [(0.0, w_narrow / 2.0), (L_narrow / 2.0, w_narrow / 2.0)]
    seg = max(6, int(arc_segments))

    c1 = (L_narrow / 2.0, w_narrow / 2.0 + r)
    a1 = arc_points(c1, r, -math.pi / 2.0, -math.pi / 2.0 + alpha, seg)
    quadrant.extend(a1[1:])

    if a1[-1][0] > L / 2.0 + 1e-6:
        raise ValueError("transition does not fit: increase overall_length or reduce radius")
    quadrant.append((L / 2.0, w_end / 2.0))
    return _close_outline(quadrant)


def _close_outline(quadrant):
    top_half    = mirror_y(quadrant[::-1]) + quadrant[1:]
    bottom_half = [(x, -y) for (x, y) in top_half]

    B, C = top_half[-1], top_half[0]
    D, E = bottom_half[0], bottom_half[-1]

    outline = [E, B]
    for p in reversed(top_half[:-1]):
        outline.append(p)
    outline.append(D)
    for p in bottom_half[1:-1]:
        outline.append(p)
    return dedupe(outline)
