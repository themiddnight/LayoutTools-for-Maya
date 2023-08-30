'''The intuitive tool for keying parent and unparenting.'''

import pymel.core as pm

def setParrentAnimUI():
    if pm.window('setParrentAnimWin', exists = True):
        pm.deleteUI('setParrentAnimWin')
        
    mainWin = pm.window('setParrentAnimWin', t = 'Set Parent Keyframe')
    with mainWin:
        mainLay = pm.columnLayout(adj = True, rs = 5, cat = ('both',5))
        with mainLay:
            pm.text(l = 'Select "parent" object, then "child" object')
            pm.button(l = 'Parent', c = doParent)
            pm.text('Select "child" object')
            pm.button(l = 'Un-parent', c = unParent)
    pm.showWindow('setParrentAnimWin')

def doParent(*args):
    sel = pm.ls(sl = True)
    currFrame = pm.currentTime()
    pm.parentConstraint(sel[0], sel[1], mo = True)
    pm.setKeyframe(sel[1])
    blendParentName = pm.listAttr(sel[1], st = 'blendParent*')
    pm.setAttr('%s.%s' %(sel[1],blendParentName[0]), 1)
    pm.setKeyframe('%s.%s' %(sel[1],blendParentName[0]))
    pm.currentTime(currFrame - 1)
    pm.setAttr('%s.%s' %(sel[1],blendParentName[0]), 0)
    pm.setKeyframe(sel[1])
    pm.currentTime(currFrame)

def unParent(*args):
    sel = pm.ls(sl = True)
    blendParentName = pm.listAttr(sel[0], st = 'blendParent*')
    pm.setKeyframe(sel[0])
    currFrame = pm.currentTime()
    pm.currentTime(currFrame + 1)
    pm.setAttr('%s.%s' %(sel[0],blendParentName[0]), 0)
    pm.setKeyframe(sel[0])
    
def run():
    setParrentAnimUI()
