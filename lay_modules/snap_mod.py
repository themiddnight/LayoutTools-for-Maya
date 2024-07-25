import maya.cmds as mc

# input the list of objects, the latest object is the target
def snap(sel):
    target = sel.pop(-1)
    posTarget = mc.xform(target, q = True, t = True, ws = True)
    rotTarget = mc.xform(target, q = True, ro = True, ws = True)
    
    for i in sel:
        mc.xform(i, t = posTarget, ws = True)
        mc.xform(i, ro = rotTarget, ws = True)
