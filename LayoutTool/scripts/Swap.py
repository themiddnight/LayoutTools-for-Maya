import maya.cmds as cmd

def run():
    sel = cmd.ls(sl = True)
    pos0 = cmd.xform(sel[0], q = True, t = True, ws = True)
    rot0 = cmd.xform(sel[0], q = True, ro = True, ws = True)
    pos1 = cmd.xform(sel[1], q = True, t = True, ws = True)
    rot1 = cmd.xform(sel[1], q = True, ro = True, ws = True)

    cmd.xform(sel[0], t = pos1, ws = True)
    cmd.xform(sel[0], ro = rot1, ws = True)
    cmd.xform(sel[1], t = pos0, ws = True)
    cmd.xform(sel[1], ro = rot0, ws = True)
