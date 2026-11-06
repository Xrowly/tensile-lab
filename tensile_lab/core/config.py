import os
import bpy

ADDON_DIR    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR     = os.path.join(ADDON_DIR, "data")
LIBRARY_FILE = os.path.join(DATA_DIR, "specimen_library.json")


def get_user_library_path():
    base = bpy.utils.user_resource('CONFIG', path='tensile_lab', create=True)
    return os.path.join(base, "user_library.json")


DEFAULT_ARC_SEGMENTS = 32
