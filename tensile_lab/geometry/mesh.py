import bpy


def build_mesh_data(name, outline, thickness):
    n = len(outline)
    z0, z1 = -thickness / 2.0, thickness / 2.0
    verts = [(x, y, z0) for (x, y) in outline] + [(x, y, z1) for (x, y) in outline]
    faces = [list(range(n - 1, -1, -1)), list(range(n, 2 * n))]
    for i in range(n):
        j = (i + 1) % n
        faces.append([i, j, n + j, n + i])
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    mesh.validate(verbose=False)
    return mesh


def create_object(name, mesh):
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    return obj


def select_only(obj):
    for o in bpy.context.selected_objects:
        o.select_set(False)
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
