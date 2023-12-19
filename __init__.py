rigify_info = {
    "name": "Godot Rigs",
    "description": "Rigs built with Godot/Unity compatible skeletons in mind.",
    "author": "Cat Prisbrey",
    "warning": "Experimental.",
    # Web site links
    "link": "https://github.com/catprisbrey/Rigodotify",
}
#script to make rigify compatible with Godot humanoid
#HOWTO: right after generating rig using rigify
#	press armature -> Rigify To Godot Converter -> (Prepare rig for Godot) button
bl_info = {
    "name": "Rigodotify",
    "category": "Rigging",
    "description": "Change Rigify rig into a Godot/Unity compatible basic humanoid",
    "location": "At the bottom of Rigify rig data/armature tab",
    "link": "https://github.com/catprisbrey/Rigodotify",
    "blender":(4,0,0)
}

import bpy
import re

def check_and_parent(child_bone,parent_bone,to_tail = False) :
    ob = bpy.context.object

    if child_bone in ob.data.edit_bones and parent_bone in ob.data.edit_bones:
        if to_tail:
            ob.data.edit_bones[child_bone].tail = ob.data.edit_bones[parent_bone].tail
        else:
            ob.data.edit_bones[child_bone].parent = ob.data.edit_bones[parent_bone]

def check_and_remove(bone_name) :
    ob = bpy.context.object
    if bone_name in ob.data.edit_bones :
        ob.data.edit_bones.remove(ob.data.edit_bones[bone_name])

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
        
        check_and_parent('DEF-shoulder.L','DEF-spine.003')
        check_and_parent('DEF-shoulder.R','DEF-spine.003')
        check_and_parent('DEF-upper_arm.L','DEF-shoulder.L')
        check_and_parent('DEF-upper_arm.R','DEF-shoulder.R')
        check_and_parent('DEF-thigh.L','DEF-spine')
        check_and_parent('DEF-thigh.R','DEF-spine')
        check_and_parent('DEF-jaw','DEF-spine.005')
        check_and_parent('DEF-eye.L','DEF-spine.005')
        check_and_parent('DEF-eye.R','DEF-spine.005')


        check_and_parent('DEF-upper_arm.L','DEF-upper_arm.L.001',True)
        check_and_parent('DEF-forearm.L','DEF-forearm.L.001',True)
        check_and_parent('DEF-forearm.L','DEF-upper_arm.L.001')
        check_and_remove('DEF-upper_arm.L.001')
        check_and_remove('DEF-forearm.L.001')

        check_and_parent('DEF-hand.L','DEF-forearm.L')
        check_and_parent('DEF-thumb.01.L','DEF-hand.L')
        check_and_parent('DEF-f_index.01.L','DEF-hand.L')
        check_and_parent('DEF-f_middle.01.L','DEF-hand.L')
        check_and_parent('DEF-f_ring.01.L','DEF-hand.L')
        check_and_parent('DEF-f_pinky.01.L','DEF-hand.L')

        check_and_parent('DEF-upper_arm.R','DEF-upper_arm.R.001',True)
        check_and_parent('DEF-forearm.R','DEF-forearm.R.001',True)
        check_and_parent('DEF-forearm.R','DEF-upper_arm.R.001')
        check_and_remove('DEF-upper_arm.R.001')
        check_and_remove('DEF-forearm.R.001')


        check_and_parent('DEF-hand.R','DEF-forearm.R')
        check_and_parent('DEF-thumb.01.R','DEF-hand.L')
        check_and_parent('DEF-f_index.01.R','DEF-hand.R')
        check_and_parent('DEF-f_middle.01.R','DEF-hand.R')
        check_and_parent('DEF-f_ring.01.R','DEF-hand.R')
        check_and_parent('DEF-f_pinky.01.R','DEF-hand.R')

        check_and_parent('DEF-thigh.L','DEF-thigh.L.001',True)
        check_and_parent('DEF-shin.L','DEF-shin.L.001',True)
        check_and_parent('DEF-shin.L','DEF-thigh.L.001')
        check_and_parent('DEF-foot.L','DEF-shin.L.001')
        check_and_remove('DEF-thigh.L.001')
        check_and_remove('DEF-shin.L.001')


        check_and_parent('DEF-thigh.R','DEF-thigh.LR.001',True)
        check_and_parent('DEF-shin.R','DEF-shin.R.001',True)
        check_and_parent('DEF-shin.R','DEF-thigh.R.001')
        check_and_parent('DEF-foot.R','DEF-shin.R.001')
        check_and_remove('DEF-thigh.R.001')
        check_and_remove('DEF-shin.R.001')

        check_and_parent('DEF-breast.L','DEF-spine.003')
        check_and_parent('DEF-breast.R','DEF-spine.003')

        #if 'DEF-pelvis.L' in ob.data.bones :
        #    ob.data.edit_bones.remove(ob.data.edit_bones['DEF-pelvis.L'])
        #if 'DEF-pelvis.R' in ob.data.bones :
        #    ob.data.edit_bones.remove(ob.data.edit_bones['DEF-pelvis.R'])

        #if 'DEF-breast.L' in ob.data.bones :
        #    ob.data.edit_bones.remove(ob.data.edit_bones['DEF-breast.L'])
        #if 'DEF-breast.R' in ob.data.bones :
        #    ob.data.edit_bones.remove(ob.data.edit_bones['DEF-breast.R'])

        bpy.ops.object.mode_set(mode='OBJECT')

        # fix a few names quick
        namelist = [("DEF-spine", "DEF-hips"),("DEF-spine.004","DEF-neck"),("DEF-spine.005", "DEF-head")]

        for name, newname in namelist:
            # get the pose bone with name
            pb = ob.pose.bones.get(name)
            # continue if no bone of that name
            if pb is None:
                continue
            # rename
            pb.name = newname


        # Remove "DEF-" from every deform bone name
        #bpy.ops.object.mode_set(mode='EDIT')

        #for edit_bone in ob.data.edit_bones:
        #    if edit_bone.name.startswith("DEF-"):
        #        edit_bone.name = edit_bone.name[len("DEF-"):]

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
