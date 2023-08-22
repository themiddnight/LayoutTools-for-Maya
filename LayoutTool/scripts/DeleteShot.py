import pymel.core as pm
import maya.cmds as cmds
from LayoutTool.modules import getSortedShotLs_mod
reload(getSortedShotLs_mod)
    
def blockShotKey():
    shotLs = getSortedShotLs_mod.getShotLs()
    curves = pm.ls(type = 'animCurve')
    time = []
    for i in shotLs:
        time.append(pm.shot(i, q = True, st = True))
        time.append(pm.shot(i, q = True, et = True))
    time.sort()
    for i in time:
        pm.setKeyframe(curves, t = (i), s = False, i = True)

def deleteKeys(start, end):
    curves = pm.ls(type = 'animCurve')                
    for i in curves:
        pm.cutKey(i, time = [start, end], clear = True)

def getShotAfter(selected_shot):
    shot_list = getSortedShotLs_mod.getShotLs()
    # Find the index of the selected shot
    selected_index = None
    for i, shot in enumerate(shot_list):
        if shot == selected_shot:
            selected_index = i
            break
    # Extract the shots that come after the selected shot
    shots_after = shot_list[selected_index:] if selected_index is not None else []
    return shots_after
    
def shiftShotsAfter(firstShot, offset):
    shotsAfter = getShotAfter(firstShot)
    for i in shotsAfter:
        st = pm.shot(i, q = True, st = True)
        sst = pm.shot(i, q = True, sst = True)
        et = pm.shot(i, q = True, et = True)
        set = pm.shot(i, q = True, set = True)
        newSt = st - offset
        newSst = sst - offset
        newEt = et - offset
        newSet = set - offset
        pm.shot(i, e = True, st = newSt)
        pm.shot(i, e = True, sst = newSst)
        pm.shot(i, e = True, et = newEt)
        pm.shot(i, e = True, set = newSet)

def offsetKeys(start, end, offset):
    curves = pm.ls(type = 'animCurve')
    pm.selectKey(curves, time = (start, end), replace = True)
    pm.keyframe(animation = 'keys', option = 'over', e = True, relative = True, tc = -offset)

########################### Remove shots, Unload/remove camera

def run():
    continueCheck = 1
    selShots = pm.ls(sl = True, type = 'shot')
    if selShots:
        confirm = pm.confirmDialog(message = "If remove camera reference, it won't be undoable", button = ['Remove', 'Unload', 'Cancel'])
        if confirm == 'Cancel':
            pass
        else:
            for i in selShots:
                shotsAfter = getShotAfter(i)
                cam = pm.shot(i, q = True, cc = True)
                duration = pm.shot(i, q = True, sd = True)
                try:
                    refNode = pm.referenceQuery(cam, referenceNode = True)
                    if confirm == 'Remove':
                        print 'remove ' + refNode
                        cmds.file(rfn = refNode, removeReference = True)
                    elif confirm == 'Unload':
                        print 'unload ' + refNode
                        cmds.file(rfn = refNode, unloadReference = True)
                    pm.delete(i)
                except:
                    pm.delete(i)
    else:
        removeGapCon = pm.confirmDialog(message = 'No shot selected. Continue to check shots gap?', button = ['OK', 'Cancel'])
        if removeGapCon == 'Cancel':
            continueCheck = 0
        
    ############################## Find gaps and shift keys and shots
    
    if continueCheck == 1:
        blockShotKey()
        shots = getSortedShotLs_mod.getShotLs()
        firstShotFrame = pm.shot(shots[0], q = True, st = True)
        if firstShotFrame != 1001: # if it's first shot
            offset = firstShotFrame - 1001
            endSeqFrame = pm.shot(shots[-1], q = True, et = True)
            
            deleteKeys(1001, firstShotFrame - 1)
            offsetKeys(firstShotFrame, endSeqFrame, offset)
            shiftShotsAfter(shots[0], offset)
        
        for i in range(len(shots)):
            endSeqFrame = pm.shot(shots[-1], q = True, et = True) # iterate
            if shots[i] == shots[-1]: # if last shot, do nothing
                pass
            else:
                frameA = pm.shot(shots[i], q = True, et = True) # end frame of before gap
                frameB = pm.shot(shots[i+1], q = True, st = True) # start frame of after gap
                offset = frameB - frameA
                if offset > 1:
                    deleteKeys(frameA + 1, frameB - 1)
                    offsetKeys(frameB, endSeqFrame, offset - 1)
                    shiftShotsAfter(shots[i+1], offset - 1)