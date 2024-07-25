import maya.cmds as mc

def bakeCamShake(camNamespace, startTime, endTime, targetOption):
    camShake = '%s:camera_shake' %camNamespace
    offset = '%s:offset_ctrl' %camNamespace
    shakeCtrl = '%s:shake_ctrl' %camNamespace
    allLocal = '%s:fly_ctrl' %camNamespace
    camera_localAim = '%s:camera_localAim_ctrl' %camNamespace
    camera_up = '%s:camera_up_ctrl' %camNamespace
    
    # create objects
    tempLoc = mc.spaceLocator(n = 'temp_loc')
    tempGroup = mc.group('temp_loc', n = 'temp_group')
    
    # constrain
    mc.parent('temp_group', offset, r = True)
    mc.parentConstraint(camShake, tempLoc, mo = False)
    
    # bake
    mc.bakeResults(tempLoc, t = (startTime, endTime), sb = 1)
    
    # copy values
    if targetOption == 1:
        mc.copyKey(tempLoc, t = (startTime, endTime), at = 'translateX', o = "curve")
        mc.pasteKey(allLocal, at = 'translateX')
        mc.copyKey(tempLoc, t = (startTime, endTime), at = 'translateY', o = "curve")
        mc.pasteKey(allLocal, at = 'translateY')
        mc.copyKey(tempLoc, t = (startTime, endTime), at = 'translateZ', o = "curve")
        mc.pasteKey(allLocal, at = 'translateZ')
        mc.copyKey(tempLoc, t = (startTime, endTime), at = 'rotateX', o = "curve")
        mc.pasteKey(allLocal, at = 'rotateX')
        mc.copyKey(tempLoc, t = (startTime, endTime), at = 'rotateY', o = "curve")
        mc.pasteKey(allLocal, at = 'rotateY')
        mc.copyKey(tempLoc, t = (startTime, endTime), at = 'rotateZ', o = "curve")
        mc.pasteKey(allLocal, at = 'rotateZ')
    elif targetOption == 2:
        mc.copyKey(tempLoc, t = (startTime, endTime), at = 'rotateX', o = "curve")
        mc.pasteKey(camera_localAim, at = 'translateY')
        mc.copyKey(tempLoc, t = (startTime, endTime), at = 'rotateY', o = "curve")
        mc.pasteKey(camera_localAim, at = 'translateX') ##
        mc.copyKey(tempLoc, t = (startTime, endTime), at = 'rotateZ', o = "curve")
        mc.pasteKey(camera_up, at = 'translateZ') ##
        mc.setAttr('%s.translateZ' %camera_localAim, -37.2)
        mc.setAttr('%s.translateY' %camera_up, 46.3)
        
        ctrlInvLs = ['%s.translateZ' %camera_up, '%s.translateX' %camera_localAim]
        for i in ctrlInvLs:
            keyLs = mc.keyframe(i, q = True, tc = True)
            for j in keyLs:
                keyValue = mc.keyframe(i, time = (j,j), q = True, vc = True)[0]
                keyValue = keyValue * -1
                mc.keyframe(i, time = (j,j), absolute = True, vc = keyValue)
            
    # clear
    mc.delete(tempGroup)    
    mc.setAttr('%s.shake3D' %shakeCtrl, 0)