import math

def solve_two_radius_angle(r1, r2, h):
    R = r1 + r2
    if R <= 0:
        raise ValueError("radii must be positive")
    c = 1.0 - h / R
    if c < -1.0 or c > 1.0:
        raise ValueError(f"Inconsistent radii (r1+r2={R}) and h={h}")
    return math.acos(c)


def solve_single_radius_angle(r, h):
    if r <= 0:
        raise ValueError("radius must be positive")
    if h > 2 * r:
        raise ValueError("height difference exceeds diameter")
    c = 1.0 - h / r
    if c < -1.0 or c > 1.0:
        raise ValueError("inconsistent radius and height")
    return math.acos(c)
