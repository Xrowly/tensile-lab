def draw_selectors(layout, props):
    box = layout.box()
    box.label(text="Specimen Selection", icon='PRESET')
    col = box.column(align=True)
    col.prop(props, "standard_family", text="Family")
    col.prop(props, "standard_number", text="Standard")
    col.prop(props, "specimen_type",  text="Specimen")
