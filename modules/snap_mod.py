import maya.cmds as cmd
import pymel.core as pm

# input the list of objects, the latest object is the target
def snap(sel):
    target = sel.pop(-1)
    posTarget = pm.xform(target, q = True, t = True, ws = True)
    rotTarget = pm.xform(target, q = True, ro = True, ws = True)
    
    for i in sel:
        pm.xform(i, t = posTarget, ws = True)
        pm.xform(i, ro = rotTarget, ws = True)
