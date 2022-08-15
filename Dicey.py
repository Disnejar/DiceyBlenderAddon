bl_info = {
    'name': 'Dicey',
    'blender': (3, 2, 2),
    'category': 'Tools',
    'version': (0, 0, 1),
    'author': 'Disnejar',
    'description': 'A built in RPG dice roller. Can be used for picturing D&D fights in blender',
}

import random
import bpy

class DICEY_OT_roll(bpy.types.Operator):
    bl_idname = "dicey.roll"
    bl_options = {'REGISTER', 'UNDO'}
    
    bl_label = "Roll"
    bl_description = "Roll the selected dice"
    
    def execute(self, context):
        context.scene.results.clear()
        
        for i in range(context.scene.dice.d2):
            result = context.scene.results.add()
            result.dice = "d2"
            result.value = random.randrange(1, 3)
            
        for i in range(context.scene.dice.d3):
            result = context.scene.results.add()
            result.dice = "d3"
            result.value = random.randrange(1, 4)
            
        for i in range(context.scene.dice.d4):
            result = context.scene.results.add()
            result.dice = "d4"
            result.value = random.randrange(1, 5)
            
        for i in range(context.scene.dice.d6):
            result = context.scene.results.add()
            result.dice = "d6"
            result.value = random.randrange(1, 7)
            
        for i in range(context.scene.dice.d8):
            result = context.scene.results.add()
            result.dice = "d8"
            result.value = random.randrange(1, 9)
            
        for i in range(context.scene.dice.d10):
            result = context.scene.results.add()
            result.dice = "d10"
            result.value = random.randrange(1, 11)
            
        for i in range(context.scene.dice.d12):
            result = context.scene.results.add()
            result.dice = "d12"
            result.value = random.randrange(1, 13)
            
        for i in range(context.scene.dice.d20):
            result = context.scene.results.add()
            result.dice = "d20"
            result.value = random.randrange(1, 21)
            
        for i in range(context.scene.dice.d100):
            result = context.scene.results.add()
            result.dice = "d100"
            result.value = random.randrange(1, 101)
        
        return {'FINISHED'}
    

class DICEY_PT_dice_panel(bpy.types.Panel):
    bl_idname = "DICEY_PT_dice_panel"
    bl_label = "Dice Selection"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Dicey"
    
    def draw(self, context):
        
        row = self.layout.row(align=True)
        
        col = row.column(align=True)
        col.prop(context.scene.dice, "d2")
        col.prop(context.scene.dice, "d4")
        col.prop(context.scene.dice, "d8")
        col.prop(context.scene.dice, "d12")
        col.prop(context.scene.dice, "d100")
        
        col = row.column(align=True)
        col.prop(context.scene.dice, "d3")
        col.prop(context.scene.dice, "d6")
        col.prop(context.scene.dice, "d10")
        col.prop(context.scene.dice, "d20")
        
        row = self.layout.row()
        row.prop(context.scene, "modifier")
        
        row = self.layout.row()
        row.operator('dicey.roll')

    
class DICEY_PT_results_panel(bpy.types.Panel):
    bl_idname = "DICEY_PT_dices_panel"
    bl_label = "Results"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Dicey"
    
    def draw(self, context):
        modifier = context.scene.modifier
        
        lastDie = None
        resultString = ""
        resultStringMod = ""
        currentResults = []
        sum = 0
        modSum = 0
        modDieSum = 0
        
        col = self.layout.column(align=True)
        
        for result in context.scene.results:
            if lastDie == None:
                lastDie = result.dice
            
            if result.dice != lastDie:
                
                for res in currentResults:
                    resultString = resultString + str(res) + ", "
                    modDieSum = modDieSum + modifier
                    modSum = modSum + modifier
                
                resultString = resultString.removesuffix(", ")
                
                row = col.row(align=True)
                
                box = row.box()
                box.label(text=lastDie + ":")
                
                box = row.box()
                box.scale_x = 2.0
                box.label(text="["+resultString+"]")
                
                box = row.box()
                box.label(text="+"+str(modDieSum))
                
                currentResults = []
                resultString = ""
                modDieSum = 0
                
            currentValue = result.value
            
            currentResults.append(result.value)
            
            lastDie = result.dice
            
            sum = sum + result.value
                
        for res in currentResults:
            resultString = resultString + str(res) + ", "
            modDieSum = modDieSum + modifier
            modSum = modSum + modifier

        resultString = resultString.removesuffix(", ")
                
        row = col.row(align=True)
        
        box = row.box()
        box.label(text=lastDie + ":")
        
        box = row.box()
        box.scale_x = 2.0
        box.label(text="["+resultString+"]")
        
        box = row.box()
        box.label(text="+"+str(modDieSum))
        
        row = self.layout.row(align=True)
        box = row.box()
        box.label(text="Sum:")
        
        box = row.box()
        box.scale_x = 2.0
        box.label(text=str(sum))
        
        box = row.box()
        box.label(text="+" + str(modSum))


class DICEY_GT_result(bpy.types.PropertyGroup):
    dice: bpy.props.StringProperty(name="dice", default="error")
    value: bpy.props.IntProperty(name="value", default=0)
    
    
class DICEY_GT_dice(bpy.types.PropertyGroup):
    d2: bpy.props.IntProperty(name="d2", default=0)
    d3: bpy.props.IntProperty(name="d3", default=0)
    d4: bpy.props.IntProperty(name="d4", default=0)
    d6: bpy.props.IntProperty(name="d6", default=0)
    d8: bpy.props.IntProperty(name="d8", default=0)
    d10: bpy.props.IntProperty(name="d10", default=0)
    d12: bpy.props.IntProperty(name="d12", default=0)
    d20: bpy.props.IntProperty(name="d20", default=0)
    d100: bpy.props.IntProperty(name="d100", default=0)

PROPS = [
    ('dice', bpy.props.PointerProperty(type=DICEY_GT_dice)),
    ('results', bpy.props.CollectionProperty(type=DICEY_GT_result)),
    ('modifier', bpy.props.IntProperty(name="Modifier", default=0))
]

CLASSES = [
    DICEY_GT_result,
    DICEY_GT_dice,
    DICEY_OT_roll,
    DICEY_PT_dice_panel,
    DICEY_PT_results_panel
]

def register():
    print("registered")
    
    for klass in CLASSES:
        bpy.utils.register_class(klass)
        
    for (prop_name, prop_value) in PROPS:
        setattr(bpy.types.Scene, prop_name, prop_value)


def unregister():
    print("unregistered")
    bpy.utils.unregister_class(DICEY_GT_result)
    for klass in CLASSES:
        bpy.utils.unregister_class(klass)


if __name__ == '__main__':
    register()
