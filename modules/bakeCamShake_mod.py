import pymel.core as pm

def bakeCamShake(camNamespace, startTime, endTime, targetOption):
    camShake = '%s:camera_shake' %camNamespace
    offset = '%s:offset_ctrl' %camNamespace
    shakeCtrl = '%s:shake_ctrl' %camNamespace
    allLocal = '%s:fly_ctrl' %camNamespace
    camera_localAim = '%s:camera_localAim_ctrl' %camNamespace
    camera_up = '%s:camera_up_ctrl' %camNamespace
    
    # create objects
    tempLoc = pm.spaceLocator(n = 'temp_loc')
    tempGroup = pm.group('temp_loc', n = 'temp_group')
    
    # constrain
    pm.parent('temp_group', offset, r = True)
    pm.parentConstraint(camShake, tempLoc, mo = False)
    
    # bake
    pm.bakeResults(tempLoc, t = (startTime, endTime), sb = 1)
    
    # copy values
    if targetOption == 1:
        pm.copyKey(tempLoc, t = (startTime, endTime), at = 'translateX', o = "curve")
        pm.pasteKey(allLocal, at = 'translateX')
        pm.copyKey(tempLoc, t = (startTime, endTime), at = 'translateY', o = "curve")
        pm.pasteKey(allLocal, at = 'translateY')
        pm.copyKey(tempLoc, t = (startTime, endTime), at = 'translateZ', o = "curve")
        pm.pasteKey(allLocal, at = 'translateZ')
        pm.copyKey(tempLoc, t = (startTime, endTime), at = 'rotateX', o = "curve")
        pm.pasteKey(allLocal, at = 'rotateX')
        pm.copyKey(tempLoc, t = (startTime, endTime), at = 'rotateY', o = "curve")
        pm.pasteKey(allLocal, at = 'rotateY')
        pm.copyKey(tempLoc, t = (startTime, endTime), at = 'rotateZ', o = "curve")
        pm.pasteKey(allLocal, at = 'rotateZ')
    elif targetOption == 2:
        pm.copyKey(tempLoc, t = (startTime, endTime), at = 'rotateX', o = "curve")
        pm.pasteKey(camera_localAim, at = 'translateY')
        pm.copyKey(tempLoc, t = (startTime, endTime), at = 'rotateY', o = "curve")
        pm.pasteKey(camera_localAim, at = 'translateX') ##
        pm.copyKey(tempLoc, t = (startTime, endTime), at = 'rotateZ', o = "curve")
        pm.pasteKey(camera_up, at = 'translateZ') ##
        pm.setAttr('%s.translateZ' %camera_localAim, -37.2)
        pm.setAttr('%s.translateY' %camera_up, 46.3)
        
        ctrlInvLs = ['%s.translateZ' %camera_up, '%s.translateX' %camera_localAim]
        for i in ctrlInvLs:
            keyLs = pm.keyframe(i, q = True, tc = True)
            for j in keyLs:
                keyValue = pm.keyframe(i, time = (j,j), q = True, vc = True)[0]
                keyValue = keyValue * -1
                pm.keyframe(i, time = (j,j), absolute = True, vc = keyValue)
            
    # clear
    pm.delete(tempGroup)    
    pm.setAttr('%s.shake3D' %shakeCtrl, 0)