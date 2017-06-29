# WEFX CFX Automation 

## Requirement
+ ### Requrire Smedge submit.exe
    + default location in `C:\Program Files\Smedge\Submit.exe`
    + config file in `config/config.cfg`

+ ### Require Shotgun API Python
    + make sure client side machine is connected to Utitle network drive
    + require internet connection

+ ### Require Python 
    + Python 2.6+

## Incoming Animation File Rules
+ ### Naming
    - `{shotCode}_{taskName}_v{##}.ma`
    - `{ep##}_{shotCode}_{taskName}_v{##}.ma`(If episode exisit)
    - Follwing spec strictly for naming.
    - File type is mayaAscii
    - File name is case-sensitive
    - Version digit contains zero-padding with a length of `2`, letter `v` in lower case.
    - Keep track on file version, do not deliver files with the same name.
+ ### Animation File Content
    - Keep rig file as reference, do not import refernece
    - Don't change reference file name
    - Keep the same file structure between animation file and reference file
    - Do not use animation layers for delivery files
    - Animation Files should contains only keyframe, if use any other tools, special inhouse tools, or extra constraints, keys shoule be baked back to provided rig controllers when delivery.
    - Do not rename any node in provided reference file
    - Clean unused node before delivery files
    - Deliver only animation files in one folder, no sub-folder needed, exclude reference files. Make sure delivery file name compile to naming convention.

## Incoming Animation Playblast for Review
+ ### Naming
    - `{shotCode}_{taskName}_v{##}.mov`
    - `{ep##}_{shotCode}_{taskName}_v{##}.mov`(If episode exisit)
    - File type is mov, codec H.264
    - File name is case-sensitive
    - Version digit contains zero-padding with a length of 2, letter `v` in lower case.
    - Playblast resolution should follow each shot spec, no overscan
    - Playblast should have show frame number, no Safe area or Action safe line    
    - A list of commentary file can be attached with clear indication of which file each commentary belongs to. 
    - If there is no Playblast from provided rendercam
