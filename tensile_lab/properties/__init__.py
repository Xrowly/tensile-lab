import bpy
from .specimen import TensileLabProperties

def register():
    bpy.utils.register_class(TensileLabProperties)
    bpy.types.Scene.tensile_lab = bpy.props.PointerProperty(type=TensileLabProperties)

def unregister():
    del bpy.types.Scene.tensile_lab
    bpy.utils.unregister_class(TensileLabProperties)
