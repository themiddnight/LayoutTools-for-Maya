import pymel.core as pm
import sys

assetIndicator = ['char', 'prop', 'vhcl', 'CMB']
camIndicator   = '*:camera'
ctrlName       = '*:placement_ctrl'

camCtrlLs = [
                'placement_ctrl', 
                'offset_ctrl', 
                'fly_ctrl', 
                'camera_roll_ctrl', 
                'dolly_tweak_ctrl', 
                'camera_localAim_ctrl', 
                'camera_up_ctrl', 
                'shake_ctrl', 
                'shake3D_ctrl', 
                'camera_ctrl'
            ]
camCtrlFn = [
                (1,'boldLabelFont'), 
                (2,'boldLabelFont'), 
                (3,'boldLabelFont')
            ]
assetCtrlLs = [
                'placement_ctrl', 
                'offset_ctrl', 
                'fly_ctrl', 
                'body_ctrl', 
                'facial_Ctrl'
              ]
assetCtrlFn = [
                (1,'boldLabelFont'), 
                (2,'boldLabelFont'), 
                (3,'boldLabelFont')
            ]

def getCtrlList():
    return camCtrlLs, camCtrlFn, assetCtrlLs, assetCtrlFn

def getNameList():
    camLs    = []
    camLsRaw = pm.ls(camIndicator) # find camera by '*:camera' ending
    for i in camLsRaw:
        camLs.append(i.split(':')[0])
    camLs.sort(key = lambda k : k.lower())
    
    assetLs = []
    for i in assetIndicator:
        for j in [k.split(':')[0] for k in pm.ls('{}{}'.format(i, ctrlName))]:
            assetLs.append(j)

    return camLs, assetLs

####################################

def selectControllers(camName, camCtrl, assetName, assetCtrl):
    pm.select(cl = True)
    if camName and camCtrl:
        for cam in camName:
            for ctrl in camCtrl:
                camCtrlSel = '%s:%s' %(cam, ctrl)
                pm.select(camCtrlSel, add = True)
    
    if assetName and assetCtrl:        
        for asset in assetName:
            for ctrl in assetCtrl:
                if ctrl == 'placement_ctrl':
                    pm.select('%s:placement_ctrl' %asset, add = True)
                if ctrl == 'offset_ctrl':
                    pm.select('%s:offset_ctrl' %asset, add = True)
                if ctrl == 'fly_ctrl':
                    pm.select('%s:fly_ctrl' %asset, add = True)
                if ctrl == 'body_ctrl':
                    allCtrlLs = pm.ls('%s:*_ctrl' %asset)
                    mainCtrl = pm.ls(['%s:placement_ctrl' %asset, '%s:offset_ctrl' %asset, '%s:fly_ctrl' %asset])
                    bodyCtrlLs = list(set(allCtrlLs).difference(set(mainCtrl)))
                    pm.select(bodyCtrlLs, add = True)
                if ctrl == 'facial_Ctrl':
                    try:
                        pm.select('%s:*_Ctrl' %asset, add = True)
                    except:
                        pass

def currentShot():
    currentShot = pm.ls(pm.sequenceManager(q = True, currentShot = True))[0]
    currentShotName = pm.shot(currentShot, q = True, cc = True).split(':')[0] # get camera namespace as shot name
    shotStart = pm.getAttr('%s.startFrame' %currentShot)
    shotEnd = pm.getAttr('%s.endFrame' %currentShot)
    return currentShotName, shotStart, shotEnd
    
def snapToRefCam(camName, camCtrl, refCam, focal):
    from LayoutTool.modules import snap_mod
    reload(snap_mod)
    snap_mod.snap(['%s:%s' %(camName, camCtrl), refCam])
    camera_ctrl = '%s:camera_ctrl' %camName
    pm.setAttr('%s.focalLength' %camera_ctrl, 7)
    pm.setAttr('%s.custom_FocalLength' %camera_ctrl, focal)

####################################
def copyShakeProc(*args):
    selCopy = pm.ls(sl = True)[-1].split(':')[0] + ':shake_ctrl'
    maxTX = pm.getAttr('%s.maxDistanceTX' %selCopy)
    maxTY = pm.getAttr('%s.maxDistanceTY' %selCopy)
    maxTZ = pm.getAttr('%s.maxDistanceTZ' %selCopy)
    maxRX = pm.getAttr('%s.maxDistanceRX' %selCopy)
    maxRY = pm.getAttr('%s.maxDistanceRY' %selCopy)
    maxRZ = pm.getAttr('%s.maxDistanceRZ' %selCopy)
    speedT = pm.getAttr('%s.speedT' %selCopy)
    speedR = pm.getAttr('%s.speedR' %selCopy)
    timeOffsetT = pm.getAttr('%s.timeOffsetT' %selCopy)
    timeOffsetR = pm.getAttr('%s.timeOffsetR' %selCopy)
    weight = pm.getAttr('%s.weight' %selCopy)
    
    shakeValue = [maxTX, maxTY, maxTZ,
                        maxRX, maxRY, maxRZ,
                        speedT , speedR, 
                        timeOffsetT, timeOffsetR,
                        weight]
    
    return shakeValue

def pasteShakeProc(shakeValue):
    selPaste = pm.ls(sl = True)
    for i in selPaste:
        shakeCtrl = i.split(':')[0] + ':shake_ctrl'
        pm.setAttr('%s.maxDistanceTX' %shakeCtrl, shakeValue[0])
        pm.setAttr('%s.maxDistanceTY' %shakeCtrl, shakeValue[1])
        pm.setAttr('%s.maxDistanceTZ' %shakeCtrl, shakeValue[2])
        pm.setAttr('%s.maxDistanceRX' %shakeCtrl, shakeValue[3])
        pm.setAttr('%s.maxDistanceRY' %shakeCtrl, shakeValue[4])
        pm.setAttr('%s.maxDistanceRZ' %shakeCtrl, shakeValue[5])
        pm.setAttr('%s.speedT' %shakeCtrl, shakeValue[6])
        pm.setAttr('%s.speedR' %shakeCtrl, shakeValue[7])
        pm.setAttr('%s.timeOffsetT' %shakeCtrl, shakeValue[8])
        pm.setAttr('%s.timeOffsetR' %shakeCtrl, shakeValue[9])
        pm.setAttr('%s.weight' %shakeCtrl, shakeValue[10])
        pm.setAttr('%s.shake3D' %shakeCtrl, 1)