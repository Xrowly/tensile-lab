from ..outline import build_single_radius_outline

DIMENSION_KEYS = (
    "overall_length", "end_width", "narrow_length",
    "narrow_width", "radius",
)


def build_outline(dims, arc_segments=32):
    return build_single_radius_outline(dims, arc_segments)
