import bpy


def _ensure_object_mode():
    if bpy.context.object and bpy.context.object.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')


def _temp_object(name, mesh):
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    return obj


def generate_mold_mesh(name, outline, thickness, margin, floor_height,
                       cavity_depth=None):
    """Block minus specimen cavity.

    Specimen sits from -thickness/2 to +thickness/2.
    Cavity: from (thickness/2 - cavity_depth) up to top face.
    Block:  from (thickness/2 - cavity_depth - floor_height) up to top face.

    cavity_depth defaults to thickness (exact fit).
    cavity_depth must be >= thickness; otherwise the specimen will not fit.
    """
    _ensure_object_mode()

    if cavity_depth is None or cavity_depth <= 0:
        cavity_depth = thickness
    if cavity_depth < thickness - 1e-6:
        raise ValueError(
            f"cavity depth ({cavity_depth:.3f} mm) < specimen thickness "
            f"({thickness:.3f} mm); specimen would not fit"
        )

    xs = [p[0] for p in outline]
    ys = [p[1] for p in outline]
    min_x, max_x = min(xs) - margin, max(xs) + margin
    min_y, max_y = min(ys) - margin, max(ys) + margin

    z_top           = thickness / 2.0
    z_cavity_bottom = z_top - cavity_depth
    z_bottom        = z_cavity_bottom - floor_height

    block_verts = [
        (min_x, min_y, z_bottom), (max_x, min_y, z_bottom),
        (max_x, max_y, z_bottom), (min_x, max_y, z_bottom),
        (min_x, min_y, z_top),    (max_x, min_y, z_top),
        (max_x, max_y, z_top),    (min_x, max_y, z_top),
    ]
    block_faces = [
        [0, 3, 2, 1], [4, 5, 6, 7],
        [0, 1, 5, 4], [1, 2, 6, 5], [2, 3, 7, 6], [3, 0, 4, 7],
    ]
    block_mesh = bpy.data.meshes.new(name + "_block_tmp")
    block_mesh.from_pydata(block_verts, [], block_faces)
    block_mesh.update()
    block_mesh.validate(verbose=False)
    block_obj = _temp_object(name + "_block_tmp", block_mesh)

    n = len(outline)
    z_cut_top    = z_top + 1.0
    z_cut_bottom = z_cavity_bottom
    cut_verts = [(x, y, z_cut_bottom) for (x, y) in outline] + \
                [(x, y, z_cut_top) for (x, y) in outline]
    cut_faces = [list(range(n - 1, -1, -1)), list(range(n, 2 * n))]
    for i in range(n):
        j = (i + 1) % n
        cut_faces.append([i, j, n + j, n + i])
    cut_mesh = bpy.data.meshes.new(name + "_cutter_tmp")
    cut_mesh.from_pydata(cut_verts, [], cut_faces)
    cut_mesh.update()
    cut_mesh.validate(verbose=False)
    cutter_obj = _temp_object(name + "_cutter_tmp", cut_mesh)

    for o in bpy.context.selected_objects:
        o.select_set(False)
    block_obj.select_set(True)
    bpy.context.view_layer.objects.active = block_obj

    mod = block_obj.modifiers.new("MoldCut", 'BOOLEAN')
    mod.operation = 'DIFFERENCE'
    mod.object = cutter_obj
    mod.solver = 'EXACT'
    try:
        result = bpy.ops.object.modifier_apply(modifier="MoldCut")
        if 'FINISHED' not in result:
            print(f"[TensileLab] Boolean returned {result}")
    except Exception as exc:
        print(f"[TensileLab] Mold boolean failed: {exc}")

    result_mesh = block_obj.data.copy()
    result_mesh.name = name

    cm = cutter_obj.data
    bpy.data.objects.remove(cutter_obj, do_unlink=True)
    if cm and cm.users == 0:
        bpy.data.meshes.remove(cm)

    bm = block_obj.data
    bpy.data.objects.remove(block_obj, do_unlink=True)
    if bm and bm.users == 0:
        bpy.data.meshes.remove(bm)

    return result_mesh
