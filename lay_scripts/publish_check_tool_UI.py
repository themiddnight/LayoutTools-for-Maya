'''For checking and validating scene before publish.'''

# import pymel.core as pm
import maya.cmds as mc
import re
import sys 
from lay_app.lay_app_core import LayoutToolCore
sys.path.append("W:\yggpipe\lay\modules")

core = LayoutToolCore()

# select constrained ctrl for baking
def selConstrainedCtrl(*args):
    core.logPubCheckData('PUB_41-checkConstrain')
    cnstAll = mc.ls(type = 'constraint')
    cnstRN = mc.ls(type = 'constraint', rn = True)
    cnstLocal = list(set(cnstAll).difference(set(cnstRN)))
    mc.select(cl = True)
    mc.select(mc.listRelatives(cnstLocal, ap = True))

# clean FXguide
def cleanFxGuide(*args):
    core.logPubCheckData('PUB_2-cleanFxGuide')
    fxItems = mc.listRelatives('fxmarker_GRP', ad = True)
    for i in fxItems:
        try:
            lyr = mc.listConnections(i, type = "displayLayer")
            for j in lyr:
                mc.disconnectAttr('%s.drawInfo' %j, '%s.drawOverride' %i)
                print('Remove "%s" from "%s" layer.' %(i, j))
        except:
            pass

    group_name = 'fxmarker_GRP'
    # Get all objects in the group and its descendants
    objects = mc.ls(group_name, dag=True, type='transform')
    
    # Iterate over each object
    for obj in objects:
        # Get all connected nodes
        connected_nodes = mc.listConnections(obj, connections=True, plugs=True)
        
        try:
            # Remove namespace from the object itself
            if ':' in obj:
                obj_name = obj.split(':')[-1]
                mc.rename(obj, obj_name)
            
            # Remove namespace from connected nodes
            if connected_nodes:
                for node in connected_nodes:
                    if ':' in node:
                        node_name = node.split(':')[-1]
                        mc.rename(node, node_name)
        except:
            pass
    mc.confirmDialog(t = 'Report', m = 'fxguide is cleared', b = 'OK')

# check sequencer and camera
def doCheckSeqCamName(*args):
    core.logPubCheckData('PUB_3-checkSeqCamName')
    import getSortedShotLs_mod
    reload(getSortedShotLs_mod)
    
    
    shots = getSortedShotLs_mod.getShotLs()
    shotNodeNamePattern = r'^shot\d+$'
    correct = 1
    for shot in shots:
        if re.search(shotNodeNamePattern, str(shot)):
            #print str(shot) + ' is cottect'
            pass
        else:
            #print str(shot) + ' is not cottect'
            correct = 0
            break
    
    n = 1
    for shot in shots:
        shotName = mc.shot(shot, q = True, sn = True)
        mc.rename(shot, 'shotTemp%d' %n)
        mc.shot(shot, e = True, sn = shotName)
        n += 1
        
    n = 1
    for shot in shots:
        shotName = mc.shot(shot, q = True, sn = True)
        mc.rename(shot, 'shot%d' %n)
        mc.shot(shot, e = True, sn = shotName)
        n += 1
        
    
    #######################################    
    
    shots = getSortedShotLs_mod.getShotLs()
    errorCheck = 0
    noMatchLs = 'These shots are not match with the camera name:\n\n'
    wrongScaleLs = 'These shots frame number are not match:\n\n'
    for shot in shots:
        camName = mc.shot(shot, q = True, cc = True).split(':')[0]
        shotName = mc.shot(shot, q = True, sn = True)
        if camName != shotName:
            noMatchLs += "- %s\n" %shotName
            errorCheck += 1
        st = mc.shot(shot, q = True, st = True)
        sst = mc.shot(shot, q = True, sst = True)
        et = mc.shot(shot, q = True, et = True)
        set = mc.shot(shot, q = True, set = True)
        if st != sst or et != set:
            wrongScaleLs += "- %s\n" %shotName
            errorCheck += 1
    if errorCheck != 0:    
        mc.confirmDialog(t = 'Report', m = '%s\n\n%s' %(noMatchLs, wrongScaleLs) , b = 'OK')
    else:
        mc.confirmDialog(t = 'Report', m = 'Sequencer is clear', b = 'OK')

