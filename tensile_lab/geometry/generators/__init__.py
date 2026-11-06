from .two_radius import build_outline as _build_two_radius, DIMENSION_KEYS as _TWO_RADIUS_KEYS
from .single_radius import build_outline as _build_single_radius, DIMENSION_KEYS as _SINGLE_RADIUS_KEYS

GENERATORS = {
    "two_radius_symmetric":    (_build_two_radius,    _TWO_RADIUS_KEYS),
    "single_radius_symmetric": (_build_single_radius, _SINGLE_RADIUS_KEYS),
}


def build_geometry(geometry_id, props):
    if geometry_id not in GENERATORS:
        raise ValueError(f"Unknown geometry identifier: {geometry_id}")
    builder, dim_keys = GENERATORS[geometry_id]
    dims = {k: getattr(props, k) for k in dim_keys if hasattr(props, k)}
    outline = builder(dims, props.arc_segments)
    return outline, float(props.thickness)


def build_outline_from_dims(geometry_id, dims, arc_segments):
    if geometry_id not in GENERATORS:
        raise ValueError(f"Unknown geometry: {geometry_id}")
    builder, _ = GENERATORS[geometry_id]
    return builder(dims, arc_segments)


def dimension_keys_for(geometry_id):
    if geometry_id not in GENERATORS:
        return []
    return list(GENERATORS[geometry_id][1])
