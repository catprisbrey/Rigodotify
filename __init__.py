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
import mathutils

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

def remove_all_drivers_and_stretch_constraints(armature_obj):
    # Remove drivers only for DEF bones
    if armature_obj.animation_data:
        for fcurve in list(armature_obj.animation_data.drivers):
            if 'pose.bones["DEF-' in fcurve.data_path:
                armature_obj.animation_data.drivers.remove(fcurve)

    for bone in armature_obj.pose.bones:
        # Skip hips
        if bone.name.startswith("DEF-"):
            # Remove "Stretch To" constraints
            stretch_constraints = [c for c in bone.constraints if c.type == 'STRETCH_TO']
            for c in stretch_constraints:
                bone.constraints.remove(c)

            if bone.name != "DEF-hips":
                # Replace "Copy Transforms" with "Copy Rotation"
                copy_transform_constraints = [c for c in bone.constraints if c.type == 'COPY_TRANSFORMS']
                for ct in copy_transform_constraints:
                    new_constraint = bone.constraints.new('COPY_ROTATION')
                    new_constraint.target = ct.target
                    new_constraint.subtarget = ct.subtarget
                    bone.constraints.remove(ct)

            # Add Limit Scale constraint
            limit_scale = bone.constraints.new('LIMIT_SCALE')
            limit_scale.use_min_x = True
            limit_scale.use_min_y = True
            limit_scale.use_min_z = True
            limit_scale.use_max_x = True
            limit_scale.use_max_y = True
            limit_scale.use_max_z = True
            limit_scale.min_x = 1.0
            limit_scale.min_y = 1.0
            limit_scale.min_z = 1.0
            limit_scale.max_x = 1.0
            limit_scale.max_y = 1.0
            limit_scale.max_z = 1.0

            # Special case: thigh or shin
            if "thigh" in bone.name.lower() or "shin" in bone.name.lower():
                limit_scale.use_transform_limit = True
                limit_scale.owner_space = 'LOCAL'

## Adding leaf bones to fingers and toes in order to make Unreal happy
def add_leaf_bones_for_fingers_and_toes(armature_obj):
    bpy.context.view_layer.objects.active = armature_obj
    bpy.ops.object.mode_set(mode='EDIT')
    edit_bones = armature_obj.data.edit_bones

    added_bone_names = []

    for bone in edit_bones:
        name = bone.name.lower()
        is_finger_tip = name.startswith("def-") and (name.endswith(".03.l") or name.endswith(".03.r"))
        is_toe_tip = name in {"def-toe.l", "def-toe.r"}

        if not (is_finger_tip or is_toe_tip):
            continue

        if bone.name.endswith(".L") or bone.name.endswith(".R"):
            base = bone.name[:-2]
            side = bone.name[-2:]
            leaf_name = f"{base}.end{side}"
        else:
            leaf_name = bone.name + ".end"

        if leaf_name in edit_bones:
            continue

        leaf_bone = edit_bones.new(leaf_name)
        leaf_bone.head = bone.tail.copy()

        direction = (bone.tail - bone.head).normalized()
        offset = direction * 0.05
        leaf_bone.tail = bone.tail + offset

        leaf_bone.parent = bone
        leaf_bone.use_connect = True

        added_bone_names.append(leaf_name)

    bpy.ops.object.mode_set(mode='POSE')

    ## Add these end leaf bones to the DEF group
    def_collection = armature_obj.data.collections.get("DEF")
    if def_collection:
        for name in added_bone_names:
            bone = armature_obj.data.bones.get(name)
            if bone:
                def_collection.assign(bone)