# bake constrained ctrl
def doBakeConstrainedCtrl(*args):
    core.logPubCheckData('PUB_42-bakeConstrain')
    startTime = mc.intFieldGrp('bakeRange_fld', q = True, v1 = True)
    endTime = mc.intFieldGrp('bakeRange_fld', q = True, v2 = True)
    cnstAll = mc.ls(type = 'constraint')
    cnstRN = mc.ls(type = 'constraint', rn = True)
    sel = mc.ls(sl = True)
    mc.bakeResults(sel, t = (startTime, endTime), sb = 1)
    mc.delete(mc.ls(list(set(cnstAll).difference(set(cnstRN)))))

# list shake ctrl
def listShake(*args):
    shakeCtrlLs = mc.ls('*:shake_ctrl')
    for i in shakeCtrlLs:  # find shaked ctrl
        if i.getAttr('shake3D' %i) == 1:
            mc.textScrollList('cam_ls', e = True, append = i.split(':')[0])
            
# bake shake
def doBake(*args):
    core.logPubCheckData('PUB_5-bakeCamShake')
    import sys 
    sys.path.append("W:\yggpipe\lay\modules")
    import bakeCamShake_mod
    reload(bakeCamShake_mod)
    
    targetOption = mc.radioButtonGrp('bakeTo_rdo', q = True, sl = True)
    camLs = mc.textScrollList('cam_ls', q = True, si = True)
    
    # prepare variables
    for shotName in camLs:
        for i in mc.ls(typ = 'shot'): # find shot of selected camera
            if mc.shot(i, q = True, sn = True) == shotName:
                startTime = mc.getAttr('%s.startFrame' %i)
                endTime = mc.getAttr('%s.endFrame' %i)
                #print i, startTime, endTime
                
        bakeCamShake_mod.bakeCamShake(shotName, startTime, endTime, targetOption)
           
        mc.textScrollList('cam_ls', e = True, ra = True)
        listShake()
    
def doSetAllKey(*args):
    core.logPubCheckData('PUB_6-checkAnimCurve')
    mc.select(cl = True)
    
    # key on empty keyed assets/cams
    keyTime = 1001
    charPLs = mc.ls('char*:placement_ctrl')
    propPLs = mc.ls('prop*:placement_ctrl')
    camPLs = mc.listRelatives('cam')
    assetPLs = []
    for i in charPLs:
        assetPLs.append(i.split(':')[0])
    for i in propPLs:
        assetPLs.append(i.split(':')[0])
    for i in camPLs:
        assetPLs.append(i.split(':')[0])
        
    for i in assetPLs:
        ctrls = mc.ls('%s:*_ctrl' %i)
        isKeyFrame = False
        for ctrl in ctrls:
            ctrl = mc.PyNode(ctrl)
            if mc.keyframe(ctrl, q = True, index = True):
                isKeyFrame = True
                break
        
        if not isKeyFrame:
            isKeyed = True
            keyCtrl = '%s:offset_ctrl' %i
            mc.setKeyframe(keyCtrl, shape = False, time = [keyTime, keyTime+1])
            
        else:
            isKeyed = False
    
    # variables
    shots = mc.ls(typ = 'shot')
    curves = mc.ls(type = 'animCurve')
    time = []
    for i in shots:
        time.append(mc.shot(i, q = True, st = True))
        time.append(mc.shot(i, q = True, et = True))
    time.sort()
    
    # -----------------------------------------------------------
    
    # trim curve function
    def trimCurves(objCurve, sTime, eTime):
        for selCurve in objCurve:
            keyframes = mc.keyframe(selCurve, q = True, tc = True)
            for time in keyframes:
                if time < sTime:
                    mc.cutKey(selCurve, time = (time,time))
                if time > eTime:
                    mc.cutKey(selCurve, time = (time,time))
                    
    # add pre/post roll function
    def addPrePostRoll(objCurve, sTime, eTime):
        for selCurve in objCurve:
            if mc.keyframe(selCurve, q = True, index = True):
                # get current infinity state
                infState = mc.setInfinity(selCurve, q = True, pri = True, poi = True)
                # set start/end outer tangent to follow inner tangent
                mc.keyTangent(selCurve, t = (sTime,sTime), itt = 'clamped')
                mc.keyTangent(selCurve, t = (eTime,eTime), ott = 'clamped')
                # set infinity
                mc.setInfinity(selCurve, pri = 'linear', poi = 'linear')
                # key pre/post roll
                mc.setKeyframe(selCurve, t = (sTime-5,sTime-5), s = False, i = True)
                mc.setKeyframe(selCurve, t = (eTime+5,eTime+5), s = False, i = True)
                # set pre/post roll tangent to linear/spline
                mc.keyTangent(selCurve, t = (sTime-5,sTime-5), itt = 'spline', ott = 'spline')
                mc.keyTangent(selCurve, t = (eTime+5,eTime+5), itt = 'spline', ott = 'spline')
                # set start/end tangent to linear/spline
                mc.keyTangent(selCurve, t = (sTime,sTime), itt = 'linear')
                mc.keyTangent(selCurve, t = (eTime,eTime), ott = 'linear')
                # set infinity state to previous
                mc.setInfinity(selCurve, pri = infState[0], poi = infState[1])
    
    # -----------------------------------------------------------
    
    # key block shot every exists curve
    for i in time:
        mc.setKeyframe(curves, t = (i), s = False, i = True)
        
    # trim overall keyframe
    sTime = time[0]
    eTime = time[-1]
    trimCurves(curves, sTime, eTime)
                
    # trim cam keyframe
    for i in shots:
        sTime = mc.shot(i, q = True, st = True)
        eTime = mc.shot(i, q = True, et = True)
        cam = mc.shot(i, q = True, cc = True)
        shotName = cam.split(':')[0]
        camCtrls = mc.ls('%s:*_ctrl' %shotName)
        trimCurves(camCtrls, sTime, eTime)
        addPrePostRoll(camCtrls, sTime, eTime)
        
