import pymel.core as pm
import maya.cmds as cmds
import re

# select constrained ctrl for baking
def selConstrainedCtrl(*args):
    cnstAll = pm.ls(type = 'constraint')
    cnstRN = pm.ls(type = 'constraint', rn = True)
    cnstLocal = list(set(cnstAll).difference(set(cnstRN)))
    pm.select(cl = True)
    pm.select(pm.listRelatives(cnstLocal, ap = True))

# clean FXguide
def cleanFxGuide(*args):
    fxItems = pm.listRelatives('fxmarker_GRP', ad = True)
    for i in fxItems:
        try:
            lyr = pm.listConnections(i, type = "displayLayer")
            for j in lyr:
                pm.disconnectAttr('%s.drawInfo' %j, '%s.drawOverride' %i)
                print 'Remove "%s" from "%s" layer.' %(i, j)
        except:
            pass

    group_name = 'fxmarker_GRP'
    # Get all objects in the group and its descendants
    objects = cmds.ls(group_name, dag=True, type='transform')
    
    # Iterate over each object
    for obj in objects:
        # Get all connected nodes
        connected_nodes = cmds.listConnections(obj, connections=True, plugs=True)
        
        try:
            # Remove namespace from the object itself
            if ':' in obj:
                obj_name = obj.split(':')[-1]
                cmds.rename(obj, obj_name)
            
            # Remove namespace from connected nodes
            if connected_nodes:
                for node in connected_nodes:
                    if ':' in node:
                        node_name = node.split(':')[-1]
                        cmds.rename(node, node_name)
        except:
            pass
    pm.confirmDialog(t = 'Report', m = 'fxguide is cleared', b = 'OK')

# check sequencer and camera
def doCheckSeqCamName(*args):
    from LayoutTool.modules import getSortedShotLs_mod
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
        shotName = pm.shot(shot, q = True, sn = True)
        pm.rename(shot, 'shotTemp%d' %n)
        pm.shot(shot, e = True, sn = shotName)
        n += 1
        
    n = 1
    for shot in shots:
        shotName = pm.shot(shot, q = True, sn = True)
        pm.rename(shot, 'shot%d' %n)
        pm.shot(shot, e = True, sn = shotName)
        n += 1
        
    
    #######################################    
    
    shots = getSortedShotLs_mod.getShotLs()
    errorCheck = 0
    noMatchLs = 'These shots are not match with the camera name:\n\n'
    wrongScaleLs = 'These shots frame number are not match:\n\n'
    for shot in shots:
        camName = pm.shot(shot, q = True, cc = True).split(':')[0]
        shotName = pm.shot(shot, q = True, sn = True)
        if camName != shotName:
            noMatchLs += "- %s\n" %shotName
            errorCheck += 1
        st = pm.shot(shot, q = True, st = True)
        sst = pm.shot(shot, q = True, sst = True)
        et = pm.shot(shot, q = True, et = True)
        set = pm.shot(shot, q = True, set = True)
        if st != sst or et != set:
            wrongScaleLs += "- %s\n" %shotName
            errorCheck += 1
    if errorCheck != 0:    
        pm.confirmDialog(t = 'Report', m = '%s\n\n%s' %(noMatchLs, wrongScaleLs) , b = 'OK')
    else:
        pm.confirmDialog(t = 'Report', m = 'Sequencer is clear', b = 'OK')

# bake constrained ctrl
def doBakeConstrainedCtrl(*args):
    startTime = pm.intFieldGrp('bakeRange_fld', q = True, v1 = True)
    endTime = pm.intFieldGrp('bakeRange_fld', q = True, v2 = True)
    cnstAll = pm.ls(type = 'constraint')
    cnstRN = pm.ls(type = 'constraint', rn = True)
    sel = pm.ls(sl = True)
    pm.bakeResults(sel, t = (startTime, endTime), sb = 1)
    pm.delete(pm.ls(list(set(cnstAll).difference(set(cnstRN)))))

