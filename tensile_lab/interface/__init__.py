import bpy
from .panel import TENSILELAB_PT_main

CLASSES = [TENSILELAB_PT_main]

def register():
    for c in CLASSES:
        bpy.utils.register_class(c)

def unregister():
    for c in reversed(CLASSES):
        bpy.utils.unregister_class(c)
