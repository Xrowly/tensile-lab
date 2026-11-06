bl_info = {
    "name": "Tensile Lab",
    "author": "Marios 'Xrowly' Diakatos",
    "version": (1, 3, 0),
    "blender": (3, 6, 0),
    "location": "View3D > Sidebar > Tensile Lab",
    "description": "Parametric tensile specimen generator with scaling and mold output",
    "category": "Add Mesh",
}

import bpy

from .data.json_loader import load_library
from .properties import register as register_props, unregister as unregister_props
from .operators  import register as register_ops,   unregister as unregister_ops
from .interface  import register as register_ui,    unregister as unregister_ui


def register():
    load_library()
    register_props()
    register_ops()
    register_ui()


def unregister():
    unregister_ui()
    unregister_ops()
    unregister_props()
