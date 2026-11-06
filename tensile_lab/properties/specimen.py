import bpy
from bpy.types import PropertyGroup
from bpy.props import (EnumProperty, FloatProperty, IntProperty,
                       StringProperty, BoolProperty)

from ..core.registry import registry
from ..core.constants import ALL_DIMENSION_KEYS
from ..core.config import DEFAULT_ARC_SEGMENTS


def _family_items(self, context):
    fams = registry.families()
    if not fams:
        return [("NONE", "(no library)", "")]
    return [(f, f, f"Standard family: {f}") for f in fams]


def _standard_items(self, context):
    fam = self.standard_family
    if not fam or fam == "NONE":
        return [("NONE", "(none)", "")]
    stds = registry.standards(fam)
    if not stds:
        return [("NONE", "(none)", "")]
    return [(s, s, f"Standard: {s}") for s in stds]


def _specimen_items(self, context):
    fam, std = self.standard_family, self.standard_number
    if not fam or not std or fam == "NONE" or std == "NONE":
        return [("NONE", "(none)", "")]
    ids = registry.specimens_for(fam, std)
    items = []
    for sid in ids:
        spec = registry.get(sid)
        if not spec:
            continue
        desc = (f"{spec.get('standard_number', '')} | "
                f"{spec.get('specimen_type', '')}\n"
                f"{spec.get('category', '')}\n"
                f"{spec.get('description', '')}")[:480]
        items.append((sid, spec.get("specimen_type", sid), desc))
    if not items:
        return [("NONE", "(none)", "")]
    return items


def _mark_dirty(self, context):
    self.dirty = True


def _on_family_changed(self, context):
    stds = registry.standards(self.standard_family)
    self.standard_number = stds[0] if stds else "NONE"


def _on_standard_changed(self, context):
    ids = registry.specimens_for(self.standard_family, self.standard_number)
    self.specimen_type = ids[0] if ids else "NONE"


def _on_specimen_changed(self, context):
    spec = registry.get(self.specimen_type)
    if spec:
        _apply_specimen(spec, self)


def _on_mode_changed(self, context):
    if self.mode == 'STANDARD':
        spec = registry.get(self.specimen_type)
        if spec:
            _apply_specimen(spec, self)


def _apply_specimen(spec, props):
    dims = spec.get("dimensions", {})
    for k in ALL_DIMENSION_KEYS:
        if k in dims:
            try:
                setattr(props, k, float(dims[k]))
            except Exception:
                pass
    settings = spec.get("settings", {})
    props.arc_segments = int(settings.get("arc_segments", DEFAULT_ARC_SEGMENTS))
    if "overall_length" in dims:
        props.target_length = float(dims["overall_length"])
    props.dirty = False


class TensileLabProperties(PropertyGroup):
    standard_family: EnumProperty(name="Family", items=_family_items, update=_on_family_changed)
    standard_number: EnumProperty(name="Standard", items=_standard_items, update=_on_standard_changed)
    specimen_type:   EnumProperty(name="Specimen", items=_specimen_items, update=_on_specimen_changed)

    mode: EnumProperty(
        name="Mode",
        items=[('STANDARD', "Standard", "Read-only reference values"),
               ('CUSTOM',   "Custom",   "Edit dimensions freely")],
        default='STANDARD',
        update=_on_mode_changed,
    )
    dirty: BoolProperty(name="Modified", default=False)

    overall_length: FloatProperty(name="Overall Length", default=100.0, min=0.01, unit='LENGTH', update=_mark_dirty, precision=3)
    end_width:      FloatProperty(name="End Width",      default=20.0,  min=0.01, unit='LENGTH', update=_mark_dirty, precision=3)
    narrow_length:  FloatProperty(name="Narrow Length",  default=40.0,  min=0.01, unit='LENGTH', update=_mark_dirty, precision=3)
    narrow_width:   FloatProperty(name="Narrow Width",   default=10.0,  min=0.01, unit='LENGTH', update=_mark_dirty, precision=3)
    radius_e:       FloatProperty(name="Radius E (inner)", default=20.0, min=0.001, unit='LENGTH', update=_mark_dirty, precision=3)
    radius_f:       FloatProperty(name="Radius F (outer)", default=20.0, min=0.001, unit='LENGTH', update=_mark_dirty, precision=3)
    radius:         FloatProperty(name="Transition Radius", default=25.0, min=0.001, unit='LENGTH', update=_mark_dirty, precision=3)
    thickness:      FloatProperty(name="Thickness",      default=2.0,   min=0.001, unit='LENGTH', update=_mark_dirty, precision=3)
    arc_segments:   IntProperty(name="Arc Segments", default=DEFAULT_ARC_SEGMENTS, min=4, max=512, update=_mark_dirty)

    # Scaling
    scale_enabled: BoolProperty(name="Enable Scaling", default=False)
    target_length: FloatProperty(name="Target Length", default=100.0, min=0.01, unit='LENGTH', precision=3)
    scale_z:       BoolProperty(name="Scale Z (thickness)", default=False)

    # Output
    output_mode: EnumProperty(
        name="Output",
        items=[('SPECIMEN', "Specimen", "Solid specimen"),
               ('MOLD',     "Mold",     "Block with specimen cavity"),
               ('BOTH',     "Both",     "Specimen and mold as separate objects")],
        default='SPECIMEN',
    )
    mold_margin: FloatProperty(name="Mold Margin", default=5.0, min=0.001, unit='LENGTH', precision=3)
    mold_floor:  FloatProperty(name="Mold Floor",  default=2.0, min=0.001, unit='LENGTH', precision=3)

    mold_use_custom_depth: BoolProperty(name="Use Custom Cavity Depth", default=False)
    mold_cavity_depth:     FloatProperty(name="Cavity Depth", default=10.0, min=0.001,
                                         unit='LENGTH', precision=3)

    custom_name: StringProperty(name="Custom Name", default="", description="Name for saved custom specimen")
