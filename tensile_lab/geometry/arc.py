import math

def arc_points(center, radius, a0, a1, segments):
    segments = max(1, int(segments))
    cx, cy = center
    out = []
    for i in range(segments + 1):
        t = i / segments
        a = a0 + (a1 - a0) * t
        out.append((cx + radius * math.cos(a), cy + radius * math.sin(a)))
    return out
