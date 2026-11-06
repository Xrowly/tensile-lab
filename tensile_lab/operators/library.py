import bpy
from bpy.types import Operator
from ..core.registry import registry
from ..data.json_loader import save_user_library, load_library
from ..geometry.generators import dimension_keys_for


def _unique_id(base):
    if base not in registry.specimens:
        return base
    i = 1
    while f"{base}_{i}" in registry.specimens:
        i += 1
    return f"{base}_{i}"


class TENSILELAB_OT_save_custom(Operator):
    bl_idname = "tensilelab.save_custom"
    bl_label = "Save as Custom"
    bl_description = "Save current base dimensions as a new custom entry"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        props = context.scene.tensile_lab
        base = registry.get(props.specimen_type)
        if not base:
            self.report({'ERROR'}, "No base specimen selected")
            return {'CANCELLED'}
        name = props.custom_name.strip() or f"{base.get('specimen_type', 'Custom')} - Custom"
        new_id = _unique_id(base["id"] + "_CUSTOM")
        dims = {k: float(getattr(props, k)) for k in dimension_keys_for(base["geometry"])}
        dims["thickness"] = float(props.thickness)
        spec = {
            "id": new_id,
            "standard": base.get("standard", "Custom"),
            "standard_number": base.get("standard_number", "Custom"),
            "edition": None,
            "specimen_type": name,
            "name": name,
            "category": base.get("category", "Custom"),
            "description": f"Custom from {base.get('name', base['id'])}",
            "geometry": base["geometry"],
            "dimensions": dims,
            "settings": {"arc_segments": int(props.arc_segments), "unit": "mm"},
            "source": {"document": None, "verified": False},
            "library": {"type": "custom", "editable": True},
        }
        registry.add(spec)
        try:
            save_user_library()
        except Exception as exc:
            self.report({'ERROR'}, f"Could not save: {exc}")
            return {'CANCELLED'}
        self.report({'INFO'}, f"Saved '{name}' (base dimensions)")
        return {'FINISHED'}


class TENSILELAB_OT_delete_custom(Operator):
    bl_idname = "tensilelab.delete_custom"
    bl_label = "Delete Custom Specimen"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        props = context.scene.tensile_lab
        sid = props.specimen_type
        if not sid or not registry.is_custom(sid):
            self.report({'ERROR'}, "Selected specimen is not custom")
            return {'CANCELLED'}
        del registry.specimens[sid]
        for std_map in registry.by_family.values():
            for lst in std_map.values():
                if sid in lst:
                    lst.remove(sid)
        try:
            save_user_library()
        except Exception as exc:
            self.report({'ERROR'}, f"Could not save: {exc}")
            return {'CANCELLED'}
        ids = registry.specimens_for(props.standard_family, props.standard_number)
        props.specimen_type = ids[0] if ids else "NONE"
        return {'FINISHED'}


class TENSILELAB_OT_reload_library(Operator):
    bl_idname = "tensilelab.reload_library"
    bl_label = "Reload Library"
    bl_options = {'REGISTER'}

    def execute(self, context):
        load_library()
        props = context.scene.tensile_lab
        fams = registry.families()
        props.standard_family = fams[0] if fams else "NONE"
        self.report({'INFO'}, f"Loaded {len(registry.specimens)} specimens")
        return {'FINISHED'}
