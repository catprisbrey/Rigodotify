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

def set_all_ik_stretch_zero(armature):
    if armature and armature.type == 'ARMATURE':
        for pbone in armature.pose.bones:
            if hasattr(pbone, 'ik_stretch'):
                pbone.ik_stretch = 0.0

class GodotMecanim_Panel(bpy.types.Panel):
    bl_label = "Rigify to Godot converter"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "data"

    @classmethod
    def poll(self, context):
        return context.object and context.object.type == 'ARMATURE' and "DEF-spine.005" in bpy.context.object.data.bones

    def draw(self, context):
        self.layout.operator("rig4mec.convert2godot")


class GodotMecanim_Convert2Godot(bpy.types.Operator):
    bl_idname = "rig4mec.convert2godot"
    bl_label = "Prepare rig for Godot"



    def execute(self, context):
        ob = bpy.context.object

        is_animal = context.object.type == 'ARMATURE' and "DEF-tail" in bpy.context.object.data.bones


        bpy.ops.object.mode_set(mode='OBJECT')

        if is_animal : # the root bone is spine.005
            print('is animal')
        if 'root' in ob.data.bones :
            ob.data.bones['root'].use_deform = True
        if 'DEF-breast.L' in ob.data.bones :
            ob.data.bones['DEF-breast.L'].use_deform = True
        if 'DEF-breast.R' in ob.data.bones :
            ob.data.bones['DEF-breast.R'].use_deform = True

        if 'DEF-pelvis.L' in ob.data.bones :
            ob.data.bones['DEF-pelvis.L'].use_deform = False
        if 'DEF-pelvis.R' in ob.data.bones :
            ob.data.bones['DEF-pelvis.R'].use_deform = False



        bpy.ops.object.mode_set(mode='EDIT')

        #if is_animal:
            #check_and_parent('DEF-tail','DEF-spine.004')
            #check_and_parent('DEF-upper_arm.L','DEF-upper_arm.L.001',True)
            #check_and_parent('DEF-forearm.L','DEF-forearm.L.001',True)
            #check_and_parent('DEF-forearm.L','DEF-upper_arm.L.001')
            #check_and_remove('DEF-upper_arm.L.001')
            #check_and_remove('DEF-forearm.L.001')

            #check_and_parent('DEF-forefoot.L','DEF-forearm.L')
            #check_and_parent('DEF-f_toes.L','DEF-forefoot.L')
            #check_and_parent('DEF-f_hoof.L','DEF-f_toes.L')
            #check_and_remove('DEF-forefoot.L.001')

            #check_and_parent('DEF-upper_arm.R','DEF-upper_arm.R.001',True)
            #check_and_parent('DEF-forearm.R','DEF-forearm.R.001',True)
            #check_and_parent('DEF-forearm.R','DEF-upper_arm.R.001')
            #check_and_remove('DEF-upper_arm.R.001')
            #check_and_remove('DEF-forearm.R.001')

            #check_and_parent('DEF-forefoot.R','DEF-forearm.R')
            #check_and_parent('DEF-f_toes.R','DEF-forefoot.R')
            #check_and_parent('DEF-f_hoof.R','DEF-f_toes.R')
            #check_and_remove('DEF-forefoot.R.001')

            #check_and_parent('DEF-shoulder.L','DEF-spine.007')
            #check_and_parent('DEF-shoulder.R','DEF-spine.007')
            #check_and_parent('DEF-upper_arm.L','DEF-shoulder.L')
            #check_and_parent('DEF-upper_arm.R','DEF-shoulder.R')
            #check_and_parent('DEF-thigh.L','DEF-spine.004')
            #check_and_parent('DEF-thigh.R','DEF-spine.004')
            #check_and_parent('DEF-jaw','DEF-spine.009')
            #check_and_parent('DEF-eye.L','DEF-spine.009')
            #check_and_parent('DEF-eye.R','DEF-spine.009')


        #else:
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

        check_and_parent('DEF-hands.L','DEF-hands.L.001',True)
        check_and_parent('DEF-hands.L','DEF-forearm.L.001')
        check_and_parent('DEF-fingers.L','DEF-hands.L.001')
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

        check_and_parent('DEF-hands.R','DEF-hands.R.001',True)
        check_and_parent('DEF-hands.R','DEF-forearm.R.001')
        check_and_parent('DEF-fingers.R','DEF-hands.R.001')
        check_and_parent('DEF-hand.R','DEF-forearm.R')
        check_and_parent('DEF-thumb.01.R','DEF-hand.R')
        check_and_parent('DEF-f_index.01.R','DEF-hand.R')
        check_and_parent('DEF-f_middle.01.R','DEF-hand.R')
        check_and_parent('DEF-f_ring.01.R','DEF-hand.R')
        check_and_parent('DEF-f_pinky.01.R','DEF-hand.R')

        # common bones
        check_and_parent('DEF-thigh.L','DEF-thigh.L.001',True)
        check_and_parent('DEF-shin.L','DEF-shin.L.001',True)
        check_and_parent('DEF-shin.L','DEF-thigh.L.001')
        check_and_parent('DEF-foot.L','DEF-shin.L.001')

        check_and_parent('DEF-feet.L','DEF-feet.L.001',True)
        check_and_parent('DEF-feet.L','DEF-shin.L.001')
        check_and_parent('DEF-toes.L','DEF-feet.L.001')
        check_and_parent('DEF-toe.R','DEF-foot.R.001')
        check_and_remove('DEF-feet.L.001')
        check_and_remove('DEF-hands.L.001')

        check_and_remove('DEF-thigh.L.001')
        check_and_remove('DEF-shin.L.001')
        check_and_remove('DEF-foot.L.001')

        check_and_parent('DEF-thigh.R','DEF-thigh.R.001',True)
        check_and_parent('DEF-shin.R','DEF-shin.R.001',True)
        check_and_parent('DEF-shin.R','DEF-thigh.R.001')
        check_and_parent('DEF-foot.R','DEF-shin.R.001')

        check_and_parent('DEF-feet.R','DEF-feet.R.001',True)
        check_and_parent('DEF-feet.R','DEF-shin.R.001')
        check_and_parent('DEF-toes.R','DEF-feet.R.001')
        check_and_parent('DEF-toe.R','DEF-foot.R.001')
        check_and_remove('DEF-feet.R.001')
        check_and_remove('DEF-hands.R.001')

        check_and_remove('DEF-thigh.R.001')
        check_and_remove('DEF-shin.R.001')
        check_and_remove('DEF-foot.R.001')

        check_and_parent('DEF-breast.L','DEF-spine.003')
        check_and_parent('DEF-breast.R','DEF-spine.003')
        check_and_parent('DEF-tail','DEF-spine')

        ob.name = "godot_rig"

        # Fix some odd parenting issues of failed contraints
        if "DEF-breast.R" in ob.data.edit_bones :
            constraint = bpy.data.objects["godot_rig"].pose.bones["DEF-breast.R"].constraints.new('COPY_TRANSFORMS')
            constraint.target = bpy.data.objects["godot_rig"]
            constraint.subtarget = "breast.R"

        if "DEF-breast.R" in ob.data.edit_bones :
            constraint = bpy.data.objects["godot_rig"].pose.bones["DEF-breast.L"].constraints.new('COPY_TRANSFORMS')
            constraint.target = bpy.data.objects["godot_rig"]
            constraint.subtarget = "breast.L"

        if "DEF-shoulder.R" in ob.data.edit_bones :
            constraint = bpy.data.objects["godot_rig"].pose.bones["DEF-shoulder.R"].constraints.new('COPY_TRANSFORMS')
            constraint.target = bpy.data.objects["godot_rig"]
            constraint.subtarget = "shoulder.R"

        if "DEF-shoulder.L" in ob.data.edit_bones :
            constraint = bpy.data.objects["godot_rig"].pose.bones["DEF-shoulder.L"].constraints.new('COPY_TRANSFORMS')
            constraint.target = bpy.data.objects["godot_rig"]
            constraint.subtarget = "shoulder.L"

        if "DEF-jaw" in ob.data.edit_bones :
            constraint = bpy.data.objects["godot_rig"].pose.bones["DEF-jaw"].constraints.new('COPY_TRANSFORMS')
            constraint.target = bpy.data.objects["godot_rig"]
            constraint.subtarget = "jaw"

        if "DEF-eye.L" in ob.data.edit_bones :
            constraint = bpy.data.objects["godot_rig"].pose.bones["DEF-eye.L"].constraints.new('COPY_TRANSFORMS')
            constraint.target = bpy.data.objects["godot_rig"]
            constraint.subtarget = "eye.L"

        if "DEF-eye.R" in ob.data.edit_bones :
            constraint = bpy.data.objects["godot_rig"].pose.bones["DEF-eye.R"].constraints.new('COPY_TRANSFORMS')
            constraint.target = bpy.data.objects["godot_rig"]
            constraint.subtarget = "eye.R"


        bpy.ops.object.mode_set(mode='OBJECT')

        # fix a few names quick
        if is_animal:
            namelist = [
                ("DEF-spine", "DEF-hips"),
                ("DEF-spine.004","DEF-neck"),
                ("DEF-spine.005", "DEF-head"),
                #("DEF-spine.006", "DEF-spine.002"),
                #("DEF-spine.005", "DEF-spine.001"),
                ("DEF-eye.L", "DEF-ear.L"),
                ("DEF-eye.R", "DEF-ear.R"),
                ("eye.L", "ear.L"),
                ("eye.R", "ear.R")
                ]

        else:
            namelist = [
                ("DEF-spine", "DEF-hips"),
                ("DEF-spine.004","DEF-neck"),
                ("DEF-spine.005", "DEF-head")
                ]

        for name, newname in namelist:
            # get the pose bone with name
            pb = ob.pose.bones.get(name)
            # continue if no bone of that name
            if pb is None:
                continue
            # rename
            pb.name = newname

        reparent_bones_to_metarig_parents()

        # hide all the uncommonly used controls

        collections_to_hide = [
            "Torso (Tweak)",
            "Fingers (Detail)",
            "Torso (Tweak)",
            "Fingers (Detail)",
            "Arm.R (Tweak)",
            "Arm.L (Tweak)",
            "Arm.L (FK)",
            "Arm.R (FK)",
            "Leg.L (Tweak)",
            "Leg.L (FK)",
            "Leg.R (FK)",
            "Leg.R (Tweak)",
            "Spine (Tweak)"
        ]

        for collection_name in collections_to_hide:
            if collection_name in bpy.context.object.data.collections:
                bpy.context.object.data.collections[collection_name].is_visible = False
            else:
                print(f"Collection '{collection_name}' not found.")


        bpy.ops.object.posemode_toggle()
        # Set IK_Stretch property to 0 for specified bones

        set_all_ik_stretch_zero(ob)

        bpy.ops.object.mode_set(mode='OBJECT')
        self.report({'INFO'}, 'Godot ready rig!')

        # Set armature viewport display to 'In Front'
        ob.show_in_front = True

        # Set armature display mode to 'Wire'
        # ob.display_type = 'WIRE'

        return{'FINISHED'}

