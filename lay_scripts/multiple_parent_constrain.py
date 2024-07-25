'''Contraining multiple objects to one target object. The last selected object is the target.'''

import maya.cmds as mc

def run():
    sel = mc.ls(sl = True)
    constrainTo = sel.pop(-1)
    for i in sel:
        mc.parentConstraint(constrainTo, i, mo = True)
