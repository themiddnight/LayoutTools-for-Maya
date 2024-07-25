'''Delete selected shot with removing animation keys, assigned camera, and shift frames and shots after the deleted.'''

import sys, os
path = os.environ['layout_tool_path'] + '/lay_modules/'
if path not in sys.path: sys.path.append(path)

import maya.cmds as mc
import get_sorted_shot_list_mod
# try:
#     reload(get_sorted_shot_list_mod)
# except:
#     import importlib
#     importlib.reload(get_sorted_shot_list_mod)
    
def blockShotKey():
    shotLs = get_sorted_shot_list_mod.getShotLs()
    curves = mc.ls(type = 'animCurve')
    time = []
    for i in shotLs:
        time.append(mc.shot(i, q = True, st = True))
        time.append(mc.shot(i, q = True, et = True))
    time.sort()
    for i in time:
        mc.setKeyframe(curves, t = (i), s = False, i = True)

def deleteKeys(start, end):
    curves = mc.ls(type = 'animCurve')                
    for i in curves:
        mc.cutKey(i, time = [start, end], clear = True)

def getShotAfter(selected_shot):
    shot_list = get_sorted_shot_list_mod.getShotLs()
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
        st = mc.shot(i, q = True, st = True)
        sst = mc.shot(i, q = True, sst = True)
        et = mc.shot(i, q = True, et = True)
        set = mc.shot(i, q = True, set = True)
        newSt = st - offset
        newSst = sst - offset
        newEt = et - offset
        newSet = set - offset
        mc.shot(i, e = True, st = newSt)
        mc.shot(i, e = True, sst = newSst)
        mc.shot(i, e = True, et = newEt)
        mc.shot(i, e = True, set = newSet)

def offsetKeys(start, end, offset):
    curves = mc.ls(type = 'animCurve')
    mc.selectKey(curves, time = (start, end), replace = True)
    mc.keyframe(animation = 'keys', option = 'over', e = True, relative = True, tc = -offset)

########################### Remove shots, Unload/remove camera

def run():
    continueCheck = 1
    selShots = mc.ls(sl = True, type = 'shot')
    if selShots:
        confirm = mc.confirmDialog(message = "If remove camera reference, it won't be undoable", button = ['Remove', 'Unload', 'Cancel'])
        if confirm == 'Cancel':
            pass
        else:
            for i in selShots:
                shotsAfter = getShotAfter(i)
                cam = mc.shot(i, q = True, cc = True)
                duration = mc.shot(i, q = True, sd = True)
                try:
                    refNode = mc.referenceQuery(cam, referenceNode = True)
                    if confirm == 'Remove':
                        print ('remove ' + refNode)
                        mc.file(rfn = refNode, removeReference = True)
                    elif confirm == 'Unload':
                        print ('unload ' + refNode)
                        mc.file(rfn = refNode, unloadReference = True)
                    mc.delete(i)
                except:
                    mc.delete(i)
    else:
        removeGapCon = mc.confirmDialog(message = 'No shot selected. Continue to check shots gap?', button = ['OK', 'Cancel'])
        if removeGapCon == 'Cancel':
            continueCheck = 0
        
    ############################## Find gaps and shift keys and shots
    
    if continueCheck == 1:
        blockShotKey()
        shots = get_sorted_shot_list_mod.getShotLs()
        firstShotFrame = mc.shot(shots[0], q = True, st = True)
        if firstShotFrame != 1001: # if it's first shot
            offset = firstShotFrame - 1001
            endSeqFrame = mc.shot(shots[-1], q = True, et = True)
            
            deleteKeys(1001, firstShotFrame - 1)
            offsetKeys(firstShotFrame, endSeqFrame, offset)
            shiftShotsAfter(shots[0], offset)
        
        for i in range(len(shots)):
            endSeqFrame = mc.shot(shots[-1], q = True, et = True) # iterate
            if shots[i] == shots[-1]: # if last shot, do nothing
                pass
            else:
                frameA = mc.shot(shots[i], q = True, et = True) # end frame of before gap
                frameB = mc.shot(shots[i+1], q = True, st = True) # start frame of after gap
                offset = frameB - frameA
                if offset > 1:
                    deleteKeys(frameA + 1, frameB - 1)
                    offsetKeys(frameB, endSeqFrame, offset - 1)
                    shiftShotsAfter(shots[i+1], offset - 1)