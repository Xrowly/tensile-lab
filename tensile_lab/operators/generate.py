import bpy
from bpy.types import Operator
from ..core.registry import registry
from ..geometry.generators import build_outline_from_dims, dimension_keys_for
from ..geometry.mesh import build_mesh_data, create_object, select_only
from ..geometry.mold import generate_mold_mesh


def compute_effective_dims(spec, props):
    """Return (dims_dict, scale_factor).

    Base dimensions come from the live props (so CUSTOM edits, including
    thickness, are honoured). Scaling is applied on top of that base.
    """
    geom = spec["geometry"]
    keys = list(dimension_keys_for(geom))
    if "thickness" not in keys:
        keys.append("thickness")

    base = {}
    for k in keys:
        if hasattr(props, k):
            base[k] = float(getattr(props, k))

    if not props.scale_enabled:
        return base, 1.0

    base_L = base.get("overall_length", 0.0)
    if base_L <= 0.0 or props.target_length <= 0.0:
        return base, 1.0

    s = props.target_length / base_L
    out = {}
    for k, v in base.items():
        if k == "thickness" and not props.scale_z:
            out[k] = float(v)
        else:
            out[k] = float(v) * s
    return out, s


def _resolve_cavity_depth(props):
    if props.mold_use_custom_depth:
        return float(props.mold_cavity_depth)
    return None


class TENSILELAB_OT_generate(Operator):
    bl_idname = "tensilelab.generate"
    bl_label = "Generate"
    bl_description = "Build the selected specimen and/or mold"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        props = context.scene.tensile_lab
        spec = registry.get(props.specimen_type)
        if not spec:
            self.report({'ERROR'}, "No specimen selected")
            return {'CANCELLED'}

        try:
            dims, factor = compute_effective_dims(spec, props)
            outline = build_outline_from_dims(spec["geometry"], dims, props.arc_segments)
            thickness = float(dims.get("thickness", 0))
        except Exception as exc:
            self.report({'ERROR'}, f"Geometry error: {exc}")
            return {'CANCELLED'}

        mode = props.output_mode
        cavity_depth = _resolve_cavity_depth(props)

        if mode in {'SPECIMEN', 'BOTH'}:
            suffix = "_Specimen" if mode == 'BOTH' else ""
            name = f"Tensile_{spec['id']}{suffix}"
            mesh = build_mesh_data(name + "_mesh", outline, thickness)
            obj = create_object(name, mesh)
            obj["tensile_specimen_id"] = spec["id"]
            obj["tensile_role"] = "specimen"
            obj["tensile_scale"] = factor
            obj["tensile_modified"] = props.dirty
            select_only(obj)

        if mode in {'MOLD', 'BOTH'}:
            name = f"Tensile_{spec['id']}_Mold"
            try:
                mold_mesh = generate_mold_mesh(
                    name + "_mesh", outline, thickness,
                    props.mold_margin, props.mold_floor, cavity_depth,
                )
            except Exception as exc:
                self.report({'ERROR'}, f"Mold error: {exc}")
                return {'CANCELLED'}
            obj = create_object(name, mold_mesh)
            obj["tensile_specimen_id"] = spec["id"]
            obj["tensile_role"] = "mold"
            obj["tensile_scale"] = factor
            select_only(obj)

        return {'FINISHED'}
