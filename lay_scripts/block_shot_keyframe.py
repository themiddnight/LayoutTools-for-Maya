'''Set keyframe to selected objects at start and end of every shot.'''

import maya.cmds as mc

def run():
    shotLs = mc.ls(type = 'shot')
    curves = mc.ls(sl = True)
    print(curves)
    time = []
    for i in shotLs:
        time.append(mc.shot(i, q = True, st = True))
        time.append(mc.shot(i, q = True, et = True))
    time.sort()
    for i in time:
        mc.setKeyframe(curves, t = (i), s = False, i = True)

