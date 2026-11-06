import math

REQUIRED = ("id", "standard", "standard_number", "specimen_type",
            "geometry", "dimensions")


def validate_specimen(spec):
    errors = []
    for field in REQUIRED:
        if field not in spec:
            errors.append(f"missing field '{field}'")

    sid = spec.get("id")
    if not isinstance(sid, str) or not sid:
        errors.append("'id' must be a non-empty string")

    dims = spec.get("dimensions")
    if not isinstance(dims, dict) or not dims:
        errors.append("'dimensions' must be a non-empty object")
    else:
        for k, v in dims.items():
            if not isinstance(v, (int, float)):
                errors.append(f"dimension '{k}' must be numeric")

    try:
        from ..geometry.generators import GENERATORS
        geom = spec.get("geometry")
        if geom not in GENERATORS:
            errors.append(f"unknown geometry '{geom}'")
    except Exception:
        pass

    return errors


def validate_geometry_feasibility(spec):
    dims = spec.get("dimensions", {})
    geom = spec.get("geometry")
    errors = []

    try:
        if geom == "two_radius_symmetric":
            h = (dims["end_width"] - dims["narrow_width"]) / 2.0
            R = dims["radius_e"] + dims["radius_f"]
            if h <= 0 or R <= 0:
                return ["non-positive widths or radii"]
            c = 1.0 - h / R
            if not (-1.0 <= c <= 1.0):
                return [f"two-radius infeasible: h={h}, r_E+r_F={R}"]
            alpha = math.acos(c)
            transition = R * math.sin(alpha)
            required_half = dims["narrow_length"] / 2.0 + transition
            if required_half > dims["overall_length"] / 2.0 + 1e-6:
                errors.append(
                    f"transition ({transition:.2f} mm/side) does not fit "
                    f"inside overall_length={dims['overall_length']}"
                )

        elif geom == "single_radius_symmetric":
            h = (dims["end_width"] - dims["narrow_width"]) / 2.0
            r = dims["radius"]
            if h <= 0 or r <= 0:
                return ["non-positive width or radius"]
            c = 1.0 - h / r
            if not (-1.0 <= c <= 1.0):
                return [f"single-radius infeasible: h={h}, r={r}"]
            alpha = math.acos(c)
            transition = r * math.sin(alpha)
            required_half = dims["narrow_length"] / 2.0 + transition
            if required_half > dims["overall_length"] / 2.0 + 1e-6:
                errors.append(
                    f"transition ({transition:.2f} mm/side) does not fit "
                    f"inside overall_length={dims['overall_length']}"
                )
    except KeyError as exc:
        errors.append(f"missing dimension for geometry check: {exc}")

    return errors
