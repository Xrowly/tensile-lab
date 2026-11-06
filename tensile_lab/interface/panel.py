import bpy
from bpy.types import Panel
from ..core.registry import registry
from .selectors import draw_selectors
from .parameters import draw_parameters, draw_scaling, draw_output


class TENSILELAB_PT_main(Panel):
    bl_label = "Tensile Lab"
    bl_idname = "TENSILELAB_PT_main"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Tensile Lab"

    def draw(self, context):
        layout = self.layout
        props = context.scene.tensile_lab
        draw_selectors(layout, props)

        spec = registry.get(props.specimen_type)
        if spec:
            info = layout.box()
            info.label(text="Information", icon='INFO')
            col = info.column(align=True)
            col.label(text=f"ID: {spec.get('id', '')}")
            col.label(text=f"Standard: {spec.get('standard_number', '')} ({spec.get('edition', '?')})")
            col.label(text=f"Type: {spec.get('specimen_type', '')}")
            col.label(text=f"Geometry: {spec.get('geometry', '')}")
            src = spec.get("source", {})
            col.label(text=f"Source: {src.get('document', '?')} / {src.get('table', '?')}")
            col.label(text="Verified" if src.get("verified") else "UNVERIFIED",
                      icon='CHECKMARK' if src.get("verified") else 'QUESTION')
            col.separator()
            col.label(text=spec.get("description", ""))

        mode_box = layout.box()
        mode_box.label(text="Mode", icon='TOOL_SETTINGS')
        mode_box.prop(props, "mode", expand=True)

        draw_parameters(layout, props, spec)
        draw_scaling(layout, props, spec)
        draw_output(layout, props)

        act = layout.box()
        act.label(text="Geometry", icon='MESH_DATA')
        col = act.column(align=True)
        col.operator("tensilelab.generate", text="Generate", icon='ADD')
        col.operator("tensilelab.update",   text="Update Selected", icon='FILE_REFRESH')
        col.operator("tensilelab.reset",    text="Reset to Standard", icon='LOOP_BACK')

        lib = layout.box()
        lib.label(text="Library", icon='FILE_FOLDER')
        col = lib.column(align=True)
        col.prop(props, "custom_name", text="Name")
        col.operator("tensilelab.save_custom",   text="Save as Custom",         icon='FILE_NEW')
        col.operator("tensilelab.delete_custom", text="Delete Custom Specimen", icon='TRASH')
        col.separator()
        col.operator("tensilelab.reload_library", text="Reload Library", icon='FILE_REFRESH')