# list shake ctrl
def listShake(*args):
    shakeCtrlLs = pm.ls('*:shake_ctrl')
    for i in shakeCtrlLs:  # find shaked ctrl
        if i.getAttr('shake3D' %i) == 1:
            pm.textScrollList('cam_ls', e = True, append = i.split(':')[0])
            
# bake shake
def doBake(*args):
    from LayoutTool.modules import bakeCamShake_mod
    reload(bakeCamShake_mod)
    
    targetOption = pm.radioButtonGrp('bakeTo_rdo', q = True, sl = True)
    camLs = pm.textScrollList('cam_ls', q = True, si = True)
    
    # prepare variables
    for shotName in camLs:
        for i in pm.ls(typ = 'shot'): # find shot of selected camera
            if pm.shot(i, q = True, sn = True) == shotName:
                startTime = pm.getAttr('%s.startFrame' %i)
                endTime = pm.getAttr('%s.endFrame' %i)
                #print i, startTime, endTime
                
        bakeCamShake_mod.bakeCamShake(shotName, startTime, endTime, targetOption)
           
        pm.textScrollList('cam_ls', e = True, ra = True)
        listShake()
    
def doSetAllKey(*args):
    pm.select(cl = True)
    
    # key on empty keyed assets/cams
    keyTime = 1001
    charPLs = pm.ls('char*:placement_ctrl')
    propPLs = pm.ls('prop*:placement_ctrl')
    camPLs = pm.listRelatives('cam')
    assetPLs = []
    for i in charPLs:
        assetPLs.append(i.split(':')[0])
    for i in propPLs:
        assetPLs.append(i.split(':')[0])
    for i in camPLs:
        assetPLs.append(i.split(':')[0])
        
    for i in assetPLs:
        ctrls = pm.ls('%s:*_ctrl' %i)
        isKeyFrame = False
        for ctrl in ctrls:
            ctrl = pm.PyNode(ctrl)
            if pm.keyframe(ctrl, q = True, index = True):
                isKeyFrame = True
                break
        
        if not isKeyFrame:
            isKeyed = True
            keyCtrl = '%s:offset_ctrl' %i
            pm.setKeyframe(keyCtrl, shape = False, time = [keyTime, keyTime+1])
            
        else:
            isKeyed = False
    
    # variables
    shots = pm.ls(typ = 'shot')
    curves = pm.ls(type = 'animCurve')
    time = []
    for i in shots:
        time.append(pm.shot(i, q = True, st = True))
        time.append(pm.shot(i, q = True, et = True))
    time.sort()
    
    # -----------------------------------------------------------
    
    # trim curve function
    def trimCurves(objCurve, sTime, eTime):
        for selCurve in objCurve:
            keyframes = pm.keyframe(selCurve, q = True, tc = True)
            for time in keyframes:
                if time < sTime:
                    pm.cutKey(selCurve, time = (time,time))
                if time > eTime:
                    pm.cutKey(selCurve, time = (time,time))
                    
    # add pre/post roll function
    def addPrePostRoll(objCurve, sTime, eTime):
        for selCurve in objCurve:
            if pm.keyframe(selCurve, q = True, index = True):
                # get current infinity state
                infState = pm.setInfinity(selCurve, q = True, pri = True, poi = True)
                # set start/end outer tangent to follow inner tangent
                pm.keyTangent(selCurve, t = (sTime,sTime), itt = 'clamped')
                pm.keyTangent(selCurve, t = (eTime,eTime), ott = 'clamped')
                # set infinity
                pm.setInfinity(selCurve, pri = 'linear', poi = 'linear')
                # key pre/post roll
                pm.setKeyframe(selCurve, t = (sTime-5,sTime-5), s = False, i = True)
                pm.setKeyframe(selCurve, t = (eTime+5,eTime+5), s = False, i = True)
                # set pre/post roll tangent to linear/spline
                pm.keyTangent(selCurve, t = (sTime-5,sTime-5), itt = 'spline', ott = 'spline')
                pm.keyTangent(selCurve, t = (eTime+5,eTime+5), itt = 'spline', ott = 'spline')
                # set start/end tangent to linear/spline
                pm.keyTangent(selCurve, t = (sTime,sTime), itt = 'linear')
                pm.keyTangent(selCurve, t = (eTime,eTime), ott = 'linear')
                # set infinity state to previous
                pm.setInfinity(selCurve, pri = infState[0], poi = infState[1])
    
    # -----------------------------------------------------------
    
    # key block shot every exists curve
    for i in time:
        pm.setKeyframe(curves, t = (i), s = False, i = True)
        
    # trim overall keyframe
    sTime = time[0]
    eTime = time[-1]
    trimCurves(curves, sTime, eTime)
                
    # trim cam keyframe
    for i in shots:
        sTime = pm.shot(i, q = True, st = True)
        eTime = pm.shot(i, q = True, et = True)
        cam = pm.shot(i, q = True, cc = True)
        shotName = cam.split(':')[0]
        camCtrls = pm.ls('%s:*_ctrl' %shotName)
        trimCurves(camCtrls, sTime, eTime)
        addPrePostRoll(camCtrls, sTime, eTime)
        
