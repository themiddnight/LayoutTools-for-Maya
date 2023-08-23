import pymel.core as pm
import os
import LayoutTool_core as LT
import LayoutTool_ctrlList as ctrlList
import scriptUsage
reload(LT)
reload(ctrlList)
reload(scriptUsage)

# -------- basic ui process
def appendCtrlList():
    reload(ctrlList)
    camCtrlLs, camCtrlFn, assetCtrlLs, assetCtrlFn = ctrlList.getCtrlList()
    camNameLs, assetNameLs                         = ctrlList.getNameList()
    pm.textScrollList('camNameTx', e = True, ra = True)
    pm.textScrollList('camCtrlTx', e = True, ra = True)
    pm.textScrollList('assetNameTx', e = True, ra = True) 
    pm.textScrollList('assetCtrlTx', e = True, ra = True)
    pm.textScrollList('camNameTx', e = True, append = camNameLs)
    pm.textScrollList('camCtrlTx', e = True, append = camCtrlLs, lf = camCtrlFn)
    pm.textScrollList('assetNameTx', e = True, append = assetNameLs)
    pm.textScrollList('assetCtrlTx', e = True, append = assetCtrlLs, lf = assetCtrlFn)
    
def appendScriptList():
    reload(LT)
    pm.textScrollList('scriptsTx', e = True, ra = True)
    pm.textScrollList('scriptsTx', e = True, append = LT.getScripts())
    
def getScriptDescription(*args):
    reload(LT)
    scriptName = pm.textScrollList('scriptsTx', q = True, si = True)[0]
    pm.scrollField('scriptDescriptionTx', e = True, cl = True)
    pm.scrollField('scriptDescriptionTx', e = True, tx = LT.getScripDescription(scriptName))
    
def runScriptTx(*args):
    scriptName = pm.textScrollList('scriptsTx', q = True, si = True)[0]
    script = scriptName
    runfrom = 'tool'
    scriptUsage.addData(script, runfrom)
    LT.runScript(scriptName)
    
def runScriptBtn(scriptName):
    script = scriptName
    runfrom = 'button'
    scriptUsage.addData(script, runfrom)
    LT.runScript(scriptName)
    
def addScriptToShelf(*args):
    reload(LT)
    scriptName = pm.textScrollList('scriptsTx', q = True, si = True)[0]
    LT.addScriptToShelf(scriptName)

def openManual(*args):
    # os.startfile('/')
    pass
    
def setCustomLens(*args):
    import setCustomLens_UI
    reload(setCustomLens_UI)
    setCustomLens_UI.UI()
    
def setCustomScript(*args):
    import setCustomScript_UI
    reload(setCustomScript_UI)
    setCustomScript_UI.UI()
    
# -------- ref cam
def setRefCamName(*args):
    reload(LT)
    refCamStr = str(pm.ls(sl = True)[0])
    LT.savePref("refCam", refCamStr)
    pm.text('refCamTx', e = True, l = '%s' %refCamStr)
    
def setsetRefCamFocal(fl):
    refCam = pm.text('refCamTx', q = True, l = True)
    refCamShape = pm.ls(refCam)
    pm.setAttr(refCamShape[-1].focalLength, fl)
    
# -------- ctrl selection
def selectCtrl(*args):
    camName = pm.textScrollList('camNameTx', q = True, si = True)
    camCtrl = pm.textScrollList('camCtrlTx', q = True, si = True)
    assetName = pm.textScrollList('assetNameTx', q = True, si = True)
    assetCtrl = pm.textScrollList('assetCtrlTx', q = True, si = True)
    ctrlList.selectControllers(camName, camCtrl, assetName, assetCtrl)
    
def selectCamCtrl(*args):
    mode = pm.checkBox('multiSelChk', q = True, v = True)
    if not mode:
        pm.textScrollList('assetNameTx', e = True, da = True)
        pm.textScrollList('assetCtrlTx', e = True, da = True)
    selectCtrl()
    
def selectAssetCtrl(*args):
    mode = pm.checkBox('multiSelChk', q = True, v = True)
    if not mode:
        pm.textScrollList('camNameTx', e = True, da = True)
        pm.textScrollList('camCtrlTx', e = True, da = True)
    selectCtrl()
    
def selectCurrentShot(*args):
    pm.textScrollList('camCtrlTx', e = True, da = True)
    currentShotName, shotStart, shotEnd = ctrlList.currentShot()
    pm.textScrollList('camNameTx', e = True, da = True, si = currentShotName)
    pm.playbackOptions(ast = shotStart, min = shotStart, aet = shotEnd, max = shotEnd)
    
def snapToRefCam(*args):
    refCam = pm.text('refCamTx', q = True, l = True)
    focal = pm.getAttr('%s.focalLength' %refCam)
    camName = pm.textScrollList('camNameTx', q = True, si = True)[-1]
    camCtrl = pm.textScrollList('camCtrlTx', q = True, si = True)[-1]
    ctrlList.snapToRefCam(camName, camCtrl, refCam, focal)
    
def clearSelection(*args):
    pm.textScrollList('camNameTx', e = True, da = True)
    pm.textScrollList('camCtrlTx', e = True, da = True)
    pm.textScrollList('assetNameTx', e = True, da = True)
    pm.textScrollList('assetCtrlTx', e = True, da = True)
    selectCtrl()
    
