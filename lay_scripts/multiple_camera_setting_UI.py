'''Set multiple cameras settings at once.'''

import maya.cmds as mc

def initial(*args):
    mc.textScrollList('camList', e = True, ra = True)
    camLs = mc.ls(type = 'camera')
    camLs.sort(key = lambda k : k.lower())
    mc.textScrollList('camList', e = True, append = camLs)
    
def selAllCams(*args):
    mc.textScrollList('camList', e = True, si = mc.textScrollList('camList', q = True, ai = True))

def applyCamSettings(*args):
    selCams   = mc.textScrollList('camList', q = True, si = True)    #list
    nearClip  = mc.floatField('nearClipV', q = True, v = True)       #float
    farClip   = mc.floatField('farClipV', q = True, v = True)        #float
    gateDisp  = mc.checkBox('displayGateV', q = True, v = True)      #bool
    gateMode  = mc.radioButtonGrp('gateType', q = True, sl = True)   #int
    gateOpac  = mc.floatSliderGrp('opacityV', q = True, v = 1)       #float
    gateColor = mc.colorSliderGrp('colorV', q = True, rgb = True)    #vecter (3 of list)
    safeAct   = mc.checkBox('safeActV', q = True, v = True)          #bool
    safeTit   = mc.checkBox('safeTitleV', q = True, v = True)        #bool
    overscan  = mc.floatSliderGrp('overscanV', q = True, v = True)   #float
    
    for i in selCams:
        errorStr = []
        try:
            mc.setAttr('%s:camera_ctrl.nearClipPlane' %i.split(':')[0], nearClip)
        except:
            try:
                mc.setAttr('%s.nearClipPlane' %i, nearClip)
            except:
                errorStr.append('Near Clip')
        try:  
            mc.setAttr('%s:camera_ctrl.farClipPlane' %i.split(':')[0], farClip)
        except:
            try:
                mc.setAttr('%s.farClipPlane' %i, farClip)
            except:
                errorStr.append('Far Clip')
        try:
            mc.setAttr('%s.displayGateMask' %i, gateDisp)
        except:
            errorStr.append('Gate Display')  
        try:
            if gateMode == 1:
                mc.setAttr('%s.displayResolution' %i, 1)
                mc.setAttr('%s.displayFilmGate' %i, 0)
            elif gateMode == 2:
                mc.setAttr('%s.displayResolution' %i, 0)
                mc.setAttr('%s.displayFilmGate' %i, 1)
        except:
            errorStr.append('Gate Type')  
        try:
            mc.setAttr('%s.displayGateMaskOpacity' %i, gateOpac)
        except:
            errorStr.append('Gate Opacity')  
        try:
            mc.setAttr('%s.displayGateMaskColor' %i, gateColor)
        except:
            errorStr.append('Gate Color')  
        try:
            mc.setAttr('%s.displaySafeAction' %i, safeAct)
        except:
            errorStr.append('Safe Action') 
        try:
            mc.setAttr('%s.displaySafeTitle' %i, safeTit)
        except:
            errorStr.append('Safe Title')  
        try:
            mc.setAttr('%s.overscan' %i, overscan)
        except:
            errorStr.append('Overscan')  
        if errorStr:
            print(' # ' + i + ' error: ' + ', '.join(errorStr))

def run():
    if mc.window('batchCamSettingWin', exists = True):
        mc.deleteUI('batchCamSettingWin')
    mc.window('batchCamSettingWin', t = 'Cameras Batch Settings', mxb = False)
    
    mc.columnLayout(adj = True, rs = 5, cat = ['both', 5])
    mc.separator(style = 'none')
    mc.text(l = 'Camera List: ', al = 'left')
    mc.textScrollList('camList', ams = True)
    mc.button(l = 'Select All', c = selAllCams)
    mc.separator(style = 'in')

    mc.rowColumnLayout(nc = 2, cw = [2,200], cal = [1,'right'], cs = [1,5], rs = [1,5])
    mc.text(l = 'Near Clip Plane: ')
    mc.floatField('nearClipV', v = 1)
    mc.text(l = 'Far Clip Plane: ')
    mc.floatField('farClipV', v = 1000000)
    mc.text(l = ' ')
    mc.checkBox('displayGateV', l = 'Display Gate Mask', v = 1)
    mc.text(l = 'Gate Display: ')
    mc.radioButtonGrp('gateType', la2 = ['Resolution', 'Film'], nrb = 2, sl = 1)
    mc.text(l = 'Opacity: ')
    mc.floatSliderGrp('opacityV', f = True, min = 0, max = 1, fmn = 0, fmx = 1, value = 1, pre = 3)
    mc.text(l = 'Color: ')
    mc.colorSliderGrp('colorV', rgb = (0, 0, 0))
    mc.text(l = ' ')
    mc.checkBox('safeActV', l = 'Safe Action', v = 1)
    mc.text(l = ' ')
    mc.checkBox('safeTitleV', l = 'Safe Title', v = 0)
    mc.text(l = 'Overscan: ')
    mc.floatSliderGrp('overscanV', f = True, min = 1, max = 2, fmn = 0, fmx = 10, value = 1.3, pre = 3)
    mc.setParent('..')

    mc.button(l = 'Apply', c = applyCamSettings)
    mc.separator(style = 'none')
    
    mc.showWindow('batchCamSettingWin')
    initial()