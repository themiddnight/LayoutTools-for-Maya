import pymel.core as pm

class LayoutToolCtrl:
    def __init__(self):

        self.camCtrlLs = [
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
        self.camCtrlFn = [
                        (1,'boldLabelFont'), 
                        (2,'boldLabelFont'), 
                        (3,'boldLabelFont')
                    ]
        self.assetCtrlLs = [
                        'placement_ctrl', 
                        'offset_ctrl', 
                        'fly_ctrl', 
                        'body_ctrl', 
                        'facial_Ctrl'
                    ]
        self.assetCtrlFn = [
                        (1,'boldLabelFont'), 
                        (2,'boldLabelFont'), 
                        (3,'boldLabelFont')
                    ]

        self.assetIndicator = ['char', 'prop', 'vhcl', 'CMB']
        self.camIndicator   = '*:camera'
        self.ctrlName       = '*:placement_ctrl'
        self.shakeValue     = []

    def getCtrlList(self):
        return self.camCtrlLs, self.camCtrlFn, self.assetCtrlLs, self.assetCtrlFn

    def getNameList(self):
        camLs    = []
        camLsRaw = pm.ls(self.camIndicator) # find camera by '*:camera' ending
        for i in camLsRaw:
            camLs.append(i.split(':')[0])
        camLs.sort(key = lambda k : k.lower())
        
        assetLs = []
        for i in self.assetIndicator:
            for j in [k.split(':')[0] for k in pm.ls('{}{}'.format(i, self.ctrlName))]:
                assetLs.append(j)

        return camLs, assetLs

    ####################################

    def selectControllers(self, mode, camName, camCtrl, assetName, assetCtrl):
        if mode == False:
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

    def currentShot(self):
        currentShot = pm.ls(pm.sequenceManager(q = True, currentShot = True))[0]
        currentShotName = pm.shot(currentShot, q = True, cc = True).split(':')[0] # get camera namespace as shot name
        shotStart = pm.getAttr('%s.startFrame' %currentShot)
        shotEnd = pm.getAttr('%s.endFrame' %currentShot)
        return currentShotName, shotStart, shotEnd
        
    def snapToRefCam(self, camName, camCtrl, refCam, focal):
        from imp import reload
        from modules import snap_mod
        reload(snap_mod)
        snap_mod.snap(['%s:%s' %(camName, camCtrl), refCam])
        camera_ctrl = '%s:camera_ctrl' %camName
        pm.setAttr('%s.focalLength' %camera_ctrl, 7)
        pm.setAttr('%s.custom_FocalLength' %camera_ctrl, focal)

    ####################################
    def copyShakeProc(self, *args):
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
        
        self.shakeValue = [maxTX, maxTY, maxTZ,
                            maxRX, maxRY, maxRZ,
                            speedT , speedR, 
                            timeOffsetT, timeOffsetR,
                            weight]

    def pasteShakeProc(self):
        selPaste = pm.ls(sl = True)
        for i in selPaste:
            shakeCtrl = i.split(':')[0] + ':shake_ctrl'
            pm.setAttr('%s.maxDistanceTX' %shakeCtrl, self.shakeValue[0])
            pm.setAttr('%s.maxDistanceTY' %shakeCtrl, self.shakeValue[1])
            pm.setAttr('%s.maxDistanceTZ' %shakeCtrl, self.shakeValue[2])
            pm.setAttr('%s.maxDistanceRX' %shakeCtrl, self.shakeValue[3])
            pm.setAttr('%s.maxDistanceRY' %shakeCtrl, self.shakeValue[4])
            pm.setAttr('%s.maxDistanceRZ' %shakeCtrl, self.shakeValue[5])
            pm.setAttr('%s.speedT' %shakeCtrl, self.shakeValue[6])
            pm.setAttr('%s.speedR' %shakeCtrl, self.shakeValue[7])
            pm.setAttr('%s.timeOffsetT' %shakeCtrl, self.shakeValue[8])
            pm.setAttr('%s.timeOffsetR' %shakeCtrl, self.shakeValue[9])
            pm.setAttr('%s.weight' %shakeCtrl, self.shakeValue[10])
            pm.setAttr('%s.shake3D' %shakeCtrl, 1)