def rename_for_unreal(ob,is_animal):
        if is_animal:
            return
        namelist = [
        ("DEF-hips", "pelvis"),
        ("DEF-spine.001","spine_01"),
        ("DEF-spine.002","spine_02"),
        ("DEF-spine.003","spine_03"),
        ("DEF-neck","neck_01"),
        ("DEF-head", "head"),
        ("DEF-jaw", "mouth"),
        ("DEF-eye.L", "eye_l"),
        ("DEF-eye.R", "eye_r"),
        ("DEF-shoulder.L", "clavicle_l"),
        ("DEF-shoulder.R", "clavicle_r"),
        ("DEF-upper_arm.L","upperarm_l"),
        ("DEF-upper_arm.R","upperarm_r"),
        ("DEF-forearm.L","lowerarm_l"),
        ("DEF-forearm.R","lowerarm_r"),
        ("DEF-hand.L","hand_l"),
        ("DEF-hand.R","hand_r"),
        #left hand
        ("DEF-f_index.01.L","index_01_l"),
        ("DEF-f_index.02.L","index_02_l"),
        ("DEF-f_index.03.L","index_03_l"),
        ("DEF-f_middle.01.L","middle_01_l"),
        ("DEF-f_middle.02.L","middle_02_l"),
        ("DEF-f_middle.03.L","middle_03_l"),
        ("DEF-f_ring.01.L","ring_01_l"),
        ("DEF-f_ring.02.L","ring_02_l"),
        ("DEF-f_ring.03.L","ring_03_l"),
        ("DEF-f_pinky.01.L","pinky_01_l"),
        ("DEF-f_pinky.02.L","pinky_02_l"),
        ("DEF-f_pinky.03.L","pinky_03_l"),
        ("DEF-thumb.01.L","thumb_01_l"),
        ("DEF-thumb.02.L","thumb_02_l"),
        ("DEF-thumb.03.L","thumb_03_l"),
        # right hand
        ("DEF-f_index.01.R", "index_01_r"),
        ("DEF-f_index.02.R", "index_02_r"),
        ("DEF-f_index.03.R", "index_03_r"),
        ("DEF-f_middle.01.R", "middle_01_r"),
        ("DEF-f_middle.02.R", "middle_02_r"),
        ("DEF-f_middle.03.R", "middle_03_r"),
        ("DEF-f_ring.01.R", "ring_01_r"),
        ("DEF-f_ring.02.R", "ring_02_r"),
        ("DEF-f_ring.03.R", "ring_03_r"),
        ("DEF-f_pinky.01.R", "pinky_01_r"),
        ("DEF-f_pinky.02.R", "pinky_02_r"),
        ("DEF-f_pinky.03.R", "pinky_03_r"),
        ("DEF-thumb.01.R", "thumb_01_r"),
        ("DEF-thumb.02.R", "thumb_02_r"),
        ("DEF-thumb.03.R", "thumb_03_r"),
        ("DEF-breast.L", "breast_l"),
        ("DEF-breast.R", "breast_r"),
        ("DEF-thigh.L", "thigh_l"),
        ("DEF-thigh.R", "thigh_r"),
        ("DEF-shin.L", "calf_l"),
        ("DEF-shin.R", "calf_r"),
        ("DEF-foot.L", "foot_l"),
        ("DEF-foot.R", "foot_r"),
        ("DEF-toe.L", "ball_l"),
        ("DEF-toe.R", "ball_r")
        ]

        for name, newname in namelist:
            # get the pose bone with name
            pb = ob.pose.bones.get(name)
            # continue if no bone of that name
            if pb is None:
                continue
            # rename
            pb.name = newname

def remove_invalid_drivers_from_armature(armature_obj):
    # Save the current context (area and space data)
    current_area = bpy.context.area
    current_ui_type = current_area.ui_type  # Track the current UI section type (e.g., 'DOPESHEET', '3D', etc.)

    # Switch to the 'DRIVERS' editor context
    bpy.context.area.ui_type = 'DRIVERS'

    # Execute the invalid driver cleanup
    bpy.ops.graph.driver_delete_invalid()

    # Return the context to its original state
    current_area.ui_type = current_ui_type

    # Toggle Pose Mode if needed (if armature was in Pose Mode before)
    bpy.ops.object.posemode_toggle()


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

        ## For unreal, rename the rig "Armature"


        is_animal = context.object.type == 'ARMATURE' and "DEF-tail" in bpy.context.object.data.bones


        bpy.ops.object.mode_set(mode='OBJECT')

        ## For unreal, rename the rig "Armature"
        ob.name = "Armature"
        ob.data.name = "Armature"

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

        remove_all_drivers_and_stretch_constraints(ob)
        add_leaf_bones_for_fingers_and_toes(ob)
        rename_for_unreal(ob,is_animal)
        remove_invalid_drivers_from_armature(ob)

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
