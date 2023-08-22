# To bake the animation of outer ctrl to inner ctrl
# Select 'placement_ctrl', set time range and run
### ENDDESCRIPTION

import pymel.core as pm

def doBakeToOffset(*args):
    sel = pm.ls(sl = True)
    nsLs = []
    for i in sel:
        nsLs.append(i.split(':')[0])
    nsLs = list(dict.fromkeys(nsLs))
    
    startTime = pm.intFieldGrp('bakeRange_fld', q = True, v1 = True)
    endTime = pm.intFieldGrp('bakeRange_fld', q = True, v2 = True)
    for i in nsLs:
        currTime = pm.currentTime(q = True)
    	pm.currentTime(startTime)
    	ns = i
    	placementCtrl = pm.ls('%s:placement_ctrl' %ns)
    	offsetCtrl = pm.ls('%s:offset_ctrl' %ns)
    	pos = pm.xform(offsetCtrl, q = True, t = True, ws = True)
    	rotY = pm.xform(offsetCtrl, q = True, ro = True, ws = True)[1]
    	tempLoc = pm.spaceLocator(n = 'temp_loc')
        
    	pm.parentConstraint(offsetCtrl, tempLoc, mo = False)
    	pm.bakeResults(tempLoc, t = (startTime, endTime), sb = 1)
        
    	pm.cutKey(placementCtrl)
    	pm.xform(placementCtrl, t = pos, ws = True)
    	pm.xform(placementCtrl, ro = [0,rotY,0], ws = True)
        
    	pm.parentConstraint(tempLoc, offsetCtrl, mo = False)
    	pm.bakeResults(offsetCtrl, t = (startTime, endTime), sb = 1)
    	
    	pm.delete(tempLoc)
    	pm.currentTime(currTime)
	
def bakeToOffsetUI():
    if pm.window('bakeToOffsetWin', exists = True):
        pm.deleteUI('bakeToOffsetWin')
    pm.window('bakeToOffsetWin', t = 'Bake placement to offset', mxb = False, w = 100)
    pm.columnLayout(adj = True, rs = 8, cat = ['both', 10])
    
    pm.text(l = "Select any asset's controller")
    pm.intFieldGrp('bakeRange_fld', cw = (1, 70), nf = 2, l = 'Start/End: ', v1 = 1001, v2 = 1100)
    pm.button(l = 'Bake', c = doBakeToOffset)
    
    pm.showWindow('bakeToOffsetWin')
    
def run():
    bakeToOffsetUI()
