'''The intuitive tool for keying parent and unparenting.'''

# import pymel.core as pm
import maya.cmds as mc

def doParent(*args):
    sel = mc.ls(sl = True)
    currFrame = mc.currentTime(q=True)
    mc.parentConstraint(sel[0], sel[1], mo = True)
    mc.setKeyframe(sel[1])
    blendParentName = mc.listAttr(sel[1], st = 'blendParent*')
    mc.setAttr('%s.%s' %(sel[1],blendParentName[0]), 1)
    mc.setKeyframe('%s.%s' %(sel[1],blendParentName[0]))
    mc.currentTime(currFrame - 1)
    mc.setAttr('%s.%s' %(sel[1],blendParentName[0]), 0)
    mc.setKeyframe(sel[1])
    mc.currentTime(currFrame)

def unParent(*args):
    sel = mc.ls(sl = True)
    blendParentName = mc.listAttr(sel[0], st = 'blendParent*')
    mc.setKeyframe(sel[0])
    currFrame = mc.currentTime(q=True)
    mc.currentTime(currFrame + 1)
    mc.setAttr('%s.%s' %(sel[0],blendParentName[0]), 0)
    mc.setKeyframe(sel[0])

def run():
    if mc.window('setParrentAnimWin', exists = True):
        mc.deleteUI('setParrentAnimWin')
        
    mainWin = mc.window('setParrentAnimWin', t = 'Set Parent Keyframe')
    # with mainWin:
    mainLay = mc.columnLayout(adj = True, rs = 5, cat = ('both',5))
    # with mainLay:
    mc.text(l = 'Select "parent" object, then "child" object')
    mc.button(l = 'Parent', c = doParent)
    mc.text('Select "child" object')
    mc.button(l = 'Un-parent', c = unParent)

    mc.showWindow('setParrentAnimWin')