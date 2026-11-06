from ..geometry.generators import dimension_keys_for

LABELS = {
    "overall_length": "Overall Length",
    "end_width": "End Width",
    "narrow_length": "Narrow Length",
    "narrow_width": "Narrow Width",
    "radius_e": "Radius E (inner)",
    "radius_f": "Radius F (outer)",
    "radius": "Transition Radius",
    "thickness": "Thickness",
}


def draw_parameters(layout, props, spec):
    box = layout.box()
    box.label(text="Dimensions (base)", icon='MOD_LENGTH')
    if not spec:
        box.label(text="(no specimen selected)", icon='INFO')
        return
    geom = spec.get("geometry")
    keys = dimension_keys_for(geom)
    if not keys:
        box.label(text=f"Unknown geometry: {geom}", icon='ERROR')
        return
    editable = (props.mode == 'CUSTOM')
    col = box.column(align=True)
    col.enabled = editable
    for key in keys:
        if hasattr(props, key):
            col.prop(props, key, text=LABELS.get(key, key))
    if "thickness" not in keys and hasattr(props, "thickness"):
        col.prop(props, "thickness", text=LABELS["thickness"])
    row = box.row()
    row.enabled = editable
    row.prop(props, "arc_segments", text="Arc Segments")
    if props.mode == 'STANDARD':
        box.label(text="Read-only (Standard mode)", icon='LOCKED')
    elif props.dirty:
        box.label(text="CUSTOM / MODIFIED", icon='ERROR')
    else:
        box.label(text="Custom (unmodified)", icon='INFO')


def draw_scaling(layout, props, spec):
    box = layout.box()
    box.label(text="Scaling", icon='FULLSCREEN_ENTER')
    box.prop(props, "scale_enabled", text="Enable Scaling")

    row = box.row()
    row.enabled = props.scale_enabled
    row.prop(props, "target_length", text="Target Length")

    if props.scale_enabled and spec and props.overall_length > 0:
        factor = props.target_length / props.overall_length
        box.label(text=f"  Factor: x{factor:.3f}  (base {props.overall_length:.2f} mm)")
        base_t = props.thickness
        eff_t = base_t * factor if props.scale_z else base_t
        box.label(text=f"  Effective thickness: {eff_t:.3f} mm")

    row = box.row()
    row.enabled = props.scale_enabled
    row.prop(props, "scale_z", text="Scale Z (thickness)")

    if props.scale_enabled:
        box.label(text="(Save as Custom uses base, unscaled)", icon='INFO')


def draw_output(layout, props):
    box = layout.box()
    box.label(text="Output", icon='MOD_BUILD')
    box.prop(props, "output_mode", expand=True)

    if props.output_mode in {'MOLD', 'BOTH'}:
        col = box.column(align=True)
        col.prop(props, "mold_margin", text="Mold Margin")
        col.prop(props, "mold_floor",  text="Mold Floor")
        col.separator()
        col.prop(props, "mold_use_custom_depth", text="Use Custom Cavity Depth")
        row = col.row()
        row.enabled = props.mold_use_custom_depth
        row.prop(props, "mold_cavity_depth", text="Cavity Depth")

        if props.mold_use_custom_depth and props.mold_cavity_depth < props.thickness:
            warn = box.row()
            warn.alert = True
            warn.label(text="Cavity depth < thickness; generation will fail", icon='ERROR')