# -------- copy/paste shake
shakeValueGlobal = []

def copyShake(*args):
    shakeValue = ctrlList.copyShakeProc()
    global shakeValueGlobal
    ctrlList.shakeValueGlobal = shakeValue
    
def pasteShake(*args):
    global shakeValueGlobal
    ctrlList.pasteShakeProc(shakeValueGlobal)

################################

def UI():
    if pm.window('layoutToolsWin', q = True, exists = True):
        pm.deleteUI('layoutToolsWin')
        
    app = pm.window('layoutToolsWin', t = 'Layout Tools')
    tabs = pm.tabLayout(imw = 5, imh = 5)
    
    ################################
    
    colMain1 = pm.columnLayout(adj = True, rs = 5)
    with colMain1:
        pm.separator(style = 'none')
        #pm.text(l = 'Preparing Camera', al = 'left', fn = 'boldLabelFont')
        row1 = pm.rowLayout(nc = 3,  adj = 2, columnAttach = [(1,'both',5),(2,'both',5),(3,'both',5)])
        with row1:
            pm.text(l = 'Ref. camera: ')
            pm.text('refCamTx', l = '%s' %LT.getPref("refCam"), fn = 'boldLabelFont', w = 80, ww = True)
            pm.button(l = 'Set', w = 70, c = setRefCamName)
        row4 = pm.rowLayout(nc = 2, adj = 1)
        with row4:
            pm.text(l = 'Ref. cam lens (mm):  ', al = 'left')
            pm.button(l = '...', h = 15, c = setCustomLens)
        rowCol2 = pm.rowColumnLayout(nc = 3, cw = ([1,81],[2,81],[3,81]), cs = ([2,5],[3,5]), rs = ([1,5]))
        with rowCol2:
            for i in LT.getPref("lensList"):
                pm.button(l = str(i) + ' mm', c = lambda x, fl = i: setsetRefCamFocal(fl))
        pm.separator()
        #pm.text(l = 'Camera Controllers', al = 'left', fn = 'boldLabelFont')
        rowCol1 = pm.rowColumnLayout(nc = 2, cw = ([1,130],[2,120]), cs = [2,5], rs = ([1,5]))
        with rowCol1:
            pm.text(l = 'Camera:', al = 'left')
            pm.text(l = 'Controller:', al = 'left')
            pm.textScrollList('camNameTx', ams = True, sc = selectCamCtrl)
            pm.textScrollList('camCtrlTx', ams = True, sc = selectCamCtrl)
            pm.button(l = 'Current Shot', c = selectCurrentShot)
            pm.button(l = 'Snap to Ref. Cam', c = snapToRefCam)
        pm.separator()
        #pm.text(l = 'Asset Controllers', al = 'left', fn = 'boldLabelFont')
        rowCol3 = pm.rowColumnLayout(nc = 2, cw = ([1,130],[2,120]), cs = [2,5], rs = ([1,5]))
        with rowCol3:
            pm.text(l = 'Asset:', al = 'left')
            pm.text(l = 'Controller:', al = 'left')
            pm.textScrollList('assetNameTx', ams = True, sc = selectAssetCtrl)
            pm.textScrollList('assetCtrlTx', ams = True, sc = selectAssetCtrl)
            pm.checkBox('multiSelChk', l = 'Multi-selection')
            pm.button(l = 'Clear Selection', c = clearSelection)
        pm.separator()
        row3 = pm.rowLayout(nc = 2, adj = 1)
        with row3:
            pm.text(l = 'Shortcuts  ', al = 'left', fn = 'boldLabelFont')
            pm.button(l = '...', h = 15, c = setCustomScript)
        rowCol4 = pm.rowColumnLayout(nc = 2, cw = ([1,125],[2,125]), cs = ([2,5]), rs = ([1,5]))
        with rowCol4:
            pm.button(l = 'Copy Shake Value', c = copyShake)
            pm.button(l = 'Paste Shake Value', c = pasteShake)
            for i in LT.getPref("customScriptBtn"):
                pm.button(l = i, c = lambda x, i = i: runScriptBtn(i))
            
    ################################
    
    colMain2 = pm.columnLayout(adj = True, rs = 5, cat = ('both', 5))
    with colMain2:
        pm.separator(style = 'none')
        pm.text(l = 'Scripts:', al = 'left')
        pm.textScrollList('scriptsTx', h = 400, w = 100, sc = getScriptDescription, dcc = runScriptTx)
        pm.text(l = 'Descriptions:', al = 'left')
        pm.scrollField('scriptDescriptionTx', w = 100, ww = True, ed = False, bgc = [0.22,0.22,0.22])
        row2 = pm.rowLayout(nc = 3, adj = 2, columnAttach = [(1,'both',2),(2,'both',2),(3,'both',2)])
        with row2:
            pm.button(l = 'Run', w = 100, c = runScriptTx)
            pm.button(l = 'Add to Shelf', c = addScriptToShelf)
            pm.button(l = '?', w = 25, c = openManual)
            
    ################################
    
    with app:
        pm.tabLayout(tabs, e = True, tabLabel = ((colMain1, 'Layout'), (colMain2, 'Scripts')))

    pm.showWindow('layoutToolsWin')
    
def initial():
    UI()
    appendCtrlList()
    appendScriptList()
    
initial()