rigify_info = {
    "name": "Godot Rigs",
    "description": "Rigs built with Godot compatible skeletons in mind.",
    "author": "Cat Prisbrey",
    "warning": "Experimental.",
    # Web site links
    "link": "https://github.com/catprisbrey/Rigify-To-Godot",
}
#script to make rigify compatible with Godot humanoid
#HOWTO: right after generating rig using rigify
#	press armature -> Rigify To Godot Converter -> (Prepare rig for Godot) button
bl_info = {
    "name": "Rigify to Godot",
    "category": "Rigging",
    "description": "Change Rigify rig into a Godot compatible the basic humanoid",
    "location": "At the bottom of Rigify rig data/armature tab",
    "blender":(2,80,0)
}

import bpy
import re


class GodotMecanim_Panel(bpy.types.Panel):
    bl_label = "Rigify to Godot converter"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "data"

    @classmethod
    def poll(self, context):
        return context.object.type == 'ARMATURE' and "DEF-upper_arm.L.001" in bpy.context.object.data.bones
    
    def draw(self, context):
        self.layout.operator("rig4mec.convert2godot")
        
        
class GodotMecanim_Convert2Godot(bpy.types.Operator):
    bl_idname = "rig4mec.convert2godot"
    bl_label = "Prepare rig for Godot"
    
    def execute(self, context):
        ob = bpy.context.object
        
        bpy.ops.object.mode_set(mode='OBJECT')

        if 'DEF-breast.L' in ob.data.bones :
            ob.data.bones['DEF-breast.L'].use_deform = False
        if 'DEF-breast.R' in ob.data.bones :
            ob.data.bones['DEF-breast.R'].use_deform = False

        if 'DEF-pelvis.L' in ob.data.bones :
            ob.data.bones['DEF-pelvis.L'].use_deform = False
        if 'DEF-pelvis.R' in ob.data.bones :
            ob.data.bones['DEF-pelvis.R'].use_deform = False

        bpy.ops.object.mode_set(mode='EDIT')
        
        ob.data.edit_bones['DEF-shoulder.L'].parent = ob.data.edit_bones['DEF-spine.003']
        ob.data.edit_bones['DEF-shoulder.R'].parent = ob.data.edit_bones['DEF-spine.003']
        
        ob.data.edit_bones['DEF-upper_arm.L'].parent = ob.data.edit_bones['DEF-shoulder.L']
        ob.data.edit_bones['DEF-upper_arm.R'].parent = ob.data.edit_bones['DEF-shoulder.R']
        
        ob.data.edit_bones['DEF-thigh.L'].parent = ob.data.edit_bones['DEF-spine']
        ob.data.edit_bones['DEF-thigh.R'].parent = ob.data.edit_bones['DEF-spine']

        ob.data.edit_bones['DEF-jaw'].parent = ob.data.edit_bones['DEF-spine.006']
        ob.data.edit_bones['DEF-eye.L'].parent = ob.data.edit_bones['DEF-spine.006']
        ob.data.edit_bones['DEF-eye.R'].parent = ob.data.edit_bones['DEF-spine.006']

        ob.data.edit_bones['DEF-upper_arm.L'].tail = ob.data.edit_bones['DEF-upper_arm.L.001'].tail
        ob.data.edit_bones['DEF-forearm.L'].tail = ob.data.edit_bones['DEF-forearm.L.001'].tail
        ob.data.edit_bones['DEF-forearm.L'].parent = ob.data.edit_bones['DEF-upper_arm.L.001'].parent
        ob.data.edit_bones['DEF-hand.L'].parent = ob.data.edit_bones['DEF-forearm.L.001'].parent
        ob.data.edit_bones['DEF-palm.01.L'].parent = ob.data.edit_bones['DEF-hand.L']
        ob.data.edit_bones.remove(ob.data.edit_bones['DEF-upper_arm.L.001'])
        ob.data.edit_bones.remove(ob.data.edit_bones['DEF-forearm.L.001'])

        ob.data.edit_bones['DEF-upper_arm.R'].tail = ob.data.edit_bones['DEF-upper_arm.R.001'].tail
        ob.data.edit_bones['DEF-forearm.R'].tail = ob.data.edit_bones['DEF-forearm.R.001'].tail
        ob.data.edit_bones['DEF-forearm.R'].parent = ob.data.edit_bones['DEF-upper_arm.R.001'].parent
        ob.data.edit_bones['DEF-hand.R'].parent = ob.data.edit_bones['DEF-forearm.R.001'].parent
        ob.data.edit_bones['DEF-palm.01.R'].parent = ob.data.edit_bones['DEF-hand.R']
        ob.data.edit_bones.remove(ob.data.edit_bones['DEF-upper_arm.R.001'])
        ob.data.edit_bones.remove(ob.data.edit_bones['DEF-forearm.R.001'])

        ob.data.edit_bones['DEF-thigh.L'].tail = ob.data.edit_bones['DEF-thigh.L.001'].tail
        ob.data.edit_bones['DEF-shin.L'].tail = ob.data.edit_bones['DEF-shin.L.001'].tail
        ob.data.edit_bones['DEF-shin.L'].parent = ob.data.edit_bones['DEF-thigh.L.001'].parent
        ob.data.edit_bones['DEF-foot.L'].parent = ob.data.edit_bones['DEF-shin.L.001'].parent
        ob.data.edit_bones.remove(ob.data.edit_bones['DEF-thigh.L.001'])
        ob.data.edit_bones.remove(ob.data.edit_bones['DEF-shin.L.001'])

        ob.data.edit_bones['DEF-thigh.R'].tail = ob.data.edit_bones['DEF-thigh.R.001'].tail
        ob.data.edit_bones['DEF-shin.R'].tail = ob.data.edit_bones['DEF-shin.R.001'].tail
        ob.data.edit_bones['DEF-shin.R'].parent = ob.data.edit_bones['DEF-thigh.R.001'].parent
        ob.data.edit_bones['DEF-foot.R'].parent = ob.data.edit_bones['DEF-shin.R.001'].parent
        ob.data.edit_bones.remove(ob.data.edit_bones['DEF-thigh.R.001'])
        ob.data.edit_bones.remove(ob.data.edit_bones['DEF-shin.R.001'])

        if 'DEF-pelvis.L' in ob.data.bones :
            ob.data.edit_bones.remove(ob.data.edit_bones['DEF-pelvis.L'])
        if 'DEF-pelvis.R' in ob.data.bones :
            ob.data.edit_bones.remove(ob.data.edit_bones['DEF-pelvis.R'])

        if 'DEF-breast.L' in ob.data.bones :
            ob.data.edit_bones.remove(ob.data.edit_bones['DEF-breast.L'])
        if 'DEF-breast.R' in ob.data.bones :
            ob.data.edit_bones.remove(ob.data.edit_bones['DEF-breast.R'])

        bpy.ops.object.mode_set(mode='OBJECT')

        # fix a few names quick
        namelist = [("DEF-spine", "DEF-hips"),("DEF-spine.005","DEF-neck"),("DEF-spine.006", "DEF-head")]

        for name, newname in namelist:
            # get the pose bone with name
            pb = ob.pose.bones.get(name)
            # continue if no bone of that name
            if pb is None:
                continue
            # rename
            pb.name = newname


        # Remove "DEF-" from every deform bone name
        bpy.ops.object.mode_set(mode='EDIT')

        for edit_bone in ob.data.edit_bones:
            if edit_bone.name.startswith("DEF-"):
                edit_bone.name = edit_bone.name[len("DEF-"):]

        bpy.ops.object.mode_set(mode='OBJECT')
        self.report({'INFO'}, 'Godot ready rig!')

        # Set armature viewport display to 'In Front'
        ob.show_in_front = True

        # Set armature display mode to 'Wire'
        ob.display_type = 'WIRE'

        ob.name = "godot_rig"

        return{'FINISHED'}

def register():
    #classes     
    bpy.utils.register_class(GodotMecanim_Panel)
    bpy.utils.register_class(GodotMecanim_Convert2Godot)

    
def unregister():
    #classes
    bpy.utils.unregister_class(GodotMecanim_Panel)
    bpy.utils.unregister_class(GodotMecanim_Convert2Godot)
