import maya.cmds as cmds
import sys
import os
from threading import Thread

amn_path = 'w:/yggpiprepo'
if not amn_path in sys.path:
    sys.path.append(amn_path)

import ammonite.package.amnapi.ammonite as ammonite

proj = os.environ['YGG_PROJECT']
ep = os.environ['YGG_EPISODE']
seq = os.environ['YGG_SEQUENCE']
shot = os.environ['YGG_SHOT']

amn = ammonite.Ammonite()
shot_result = amn.search(
        'shot', 
        filters = {
            'project': proj,
            'episode': ep,
            'sequence': seq,
            'shot': shot
        }
    )[0]

sTime = shot_result['cut_in']
eTime = shot_result['cut_out']
sg_duration = shot_result['cut_duration']
scene_duration = int(cmds.playbackOptions(q=1, max=1) - cmds.playbackOptions(q=1, min=1)) + 1

# -------------------------------------------

def setPrePostRoll(*args):
    
    preroll = cmds.intFieldGrp('prerollTx', q=True, v1=True)
    postroll = cmds.intFieldGrp('postrollTx', q=True, v1=True)
    presim = cmds.intFieldGrp('presimTx', q=True, v1=True)
    
    # pre-bake
    cmds.text('progressTx', e=1, l='Pre-baking...')
    cmds.progressBar('progBar', e=1, step = 0, vis=True)
    
    cnstAll = cmds.ls(type = 'constraint')
    cnstRN = cmds.ls(type = 'constraint', rn = True)
    cnstLocal = list(set(cnstAll).difference(set(cnstRN)))
    constrainedCtrl = cmds.listRelatives(cnstLocal, ap = True)
    cmds.bakeResults(constrainedCtrl, t = (sTime, eTime), sb = 1, mr=1, dic=1)
    cmds.delete(cmds.ls(list(set(cnstAll).difference(set(cnstRN)))))
    
    # select all anim nodes
    objCurve = cmds.ls('*:*_ctrl')
    facialCurve = cmds.ls('*:*_Ctrl')
    allCurve = objCurve
    allCurve.extend(facialCurve)
    objCurveCount = len(objCurve)
    
    # trim curve function
    for index, selCurve in enumerate(objCurve):
        progressPercent = (100 * index) / objCurveCount
        cmds.text('progressTx', e=1, l='Keying pre/post-roll...')
        cmds.progressBar('progBar', e=1, step = progressPercent)
        
        keyframes = cmds.keyframe(selCurve, q=True, tc=True)
        if keyframes:
            for time in keyframes:
                if time < sTime: 
                    cmds.cutKey(selCurve, time=(time,time))
                if time > eTime: 
                    cmds.cutKey(selCurve, time=(time,time))
                    
            # get current infinity state
            infState = cmds.setInfinity(selCurve, q=True, pri=True, poi=True)
            cmds.setInfinity(selCurve, pri='linear', poi='linear')
            
            # set start/end outer tangent to follow inner tangent
            if cmds.keyframe(selCurve, q=True, t=(sTime+1, sTime+1)):
                cmds.keyTangent(selCurve, t=(sTime, sTime), itt='spline')
            else:
                cmds.keyTangent(selCurve, t=(sTime, sTime), itt='clamped')
            
            if cmds.keyframe(selCurve, q=True, t=(eTime-1, eTime-1)):
                cmds.keyTangent(selCurve, t=(eTime, eTime), ott='spline')
            else:
                cmds.keyTangent(selCurve, t=(eTime, eTime), ott='clamped')
                
            # key pre/post roll
            cmds.setKeyframe(selCurve, t=(sTime-preroll, sTime-preroll), s=False, i=True)
            cmds.setKeyframe(selCurve, t=(eTime+postroll, eTime+postroll), s=False, i=True)
            
            # set pre/post roll tangent to linear/spline
            cmds.keyTangent(selCurve, t=(sTime-preroll, sTime-preroll), itt='spline', ott='spline')
            cmds.keyTangent(selCurve, t=(eTime+postroll, eTime+postroll), itt='spline', ott='spline')
            
            # set start/end outer tangent to linear
            cmds.keyTangent(selCurve, t=(sTime, sTime), itt='linear')
            cmds.keyTangent(selCurve, t=(eTime, eTime), ott='linear')
            
            # set infinity state to previous
            cmds.setInfinity(selCurve, pri=infState[0], poi=infState[1])

    
    # post-bake
    cmds.text('progressTx', e=1, l='Post-baking...')
    cmds.progressBar('progBar', e=1, step = 1)
    cmds.bakeResults(allCurve, t = (sTime, eTime), sb = 1, mr=1, dic=1, pok=1)
    
    cmds.playbackOptions(ast=sTime-(preroll+presim), aet=eTime+postroll, min=sTime-(preroll+presim), max=eTime+postroll)
    cmds.text('progressTx', e=1, l='Done')
    cmds.progressBar('progBar', e=1, step = 1, vis=False)
    cmds.confirmDialog(t='Done', m='Done', b='OK')
    cmds.text('progressTx', e=1, l='')
    

def start_process(*args):
    thread = Thread(target = setPrePostRoll)
    thread.start()
    
    
def run():
    if cmds.window('prepostrollWin', q=True, exists=True):
        cmds.deleteUI('prepostrollWin')
    
    cmds.window('prepostrollWin', t='Pre/Post-Roll')
    main = cmds.columnLayout(adj=1, rs=5)
    
    cmds.text(l='* Merge anim layer first *')

    cmds.separator(p=main)
    cmds.text(l='Pre-sim assets', al='left', p=main)
    cmds.textScrollList('simAssetsTx', w=250, h=150, p=main, en=False) ###
    btnGrp = cmds.rowLayout(nc=2, p=main)
    cmds.button(l='+ Add pre-sim asset', w=125, p=btnGrp, en=False)
    cmds.button(l='X Remove', w=125, p=btnGrp, en=False)
    
    cmds.separator(style='in', p=main)
    cmds.intFieldGrp('prerollTx', l='Preroll: ', nf=1, cw2=(70,100), v1=10, p=main) ###
    cmds.intFieldGrp('postrollTx', l='Postroll: ', nf=1, cw2=(70,100), v1=10, p=main) ###
    cmds.intFieldGrp('presimTx', l='Pre-sim: +', nf=1, cw2=(70,100), v1=0, p=main) ###

    cmds.separator(style='in', p=main)
    grid221 = cmds.rowColumnLayout(nc=2, p=main)
    cmds.text(l='Scene duration: ', al='right', p=grid221)
    cmds.text('sceneDurTx', l=scene_duration, p=grid221) ###
    cmds.text(l='SG duration: ', al='right', p=grid221)
    cmds.text('sgDurTx', l=sg_duration, p=grid221) ###
    if scene_duration != sg_duration:
        cmds.text('sceneDurTx', e=1, bgc=(1,0,0))
    cmds.button(l='OK', c=setPrePostRoll, p=main)

    cmds.separator(p=main)
    cmds.text('progressTx', l='', p=main)
    cmds.progressBar('progBar', max=100, p=main, vis=False)
    
    cmds.showWindow('prepostrollWin')