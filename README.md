<h1 align="left">Rigodotify</h1>

###

<p align="left">A dual purpose Rigify feature set and Blender rig converter plugin. Recently reworked to add compatibilty across all major game engine retargeters: Godot, Unity, and Unreal standards are used to make retargeters autodetect bone structure and more happily share animations across models.

Rigs can be converted in a button press to make them game engine compatible. Convert the rig before parenting it to your mesh and your model will be ready for animating for games!

Bonus animal rigs based off Rigify for: Canid, Felid, Equid animal bodies.(Experimental)</p>

###
<h2 align="left">Purpose:</h2>


<p align="left">Skeletons and rigs used for game development are distinct to those used for animation. They tend to be placed in T-Pose, have far fewer bones, and a hierarchical bone order. This makes animations more efficient for processing and also aids in animation transferring to other characters, and keeping in-engine IKs working as expected.

This plugin and feature set produces standard Godot, Unity and Unreal skeletons  with extra Rigify bones removed, the bone order fixed, and friendlier names given for mapping them in engine.​ Leaf bones are added for Unreal, and constraints adjusted to minimize scale errors, and animation jitters in engines.</p>


<h2 align="left">Installation:</h2>

###

<p align="left">https://youtu.be/QYx2mYBL3T8<br><br>This ZIP file is both a plugin AND a Rigify feature set. You install it in two places of the Add-ons window.<br><br><br>1. Enabled Rigify:<br>- Open Blender's preferences<br>- Select Add-Ons<br>- Enable Rigify plugin<br><br>2. Install the Godot feature set<br>- Open the Rigify drop down<br>- Install Feature Set<br>- Select the Rigodotify.zip file<br><br>3. Install the rig converter plugin:<br>- In Blender's Add-ons again<br>- Select "Install"<br>- Select the Rigodotify.zip file again<br>- Enable the Rigodotify plugin</p>

###

<div align="center">
  <img height="640" src="https://github.com/catprisbrey/Rigodotify/blob/master/HowTo/install_plugin_and_featureset.gif?raw=true"  />
</div>

###

<h2 align="left">Usage:</h2>

###

<p align="left">- Add an Armature as you would through the normal menus.<br>- Select the new armature option "Godot Human"<br>- Make adjustments to scale, and position as needed<br>- From the Armature menu select "Generate Rig"<br>- With the new Rig selected, click the "Prepare Rig for Godot" button<br>- Parent the game dev compatible rig to your meshes as you normally would.</p>

###

<br clear="both">

<div align="center">
  <img height="640" src="https://github.com/catprisbrey/Rigodotify/blob/master/HowTo/metarig_and_rig.gif?raw=true"  />
</div>

###

<h2 align="left">Differences:</h2>

###

<p align="left">Side by side of the Rigify standard metarig skeleton compared to the Godot metarig skeleton</p>

###

<div align="center">
  <img height="640" src="https://github.com/catprisbrey/Rigodotify/blob/master/HowTo/metarig-differences.png?raw=true"  />
</div>

###

<p align="left">Below is the new bone structure and naming scheme.</p>

###

root<br/>-pelvis<br/>--spine_01<br/>---spine_02<br/>----spine_03<br/>-----breast_l<br/>-----breast_r<br/>-----clavicle_l<br/>------upperarm_l<br/>-------lowerarm_l<br/>--------hand_l<br/>---------index_01_l<br/>----------index_02_l<br/>-----------index_03_l<br/>------------index_04_leaf_l<br/>---------middle_01_l<br/>----------middle_02_l<br/>-----------middle_03_l<br/>------------middle_04_leaf_l<br/>---------pinky_01_l<br/>----------pinky_02_l<br/>-----------pinky_03_l<br/>------------pinky_04_leaf_l<br/>---------ring_01_l<br/>----------ring_02_l<br/>-----------ring_03_l<br/>------------ring_04_leaf_l<br/>---------thumb_01_l<br/>----------thumb_02_l<br/>-----------thumb_03_l<br/>------------thumb_04_leaf_l<br/>-----clavicle_r<br/>------upperarm_r<br/>-------lowerarm_r<br/>--------hand_r<br/>---------index_01_r<br/>----------index_02_r<br/>-----------index_03_r<br/>------------index_04_leaf_r<br/>---------middle_01_r<br/>----------middle_02_r<br/>-----------middle_03_r<br/>------------middle_04_leaf_r<br/>---------pinky_01_r<br/>----------pinky_02_r<br/>-----------pinky_03_r<br/>------------pinky_04_leaf_r<br/>---------ring_01_r<br/>----------ring_02_r<br/>-----------ring_03_r<br/>------------ring_04_leaf_r<br/>---------thumb_01_r<br/>----------thumb_02_r<br/>-----------thumb_03_r<br/>------------thumb_04_leaf_r<br/>-----neck_01<br/>------Head<br/>-------Jaw<br/>-------eye_l<br/>-------eye_r<br/>--thigh_l<br/>---calf_l<br/>----foot_l<br/>-----ball_l<br/>------ball_leaf_l<br/>--thigh_r<br/>---calf_r<br/>----foot_r<br/>-----ball_r<br/>------ball_leaf_r






###

<h2 align="left">Built in:</h2>

###

<div align="left">
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/blender/blender-original.svg" height="40" alt="blender logo"  />
  <img width="12" />
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg" height="40" alt="python logo"  />
</div>

###
