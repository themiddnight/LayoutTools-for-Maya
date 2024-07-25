import maya.cmds as cmds

def offsetKeyframe(offset, start=None, end=None):
    curves = cmds.ls(type='animCurve')
    keys = cmds.keyframe(curves, q=True, tc=True)
    if start == None:
        start = min(keys)
    if end == None:
        end = max(keys)
    cmds.keyframe(curves, e=True, t=(start, end), relative=True, tc=offset)
