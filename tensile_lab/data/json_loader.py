import json, os, shutil

from ..core.config import LIBRARY_FILE, get_user_library_path
from ..core.registry import registry
from .json_validator import validate_specimen, validate_geometry_feasibility


def _read(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _ingest(path):
    if not os.path.isfile(path):
        return
    try:
        data = _read(path)
    except Exception as exc:
        print(f"[TensileLab] Failed to load {path}: {exc}")
        return
    for spec in data.get("specimens", []):
        errs = validate_specimen(spec) + validate_geometry_feasibility(spec)
        if errs:
            print(f"[TensileLab] REJECTED {spec.get('id', '?')}: {'; '.join(errs)}")
            continue
        registry.add(spec)


def load_library():
    registry.clear()
    _ingest(LIBRARY_FILE)
    _ingest(get_user_library_path())


def save_user_library():
    custom = registry.all_custom()
    path = get_user_library_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if os.path.isfile(path):
        shutil.copy2(path, path + ".bak")
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump({"version": "1.3", "specimens": custom}, f, indent=2)
    os.replace(tmp, path)
