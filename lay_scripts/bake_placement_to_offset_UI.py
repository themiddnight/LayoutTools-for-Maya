'''To bake the animation of outer ctrl to inner ctrl.
Select 'placement_ctrl', set time range and run.'''

import maya.cmds as mc

def doBakeToOffset(*args):
    sel = mc.ls(sl = True)
    nsLs = []
    for i in sel:
        nsLs.append(i.split(':')[0])
    nsLs = list(dict.fromkeys(nsLs))
    
    startTime = mc.intFieldGrp('bakeRange_fld', q = True, v1 = True)
    endTime = mc.intFieldGrp('bakeRange_fld', q = True, v2 = True)
    for i in nsLs:
        currTime = mc.currentTime(q = True)
        mc.currentTime(startTime)
        ns = i
        placementCtrl = mc.ls('%s:placement_ctrl' %ns)
        offsetCtrl = mc.ls('%s:offset_ctrl' %ns)
        pos = mc.xform(offsetCtrl, q = True, t = True, ws = True)
        rotY = mc.xform(offsetCtrl, q = True, ro = True, ws = True)[1]
        tempLoc = mc.spaceLocator(n = 'temp_loc')
        
        mc.parentConstraint(offsetCtrl, tempLoc, mo = False)
        mc.bakeResults(tempLoc, t = (startTime, endTime), sb = 1)
        
        mc.cutKey(placementCtrl)
        mc.xform(placementCtrl, t = pos, ws = True)
        mc.xform(placementCtrl, ro = [0,rotY,0], ws = True)
        
        mc.parentConstraint(tempLoc, offsetCtrl, mo = False)
        mc.bakeResults(offsetCtrl, t = (startTime, endTime), sb = 1)
        
        mc.delete(tempLoc)
        mc.currentTime(currTime)
	
def run():
    if mc.window('bakeToOffsetWin', exists = True):
        mc.deleteUI('bakeToOffsetWin')
    mc.window('bakeToOffsetWin', t = 'Bake placement to offset', mxb = False, w = 100)
    mc.columnLayout(adj = True, rs = 8, cat = ['both', 10])
    
    mc.text(l = "Select any asset's controller")
    mc.intFieldGrp('bakeRange_fld', cw = (1, 70), nf = 2, l = 'Start/End: ', v1 = 1001, v2 = 1100)
    mc.button(l = 'Bake', c = doBakeToOffset)
    
    mc.showWindow('bakeToOffsetWin')