def preparePublishUI():
    filename = cmds.file(q = True, sn = True)
    match = re.search('publish', filename) #########
    if match:
        time = []
        shots = pm.ls(typ = 'shot')
        for i in shots:
            time.append(pm.shot(i, q = True, st = True))
            time.append(pm.shot(i, q = True, et = True))
        time.sort()
        sTime = time.pop(0)
        eTime = time.pop(-1)
        
        if pm.window('preparePublishWin', exists = True):
            pm.deleteUI('preparePublishWin')
        pm.window('preparePublishWin', t = 'Prepare Scene for Publish', mxb = False, w = 100)
        
        pm.columnLayout(adj = True, rs = 8, cat = ['both', 10])
        pm.separator(style = 'none')
        
        pm.text(al = 'left', l = '1. Please clear your displayLayer visibility and animLayers.', ww = True)
        pm.separator(style = 'in')
        
        pm.text(al = 'left', l = '2. Remove FXguide from layers and namespaces.', ww = True)
        pm.text(al = 'left', l = 'Note: Please check your current namespace is "root". Go to Windows > General Editors > Namespace Editor.', ww = True)
        pm.button(l = 'Clean FXguide', c = cleanFxGuide)
        pm.separator(style = 'in')
        
        pm.text(al = 'left', l = '3. Check sequencer shots and camera name.')
        pm.button(l = 'Check Shots and Cameras', c = doCheckSeqCamName)
        pm.separator(style = 'in')
        
        pm.text(al = 'left', l = '4. Bake constrained ctrl.')
        pm.button(l = 'Check Constrained Ctrl', c = selConstrainedCtrl)
        pm.intFieldGrp('bakeRange_fld', cw = (1, 70), nf = 2, l = 'Start/End: ', v1 = sTime, v2 = eTime)
        pm.button(l = 'Bake', c = doBakeConstrainedCtrl)
        pm.separator(style = 'in')
        
        pm.text(al = 'left', l = '5. Bake camera shake.')
        pm.textScrollList('cam_ls', ams = True, h = 120)
        pm.radioButtonGrp('bakeTo_rdo', la2 = ['fly_ctrl (rotate)', 'localAim (translate)'], nrb = 2, sl = 1)
        pm.button(l = 'Bake Selected Shake', c = doBake)
        pm.separator(style = 'in')
        
        pm.text(al = 'left', l = '6. Clear animCurves.')
        pm.text(al = 'left', l = "What's it works: \n - Set key to empty keyed assets \n - Set key to all animCurve at start/end every shot \n - Trim out all animCurve in sequence range  \n - Trim out and set pre/post roll to cam each shot")
        pm.button(l = 'Clear animCurves', c = doSetAllKey)
        pm.separator(style = 'none')
        
        listShake()
        
        pm.showWindow('preparePublishWin')
        
    else:
        if pm.window('preparePublishWin', exists = True):
            pm.deleteUI('preparePublishWin')
        pm.confirmDialog(t = 'Report', m = 'Please save as Publish task.', b = 'OK')

def run():
    preparePublishUI()