def run():
    filename = mc.file(q = True, sn = True)
    match = re.search('publish', filename) #########
    if True:
        time = []
        shots = mc.ls(typ = 'shot')
        for i in shots:
            time.append(mc.shot(i, q = True, st = True))
            time.append(mc.shot(i, q = True, et = True))
        time.sort()
        sTime = time.pop(0)
        eTime = time.pop(-1)
        
        if mc.window('preparePublishWin', exists = True):
            mc.deleteUI('preparePublishWin')
        mc.window('preparePublishWin', t = 'Prepare Scene for Publish', mxb = False, w = 100)
        
        mc.columnLayout(adj = True, rs = 8, cat = ['both', 10])
        mc.separator(style = 'none')
        
        mc.text(al = 'left', l = '1. Please clear your displayLayer visibility and animLayers.', ww = True)
        mc.separator(style = 'in')
        
        mc.text(al = 'left', l = '2. Remove FXguide from layers and namespaces.', ww = True)
        mc.text(al = 'left', l = 'Note: Please check your current namespace is "root". Go to Windows > General Editors > Namespace Editor.', ww = True)
        mc.button(l = 'Clean FXguide', c = cleanFxGuide)
        mc.separator(style = 'in')
        
        mc.text(al = 'left', l = '3. Check sequencer shots and camera name.')
        mc.button(l = 'Check Shots and Cameras', c = doCheckSeqCamName)
        mc.separator(style = 'in')
        
        mc.text(al = 'left', l = '4. Bake constrained ctrl.')
        mc.button(l = 'Check Constrained Ctrl', c = selConstrainedCtrl)
        mc.intFieldGrp('bakeRange_fld', cw = (1, 70), nf = 2, l = 'Start/End: ', v1 = sTime, v2 = eTime)
        mc.button(l = 'Bake', c = doBakeConstrainedCtrl)
        mc.separator(style = 'in')
        
        mc.text(al = 'left', l = '5. Bake camera shake.')
        mc.textScrollList('cam_ls', ams = True, h = 120)
        mc.radioButtonGrp('bakeTo_rdo', la2 = ['fly_ctrl (rotate)', 'localAim (translate)'], nrb = 2, sl = 1)
        mc.button(l = 'Bake Selected Shake', c = doBake)
        mc.separator(style = 'in')
        
        mc.text(al = 'left', l = '6. Clear animCurves.')
        mc.text(al = 'left', l = "What's it works: \n - Set key to empty keyed assets \n - Set key to all animCurve at start/end every shot \n - Trim out all animCurve in sequence range  \n - Trim out and set pre/post roll to cam each shot")
        mc.button(l = 'Clear animCurves', c = doSetAllKey)
        mc.separator(style = 'none')
        
        listShake()
        
        mc.showWindow('preparePublishWin')
        
    else:
        if mc.window('preparePublishWin', exists = True):
            mc.deleteUI('preparePublishWin')
        mc.confirmDialog(t = 'Report', m = 'Please save as Publish task.', b = 'OK')