import bpy
from bpy.types import Operator
from ..core.registry import registry
from ..properties.specimen import _apply_specimen


class TENSILELAB_OT_reset(Operator):
    bl_idname = "tensilelab.reset"
    bl_label = "Reset to Standard"
    bl_description = "Restore reference dimensions from the JSON library"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        props = context.scene.tensile_lab
        spec = registry.get(props.specimen_type)
        if not spec:
            self.report({'ERROR'}, "No specimen selected")
            return {'CANCELLED'}
        _apply_specimen(spec, props)
        props.mode = 'STANDARD'
        return {'FINISHED'}
