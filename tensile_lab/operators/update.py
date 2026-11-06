import bpy
from bpy.types import Operator
from ..core.registry import registry
from ..geometry.generators import build_outline_from_dims
from ..geometry.mesh import build_mesh_data
from ..geometry.mold import generate_mold_mesh
from .generate import compute_effective_dims, _resolve_cavity_depth


class TENSILELAB_OT_update(Operator):
    bl_idname = "tensilelab.update"
    bl_label = "Update"
    bl_description = "Rebuild the active specimen or mold from current settings"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = context.active_object
        if not obj or "tensile_role" not in obj:
            self.report({'ERROR'}, "Select a generated specimen or mold first")
            return {'CANCELLED'}

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

        role = obj["tensile_role"]
        old = obj.data
        cavity_depth = _resolve_cavity_depth(props)

        try:
            if role == "mold":
                new_mesh = generate_mold_mesh(
                    obj.name + "_mesh", outline, thickness,
                    props.mold_margin, props.mold_floor, cavity_depth,
                )
            else:
                new_mesh = build_mesh_data(obj.name + "_mesh", outline, thickness)
        except Exception as exc:
            self.report({'ERROR'}, f"Rebuild error: {exc}")
            return {'CANCELLED'}

        obj.data = new_mesh
        if old and old.users == 0:
            bpy.data.meshes.remove(old)

        obj["tensile_specimen_id"] = spec["id"]
        obj["tensile_scale"] = factor
        obj["tensile_modified"] = props.dirty
        return {'FINISHED'}
