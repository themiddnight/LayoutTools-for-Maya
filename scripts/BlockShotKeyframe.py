'''Set keyframe to selected objects at start and end of every shot.'''

import pymel.core as pm

def run():
    shotLs = pm.ls(type = 'shot')
    curves = pm.ls(sl = True)
    time = []
    for i in shotLs:
        time.append(pm.shot(i, q = True, st = True))
        time.append(pm.shot(i, q = True, et = True))
    time.sort()
    for i in time:
        pm.setKeyframe(curves, t = (i), s = False, i = True)