def reparent_bones_to_metarig_parents():
    # Ensure we harve the active armature and the 'metarig' armature
    godot_rig = bpy.data.objects.get('godot_rig')
    metarig_armature = bpy.data.objects.get('metarig')
    # Ensure we have the active armature and the 'metarig' armature

    # Check if the active object is an armature and 'metarig' exists
    if godot_rig is None or godot_rig.type != 'ARMATURE':
        print("Error: The active object is not an armature.")
        return

    if metarig_armature is None or metarig_armature.type != 'ARMATURE':
        print("Error: 'metarig' armature not found.")
        return
    # EDIT MODE IN GODOT RIG
    bpy.ops.object.mode_set(mode='EDIT')
    # Loop through each bone in the active armature
    print("START BONE LOOP")
    for bone in godot_rig.data.edit_bones:
        # Check if the parent bone name starts with "ORG-" this means is a extra bone
        if bone.parent:
            if bone.parent.name.startswith("ORG-"):
                # Check if the bone name starts with "DEF-" in the active armature
                if bone.name.startswith("DEF-"):
                    # Remove the 'DEF-' prefix to match the corresponding bone name in the 'metarig'
                    active_bone_name = bone.name[4:]

                    # Try to get the corresponding bone from the 'metarig'
                    if active_bone_name in metarig_armature.data.bones:
                        print(f"Bone {active_bone_name} found in 'metarig'.")
                        metarig_bone_name = active_bone_name
                        metarig_bone = metarig_armature.data.bones[metarig_bone_name]

                        # Check the parent of the bone in the 'metarig'
                        if metarig_bone.parent:
                            parent_bone_name = metarig_bone.parent.name
                            #Fix diferent bone names between rigs
                            if parent_bone_name == "spine.005":
                                parent_bone_name = "head"
                            if parent_bone_name == "spine.004":
                                parent_bone_name = "neck"
                            if parent_bone_name == "spine":
                                parent_bone_name = "hips"
                            print(f"PARENT OF {active_bone_name} = {parent_bone_name}.")
                            parent_bone_name = "DEF-" + parent_bone_name
                            # Set the parent of the active armature's bone to match the 'metarig' bone's parent
                            if parent_bone_name in godot_rig.data.bones:
                                active_bone = godot_rig.data.bones[bone.name]
                                parent_bone = godot_rig.data.edit_bones[parent_bone_name]
                                bone.parent = parent_bone
                                print(f"Reparented {bone.name} to {parent_bone_name}")
                                # Constraint the bone to its controller
                                constraint = bpy.data.objects["godot_rig"].pose.bones[bone.name].constraints.new('COPY_TRANSFORMS')
                                constraint.target = bpy.data.objects["godot_rig"]
                                constraint.subtarget = bone.name[4:]

def register():
    #classes
    bpy.utils.register_class(GodotMecanim_Panel)
    bpy.utils.register_class(GodotMecanim_Convert2Godot)


def unregister():
    #classes
    bpy.utils.unregister_class(GodotMecanim_Panel)
    bpy.utils.unregister_class(GodotMecanim_Convert2Godot)
