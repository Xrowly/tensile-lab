import bpy
from .generate import TENSILELAB_OT_generate
from .update   import TENSILELAB_OT_update
from .reset    import TENSILELAB_OT_reset
from .library  import (TENSILELAB_OT_save_custom, TENSILELAB_OT_delete_custom,
                       TENSILELAB_OT_reload_library)

CLASSES = [TENSILELAB_OT_generate, TENSILELAB_OT_update, TENSILELAB_OT_reset,
           TENSILELAB_OT_save_custom, TENSILELAB_OT_delete_custom,
           TENSILELAB_OT_reload_library]

def register():
    for c in CLASSES:
        bpy.utils.register_class(c)

def unregister():
    for c in reversed(CLASSES):
        bpy.utils.unregister_class(c)
