import maya.cmds as cmds

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
        camLsRaw = cmds.ls(self.camIndicator) # find camera by '*:camera' ending
        for i in camLsRaw:
            camLs.append(i.split(':')[0])
        camLs.sort(key = lambda k : k.lower())
        
        assetLs = []
        for i in self.assetIndicator:
            for j in [k.split(':')[0] for k in cmds.ls('{}{}'.format(i, self.ctrlName))]:
                assetLs.append(j)

        return camLs, assetLs

    ####################################

    def selectControllers(self, mode, camName, camCtrl, assetName, assetCtrl):
        if mode == False:
            cmds.select(cl = True)
        if camName and camCtrl:
            for cam in camName:
                for ctrl in camCtrl:
                    camCtrlSel = '%s:%s' %(cam, ctrl)
                    cmds.select(camCtrlSel, add = True)
        
        if assetName and assetCtrl:        
            for asset in assetName:
                for ctrl in assetCtrl:
                    if ctrl == 'placement_ctrl':
                        cmds.select('%s:placement_ctrl' %asset, add = True)
                    if ctrl == 'offset_ctrl':
                        cmds.select('%s:offset_ctrl' %asset, add = True)
                    if ctrl == 'fly_ctrl':
                        cmds.select('%s:fly_ctrl' %asset, add = True)
                    if ctrl == 'body_ctrl':
                        allCtrlLs = cmds.ls('%s:*_ctrl' %asset)
                        mainCtrl = cmds.ls(['%s:placement_ctrl' %asset, '%s:offset_ctrl' %asset, '%s:fly_ctrl' %asset])
                        bodyCtrlLs = list(set(allCtrlLs).difference(set(mainCtrl)))
                        cmds.select(bodyCtrlLs, add = True)
                    if ctrl == 'facial_Ctrl':
                        try:
                            cmds.select('%s:*_Ctrl' %asset, add = True)
                        except:
                            pass

    def currentShot(self):
        currentShot = cmds.ls(cmds.sequenceManager(q = True, currentShot = True))[0]
        currentShotName = cmds.shot(currentShot, q = True, cc = True).split(':')[0] # get camera namespace as shot name
        shotStart = cmds.getAttr('%s.startFrame' %currentShot)
        shotEnd = cmds.getAttr('%s.endFrame' %currentShot)
        return currentShotName, shotStart, shotEnd
        
    def snapToRefCam(self, camName, camCtrl, refCam, focal):
        from imp import reload
        from lay_modules import snap_mod
        reload(snap_mod)
        snap_mod.snap(['%s:%s' %(camName, camCtrl), refCam])
        camera_ctrl = '%s:camera_ctrl' %camName
        cmds.setAttr('%s.focalLength' %camera_ctrl, 7)
        cmds.setAttr('%s.custom_FocalLength' %camera_ctrl, focal)

    ####################################
    def copyShakeProc(self, *args):
        selCopy = cmds.ls(sl = True)[-1].split(':')[0] + ':shake_ctrl'
        maxTX = cmds.getAttr('%s.maxDistanceTX' %selCopy)
        maxTY = cmds.getAttr('%s.maxDistanceTY' %selCopy)
        maxTZ = cmds.getAttr('%s.maxDistanceTZ' %selCopy)
        maxRX = cmds.getAttr('%s.maxDistanceRX' %selCopy)
        maxRY = cmds.getAttr('%s.maxDistanceRY' %selCopy)
        maxRZ = cmds.getAttr('%s.maxDistanceRZ' %selCopy)
        speedT = cmds.getAttr('%s.speedT' %selCopy)
        speedR = cmds.getAttr('%s.speedR' %selCopy)
        timeOffsetT = cmds.getAttr('%s.timeOffsetT' %selCopy)
        timeOffsetR = cmds.getAttr('%s.timeOffsetR' %selCopy)
        weight = cmds.getAttr('%s.weight' %selCopy)
        
        self.shakeValue = [maxTX, maxTY, maxTZ,
                            maxRX, maxRY, maxRZ,
                            speedT , speedR, 
                            timeOffsetT, timeOffsetR,
                            weight]

    def pasteShakeProc(self):
        selPaste = cmds.ls(sl = True)
        for i in selPaste:
            shakeCtrl = i.split(':')[0] + ':shake_ctrl'
            cmds.setAttr('%s.maxDistanceTX' %shakeCtrl, self.shakeValue[0])
            cmds.setAttr('%s.maxDistanceTY' %shakeCtrl, self.shakeValue[1])
            cmds.setAttr('%s.maxDistanceTZ' %shakeCtrl, self.shakeValue[2])
            cmds.setAttr('%s.maxDistanceRX' %shakeCtrl, self.shakeValue[3])
            cmds.setAttr('%s.maxDistanceRY' %shakeCtrl, self.shakeValue[4])
            cmds.setAttr('%s.maxDistanceRZ' %shakeCtrl, self.shakeValue[5])
            cmds.setAttr('%s.speedT' %shakeCtrl, self.shakeValue[6])
            cmds.setAttr('%s.speedR' %shakeCtrl, self.shakeValue[7])
            cmds.setAttr('%s.timeOffsetT' %shakeCtrl, self.shakeValue[8])
            cmds.setAttr('%s.timeOffsetR' %shakeCtrl, self.shakeValue[9])
            cmds.setAttr('%s.weight' %shakeCtrl, self.shakeValue[10])
            cmds.setAttr('%s.shake3D' %shakeCtrl, 1)