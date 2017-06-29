# WEFX Naming Convention
## General Rule
- By default, all names with one word should be in lower case
- If a name contains more than two words, do not put a sapce, or any special character, in between words. Use  [lower camel style][1] instead, initial lower case letter. ex. `run cycle` should be `runCycle`, and `Hero Tiger roars` should be `heroTigerRoars`.
- All folder related naming allow only alphabet and digit, except a sequence foler within a episode.
- All name should start with alphabet letter
- Use `_` to separate element
- Use `.` for image sequence and extension
## Project Name
- Abbreviation
- Three letters, only alphabet and digit 
- All upper case
- Examples
    * `TGB`
    * `MYS`
## Episode Name
- Epsiode name format: `ep{##}`, zero-padding with a length of `2`
- Lower case `ep`
- Examples
    * `ep22`, `ep01`, ......., etc.
## Sequence Name
- Sequence name don't require zero-padding, we treat digit as string here.
- Usually abbreviation, when it's in abbreviation form, letters are all in lower case.
- Examples
    * `sc234`
    * `tb`
    * `tigerBite`, rarly we will use words for sequence name, but if it happens, follow [lower camel rule][1]
## Sequence Folder Name
- Sequence Folder Name has an exception if the sequence is within an episode.
- We don't generate folder for episode, instead, we use episode name as a prefix for sequence folder name, separated by `_`
- `Sequence folder` within a Episode will be named in a format of `ep{##}_{sequenceName}`, zero-padding with a length of `2`
- Examples( this naming only affects `sequence folder name` with episode)
    * `ep22_xs`, means this folder contains Episode `22`, Sequence `xs`
## Shot Code
- Shot code format : `{sequenceName}{shotNumber}`
- Shot code contains sequence name and shot number
- Shot number, zero-padding with a length of `4` 
- Keep the last digit 0, it's used only if an insert shot is added
- Examples
    * `md0050`, `md0010`, `xs0100`
    * `xs0105`, when there is a number other than 0 at the last digit, we know that it's an inset shot between xs0100 and xs0110
## Task Name in Shot Level
- By default, task name will use pipeline step name if not specify.
- Examples
    * `aniCar`
    * `lgt`
    * `roto`
    * `roughComp`
    * `lay`
## File Name in Shot Task
- Task name format: `{taskName}_{elements}_{v###}.{ma/mb/abc/hip/zb....}`
- Element is not mandatory
- Use `_` to separate elements.
- File version starts with lower case `v` follow by version number, zero-padding with a length of `3`.
- Examples
    * `lgt_v003.ma`
    * `lgt_v002.ma`
    * `aniCar_v002.ma`
    * `comp_v003.nk`
    * `roto_tiger_v001.nk`
    * `lay_refGeo_v005.abc`
    * `lay_cam_v001.abc`
## Asset Name
- Asset Name should contains short description right after its name, this description is mamdatory
- Examples
    * `tigerHero` or `tigerBaby`, in this case we know these two are different type of tiger assets.
    * `tigerGeneric`, when there is no specific descrition, use `Generic` instead.
## Task Name in Asset Level
- This usually use pipeline step name, if not specify.
- Examples
    * `rig`
    * `tissueRd`
    * `surface`
## File Name in Asset Task
- Task name format: `{assetName}_{taskName}_{elements}_{v###}.{ma/mb/abc/hip/zb....}`.
- Element is not mandatory
- Use `_` to separate elements.
- File version starts with lower case `v` follow by version number, zero-padding with a length of `3`.
- Examples
    * `tiger_rig_skin_v002.ma`
    * `car_model_head_v005.hip`
    * `room_lightRig_main_v002.ma`



[1]:https://en.wikipedia.org/wiki/Camel_case