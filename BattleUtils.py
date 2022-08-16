bl_info = {
    'name': 'BattleUtils',
    'blender': (3, 2, 2),
    'category': 'Tools',
    'version': (0, 0, 0),
    'author': 'Disnejar',
    'description': 'A script to help picture simple battles in blender',
}

import bpy
import bmesh
from mathutils import Vector


def add_object():

    if bpy.context.object is not None:
        bpy.ops.object.mode_set(mode = 'OBJECT')
    

    bpy.ops.mesh.primitive_cylinder_add(enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(0.5, 0.5, 0.05))
    me = bpy.context.object.data
    
    bm = bmesh.new()
    bm.from_mesh(me)
    
    i = 1
    while i < 64:
        bm.verts.ensure_lookup_table()
        bm.verts[i].co.x *= 0.85
        bm.verts[i].co.y *= 0.85
        i += 2
        
    co = Vector()
    co.x = bm.verts[1].co.x
    co.y = bm.verts[1].co.y
    co.z = bm.verts[1].co.z + 1.8
    bm.verts.new(co)
    bm.verts.ensure_lookup_table()
    
    co = Vector()
    co.x = bm.verts[33].co.x
    co.y = bm.verts[33].co.y
    co.z = bm.verts[33].co.z + 1.8
    bm.verts.new(co)
    bm.verts.ensure_lookup_table()
    
    bm.faces.new([bm.verts[1], bm.verts[64], bm.verts[65], bm.verts[33]])
        
    bm.to_mesh(me)
    bm.free()
    
    
def color_base(type):
    if type not in bpy.data.materials:
        mat = bpy.data.materials.new(name=type)
        if type is "Enemy":
            mat.diffuse_color = (0.8, 0.0, 0.0, 1.0)
        elif type is "Neutral":
            mat.diffuse_color = (0.1, 0.1, 0.1, 1.0)
        elif type is "Friend":
            mat.diffuse_color = (0.0, 0.8, 0.0, 1.0)
        
    if "Material" not in bpy.data.materials:
        mat = bpy.data.materials.new(name="Material")
        
    bpy.context.object.data.materials.append(bpy.data.materials["Material"])
    
    bpy.context.object.data.materials.append(bpy.data.materials[type])
        
    for i in range( len( bpy.context.object.data.polygons ) ):
        if i is not 30 and i is not 34:
            bpy.context.object.data.polygons[i].material_index = 1


class BATTLEUTILS_OT_spawn_enemy(bpy.types.Operator):
    bl_idname = "battleutils.spawn_enemy"
    bl_options = {'REGISTER', 'UNDO'}
    
    bl_label = "Enemy"
    bl_description = "Spawn one enemy unit"
    
    def execute(self, context):
        add_object()
        color_base("Enemy")
        
        return {'FINISHED'}
    

class BATTLEUTILS_OT_spawn_friendly(bpy.types.Operator):
    bl_idname = "battleutils.spawn_friendly"
    bl_options = {'REGISTER', 'UNDO'}
    
    bl_label = "Friendly"
    bl_description = "Spawn one friendly unit"
    
    def execute(self, context):
        add_object()
        color_base("Friend")
        
        return {'FINISHED'}
    
    
class BATTLEUTILS_OT_spawn_neutral(bpy.types.Operator):
    bl_idname = "battleutils.spawn_neutral"
    bl_options = {'REGISTER', 'UNDO'}
    
    bl_label = "Neutral"
    bl_description = "Spawn one neutral unit"
    
    def execute(self, context):
        add_object()
        color_base("Neutral")
        
        return {'FINISHED'}

    

class BATTLEUTILS_PT_spawn_panel(bpy.types.Panel):
    bl_idname = "BATTLEUTILS_PT_spawn_panel"
    bl_label = "Spawn Menu"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "BattleUtils"
    
    def draw(self, context):
        row = self.layout.row(align=True)
        row.operator(BATTLEUTILS_OT_spawn_enemy.bl_idname, text=BATTLEUTILS_OT_spawn_enemy.bl_label)
        row.operator(BATTLEUTILS_OT_spawn_friendly.bl_idname, text=BATTLEUTILS_OT_spawn_friendly.bl_label)
        row.operator(BATTLEUTILS_OT_spawn_neutral.bl_idname, text=BATTLEUTILS_OT_spawn_neutral.bl_label)


PROPS = [
    #All properties/property groups
]

CLASSES = [
    #All used classes
    BATTLEUTILS_OT_spawn_enemy,
    BATTLEUTILS_OT_spawn_friendly,
    BATTLEUTILS_OT_spawn_neutral,
    BATTLEUTILS_PT_spawn_panel
    
]

def register():
    for klass in CLASSES:
        bpy.utils.register_class(klass)
        
    for (prop_name, prop_value) in PROPS:
        setattr(bpy.types.Scene, prop_name, prop_value)


def unregister():
    bpy.utils.unregister_class(DICEY_GT_result)
    for klass in CLASSES:
        bpy.utils.unregister_class(klass)


if __name__ == '__main__':
    register()
