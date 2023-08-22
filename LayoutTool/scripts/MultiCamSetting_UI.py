import pymel.core as pm

def batchCamSettingUI():
    if pm.window('batchCamSettingWin', exists = True):
        pm.deleteUI('batchCamSettingWin')
    pm.window('batchCamSettingWin', t = 'Cameras Batch Settings', mxb = False)
    
    mainLay = pm.columnLayout(adj = True, rs = 5, cat = ['both', 5])
    with mainLay:
        pm.separator(style = 'none')
        pm.text(l = 'Camera List: ', al = 'left')
        pm.textScrollList('camList', ams = True)
        pm.button(l = 'Select All', c = selAllCams)
        pm.separator(style = 'in')
    
        settingLay = pm.rowColumnLayout(nc = 2, cw = [2,200], cal = [1,'right'], cs = [1,5], rs = [1,5])
        with settingLay:
            pm.text(l = 'Near Clip Plane: ')
            pm.floatField('nearClipV', v = 1)
            pm.text(l = 'Far Clip Plane: ')
            pm.floatField('farClipV', v = 1000000)
            pm.text(l = ' ')
            pm.checkBox('displayGateV', l = 'Display Gate Mask', v = 1)
            pm.text(l = 'Gate Display: ')
            pm.radioButtonGrp('gateType', la2 = ['Resolution', 'Film'], nrb = 2, sl = 1)
            pm.text(l = 'Opacity: ')
            pm.floatSliderGrp('opacityV', f = True, min = 0, max = 1, fmn = 0, fmx = 1, value = 1, pre = 3)
            pm.text(l = 'Color: ')
            pm.colorSliderGrp('colorV', rgb = (0, 0, 0))
            pm.text(l = ' ')
            pm.checkBox('safeActV', l = 'Safe Action', v = 1)
            pm.text(l = ' ')
            pm.checkBox('safeTitleV', l = 'Safe Title', v = 0)
            pm.text(l = 'Overscan: ')
            pm.floatSliderGrp('overscanV', f = True, min = 1, max = 2, fmn = 0, fmx = 10, value = 1.3, pre = 3)
        pm.button(l = 'Apply', c = applyCamSettings)
        pm.separator(style = 'none')
    
    pm.showWindow('batchCamSettingWin')
    initial()

def initial(*args):
    pm.textScrollList('camList', e = True, ra = True)
    camLs = pm.ls(type = 'camera')
    camLs.sort(key = lambda k : k.lower())
    pm.textScrollList('camList', e = True, append = camLs)
    
def selAllCams(*args):
    pm.textScrollList('camList', e = True, si = pm.textScrollList('camList', q = True, ai = True))

def applyCamSettings(*args):
    selCams   = pm.textScrollList('camList', q = True, si = True)    #list
    nearClip  = pm.floatField('nearClipV', q = True, v = True)       #float
    farClip   = pm.floatField('farClipV', q = True, v = True)        #float
    gateDisp  = pm.checkBox('displayGateV', q = True, v = True)      #bool
    gateMode  = pm.radioButtonGrp('gateType', q = True, sl = True)   #int
    gateOpac  = pm.floatSliderGrp('opacityV', q = True, v = 1)       #float
    gateColor = pm.colorSliderGrp('colorV', q = True, rgb = True)    #vecter (3 of list)
    safeAct   = pm.checkBox('safeActV', q = True, v = True)          #bool
    safeTit   = pm.checkBox('safeTitleV', q = True, v = True)        #bool
    overscan  = pm.floatSliderGrp('overscanV', q = True, v = True)   #float
    
    for i in selCams:
        errorStr = []
        try:
            pm.setAttr('%s:camera_ctrl.nearClipPlane' %i.split(':')[0], nearClip)
        except:
            try:
                pm.setAttr('%s.nearClipPlane' %i, nearClip)
            except:
                errorStr.append('Near Clip')
        try:  
            pm.setAttr('%s:camera_ctrl.farClipPlane' %i.split(':')[0], farClip)
        except:
            try:
                pm.setAttr('%s.farClipPlane' %i, farClip)
            except:
                errorStr.append('Far Clip')
        try:
            pm.setAttr('%s.displayGateMask' %i, gateDisp)
        except:
            errorStr.append('Gate Display')  
        try:
            if gateMode == 1:
                pm.setAttr('%s.displayResolution' %i, 1)
                pm.setAttr('%s.displayFilmGate' %i, 0)
            elif gateMode == 2:
                pm.setAttr('%s.displayResolution' %i, 0)
                pm.setAttr('%s.displayFilmGate' %i, 1)
        except:
            errorStr.append('Gate Type')  
        try:
            pm.setAttr('%s.displayGateMaskOpacity' %i, gateOpac)
        except:
            errorStr.append('Gate Opacity')  
        try:
            pm.setAttr('%s.displayGateMaskColor' %i, gateColor)
        except:
            errorStr.append('Gate Color')  
        try:
            pm.setAttr('%s.displaySafeAction' %i, safeAct)
        except:
            errorStr.append('Safe Action') 
        try:
            pm.setAttr('%s.displaySafeTitle' %i, safeTit)
        except:
            errorStr.append('Safe Title')  
        try:
            pm.setAttr('%s.overscan' %i, overscan)
        except:
            errorStr.append('Overscan')  
        if errorStr:
            print ' # ' + i + ' error: ' + ', '.join(errorStr)

def run():
    batchCamSettingUI()
run()