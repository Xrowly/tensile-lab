def mirror_y(points):
    return [(-x, y) for (x, y) in points]


def dedupe(points, eps=1e-7):
    out = []
    for p in points:
        if not out or abs(p[0] - out[-1][0]) > eps or abs(p[1] - out[-1][1]) > eps:
            out.append(p)
    if len(out) > 1 and abs(out[0][0] - out[-1][0]) < eps \
            and abs(out[0][1] - out[-1][1]) < eps:
        out.pop()
    return out
