import maya.cmds as mc
from lay_app import lay_app_core
from lay_app import lay_app_ctrlList

try:
    reload(lay_app_core)
    reload(lay_app_ctrlList)
except:
    import importlib
    importlib.reload(lay_app_core)
    importlib.reload(lay_app_ctrlList)


class LayoutToolUI:
    def __init__(self, *args, **kwargs):

        self.selMode = False
        self.shakeValue = []
        self.core = lay_app_core.LayoutToolCore()
        self.ctrl = lay_app_ctrlList.LayoutToolCtrl()

        self.camLs, self.assetLs = self.ctrl.getNameList()
        self.scriptLs = self.core.getScripts()
        
        if mc.window('layoutToolsWin', q = True, exists = True):
            mc.deleteUI('layoutToolsWin')
            # mc.deleteUI('layoutToolsDock')
            
        mc.window('layoutToolsWin', t = 'Layout Tools', nde=True) #, tlb=True, rtf=True, ip=True
        self.tabs = mc.tabLayout(imw = 5, imh = 5)
        
        ################################
        
        self.tabA = mc.columnLayout(adj = True, rs = 5)
        mc.separator(style = 'none')
        
        mc.rowLayout('refcamRow', nc = 3,  adj = 2, columnAttach = [(1,'both',5),(2,'both',5),(3,'both',5)])
        mc.text(l = 'Ref. camera: ')
        mc.text('refCamTx', l = '%s' %self.core.getPref("refCam"), fn = 'boldLabelFont', w = 80, ww = True)
        mc.button(l = 'Set', w = 70, c = self.setRefCamName)
        mc.setParent('..')
        
        mc.rowLayout('refcamlensTitleRow', nc = 2, adj = 1)
        mc.text(l = 'Ref. cam lens (mm):  ', al = 'left')
        mc.button(l = '...', h = 15, c = SetCustomLensUI)
        mc.setParent('..')
        
        mc.rowColumnLayout('refcamlensGrid', nc = 3, cw = ([1,81],[2,81],[3,81]), cs = ([2,5],[3,5]), rs = ([1,5]))
        for i in self.core.getPref("lensList"):
            mc.button(l = str(i) + ' mm', c = lambda x, fl = i: self.setRefCamFocal(fl))
        mc.setParent('..')

        mc.separator()
        mc.rowColumnLayout('camlistGrid', nc = 2, cw = ([1,130],[2,120]), cs = [2,5], rs = ([1,5]))
        mc.text(l = 'Camera:', al = 'left')
        mc.text(l = 'Controller:', al = 'left')
        mc.textScrollList('camNameTx', ams = True, h = 200, 
                            append = self.camLs, 
                            sc = self.selectCamCtrl)
        mc.textScrollList('camCtrlTx', ams = True, h = 200, 
                            append = self.ctrl.camCtrlLs, 
                            lf = self.ctrl.camCtrlFn, 
                            sc = self.selectCamCtrl)
        mc.button(l = 'Current Shot', c = self.selectCurrentShot)
        mc.button(l = 'Snap to Ref. Cam', c = self.snapToRefCam)
        mc.setParent('..')

        mc.separator()
        mc.rowColumnLayout('assetlistGrid', nc = 2, cw = ([1,130],[2,120]), cs = [2,5], rs = ([1,5]))
        mc.text(l = 'Asset:', al = 'left')
        mc.text(l = 'Controller:', al = 'left')
        mc.textScrollList('assetNameTx', ams = True, h = 200, 
                            append = self.assetLs, 
                            sc = self.selectAssetCtrl)
        mc.textScrollList('assetCtrlTx', ams = True, h = 200, 
                            append = self.ctrl.assetCtrlLs, 
                            lf = self.ctrl.assetCtrlFn, 
                            sc = self.selectAssetCtrl)
        mc.checkBox('multiSelChk', l = 'Multi-selection', cc = self.setSelectionMode)
        mc.button(l = 'Clear Selection', c = self.clearSelection)
        mc.setParent('..')

        mc.separator()
        mc.rowLayout('shortcuttitleRow', nc = 2, adj = 1)
        mc.text(l = 'Shortcuts  ', al = 'left', fn = 'boldLabelFont')
        mc.button(l = '...', h = 15, c = SetCustomScriptBtnUI)
        mc.setParent('..')
        
        mc.rowColumnLayout('shortcutbtnGrid', nc = 2, cw = ([1,125],[2,125]), cs = ([2,5]), rs = ([1,5]))
        mc.button(l = 'Copy Shake Value', c = self.copyShake)
        mc.button(l = 'Paste Shake Value', c = self.pasteShake)
        for i in self.core.getPref("customScriptBtn"):
            mc.button(l = i, bgc = (0.3,0.3,0.3), c = lambda x, i = i: self.runScriptBtn(i))
        mc.setParent('..')

        mc.separator()
        mc.button(l = 'Refresh', h = 20, c = self.refresh)
        mc.setParent('..')
                
        ################################
        
        self.TabB = mc.columnLayout(adj = True, rs = 5, cat = ('both', 5))
        mc.separator(style = 'none')
        mc.text(l = 'Scripts:', al = 'left')
        mc.textScrollList('scriptsTx', h = 400, w = 100, 
                            append = self.scriptLs, 
                            sc = self.getScriptDescription, 
                            dcc = self.runScriptTx)
        mc.text(l = 'Descriptions:', al = 'left')
        mc.scrollField('scriptDescriptionTx', w = 100, h = 200, ww = True, ed = False, bgc = [0.22,0.22,0.22])

        mc.rowLayout('scriptBtnRow', nc = 3, adj = 2, columnAttach = [(1,'both',2),(2,'both',2),(3,'both',2)])
        mc.button(l = 'Run', w = 100, c = self.runScriptTx)
        mc.button(l = 'Add to Shelf', c = self.addScriptToShelf)
        mc.button(l = '?', w = 25, c = self.core.openCustomDir)
                
        ################################

        mc.tabLayout(self.tabs, e = True, tabLabel = ((self.tabA, 'Layout'), (self.TabB, 'Scripts')))
    
        mc.showWindow('layoutToolsWin')
        # mc.dockControl('layoutToolsDock', label='Layout Tools', area='left', content='layoutToolsWin', allowedArea=['left', 'right'], floating=True)

        
    ################################
        
    # -------- basic ui process

    def refresh(self, *args):
        self.camLs, self.assetLs = self.ctrl.getNameList()
        self.scriptLs = self.core.getScripts()
        mc.textScrollList('camNameTx', e = True, ra = True)
        mc.textScrollList('assetNameTx', e = True, ra = True)
        mc.textScrollList('camNameTx', e = True, append = self.camLs)
        mc.textScrollList('assetNameTx', e = True, append = self.assetLs)
        mc.textScrollList('scriptsTx', e = True, ra = True)
        mc.textScrollList('scriptsTx', e = True, append = self.scriptLs)
        
    def getScriptDescription(self, *args):
        scriptName = mc.textScrollList('scriptsTx', q = True, si = True)[0]
        mc.scrollField('scriptDescriptionTx', e = True, cl = True)
        mc.scrollField('scriptDescriptionTx', e = True, tx = self.core.getScripDescription(scriptName))
        
    def runScriptTx(self, *args):
        scriptName = mc.textScrollList('scriptsTx', q = True, si = True)[0]
        self.core.runScript(scriptName)
        
    def runScriptBtn(self, scriptName):
        self.core.runScript(scriptName)
        
    def addScriptToShelf(self, *args):
        scriptName = mc.textScrollList('scriptsTx', q = True, si = True)[0]
        self.core.addScriptToShelf(scriptName)
        
    # -------- ref cam
    def setRefCamName(self, *args):
        refCamStr = str(mc.ls(sl = True)[0])
        self.core.savePref("refCam", refCamStr)
        mc.text('refCamTx', e = True, l = '%s' %refCamStr)
        
    def setRefCamFocal(self, fl):
        refCam = mc.text('refCamTx', q = True, l = True)
        refCamShape = mc.ls(refCam)
        mc.setAttr("{}.focalLength".format(refCamShape[-1]), fl)
        
    # -------- ctrl selection
    def selectCtrl(self, *args):
        camName = mc.textScrollList('camNameTx', q = True, si = True)
        camCtrl = mc.textScrollList('camCtrlTx', q = True, si = True)
        assetName = mc.textScrollList('assetNameTx', q = True, si = True)
        assetCtrl = mc.textScrollList('assetCtrlTx', q = True, si = True)
        self.ctrl.selectControllers(self.selMode, camName, camCtrl, assetName, assetCtrl)
        
    def selectCamCtrl(self, *args):
        if not self.selMode:
            mc.textScrollList('assetNameTx', e = True, da = True)
            mc.textScrollList('assetCtrlTx', e = True, da = True)
        self.selectCtrl(self.selMode)
        
    def selectAssetCtrl(self, *args):
        if not self.selMode:
            mc.textScrollList('camNameTx', e = True, da = True)
            mc.textScrollList('camCtrlTx', e = True, da = True)
        self.selectCtrl(self.selMode)

    def setSelectionMode(self, *args):
        mode = mc.checkBox('multiSelChk', q = True, v = True)
        if mode:
            self.selMode = True
        else:
            self.selMode = False
        
    def selectCurrentShot(self, *args):
        mc.textScrollList('camCtrlTx', e = True, da = True)
        currentShotName, shotStart, shotEnd = self.ctrl.currentShot()
        mc.textScrollList('camNameTx', e = True, da = True, si = currentShotName)
        mc.playbackOptions(ast = shotStart, min = shotStart, aet = shotEnd, max = shotEnd)
        
    def snapToRefCam(self, *args):
        refCam = mc.text('refCamTx', q = True, l = True)
        focal = mc.getAttr('%s.focalLength' %refCam)
        camName = mc.textScrollList('camNameTx', q = True, si = True)[-1]
        camCtrl = mc.textScrollList('camCtrlTx', q = True, si = True)[-1]
        self.ctrl.snapToRefCam(camName, camCtrl, refCam, focal)
        
    def clearSelection(self, *args):
        mc.textScrollList('camNameTx', e = True, da = True)
        mc.textScrollList('camCtrlTx', e = True, da = True)
        mc.textScrollList('assetNameTx', e = True, da = True)
        mc.textScrollList('assetCtrlTx', e = True, da = True)
        self.selectCtrl(self.selMode)
        
    # -------- copy/paste shake
    
    def copyShake(self, *args):
        self.ctrl.copyShakeProc()
        
    def pasteShake(self, *args):
        self.ctrl.pasteShakeProc()


class SetCustomLensUI(LayoutToolUI):
    def __init__(self, *args, **kwargs):

        self.core = lay_app_core.LayoutToolCore()
        self.ctrl = lay_app_ctrlList.LayoutToolCtrl()

        lensLs = self.core.getPref("lensList")
        
        if mc.window('setLensWin', q = True, exists = True):
            mc.deleteUI('setLensWin')

        mc.window('setLensWin', t = 'Set Ref. Cam Lens')
        mc.columnLayout()

        mc.rowColumnLayout(nc = 3)
        mc.intField('int1', v = lensLs[0])
        mc.intField('int2', v = lensLs[1])
        mc.intField('int3', v = lensLs[2])
        mc.intField('int4', v = lensLs[3])
        mc.intField('int5', v = lensLs[4])
        mc.intField('int6', v = lensLs[5])
        mc.setParent('..')

        mc.rowLayout(nc = 2)
        mc.button(l = 'OK', w = 100, c = self.okBtn)
        mc.button(l = 'Cancel', w = 100, c = self.cancelBtn)
        
        mc.showWindow('setLensWin')
    
    def okBtn(self, *args):
        lensLs = []
        lensLs.append(mc.intField('int1', q = True, v = True))
        lensLs.append(mc.intField('int2', q = True, v = True))
        lensLs.append(mc.intField('int3', q = True, v = True))
        lensLs.append(mc.intField('int4', q = True, v = True))
        lensLs.append(mc.intField('int5', q = True, v = True))
        lensLs.append(mc.intField('int6', q = True, v = True))
        self.core.savePref("lensList", lensLs)
        mc.deleteUI('setLensWin')
        LayoutToolUI()
        
    def cancelBtn(self, *args):
        mc.deleteUI('setLensWin')


class SetCustomScriptBtnUI(LayoutToolUI):
    def __init__(self, *args, **kwargs):

        self.core = lay_app_core.LayoutToolCore()
        self.ctrl = lay_app_ctrlList.LayoutToolCtrl()

        scriptLs = self.core.getScripts()
        btnLs = self.core.getPref("customScriptBtn")
        scroll_w = 200
        scroll_h = 200
        btnWidth = 100
        if mc.window('setBtnWin', q = True, exists = True):
            mc.deleteUI('setBtnWin')
            
        mc.window('setBtnWin', t = 'Set Custom Script Button')
        mc.columnLayout(adj = True)
        mc.separator(style = 'none', h = 5)

        mc.rowColumnLayout(nc = 3, cat = ([1,'both',5],[3,'both',5]), rs = ([1,5]))
        mc.text(l = 'Scripts', al = 'left')
        mc.separator(style = 'none')
        mc.text(l = 'Custom Buttons', al = 'left')
        
        mc.textScrollList('allScriptTx', w = scroll_w, h = scroll_h,
                            append = scriptLs, ams = True, 
                            sc = self.getScriptDescription, 
                            dcc = self.addCustomScript)
        mc.text(l = '->')
        mc.textScrollList('customScriptTx', w = scroll_w, h = scroll_h, append = btnLs, ams = True)
        
        mc.button(l = 'Add ->', c = self.addCustomScript)
        mc.separator(style = 'none')

        mc.rowLayout(nc = 3, adj = 3, cat = (2, 'right', 5))
        mc.button(l = '^', w = 30, c = self.moveUpTxLs)
        mc.button(l = 'v', w = 30, c = self.moveDownTxLs)
        mc.button(l = 'Remove', c = self.removeTxLs)
        mc.setParent('..')
        
        mc.text(l = 'Description', al = 'left')
        mc.separator(style = 'none')
        mc.separator(style = 'none')
        
        mc.scrollField('descriptionTx', w = scroll_w, h = scroll_h, ed = False, ww = True, bgc = [0.22,0.22,0.22])
        mc.separator(style = 'none')

        mc.columnLayout(adj = True, rs = 5)
        mc.separator(h = 150, style = 'none')
        mc.button(l = 'OK', c = self.okBtn)
        mc.button(l = 'Cancel', c = self.cancelBtn)
        mc.separator(style = 'none')
        mc.setParent('..')
        
        mc.setParent('..')
        mc.separator(style = 'none', h = 5)

        mc.showWindow('setBtnWin')

    def getScriptDescription(self, *args):
        scriptName = mc.textScrollList('allScriptTx', q = True, si = True)[0]
        mc.scrollField('descriptionTx', e = True, cl = True)
        mc.scrollField('descriptionTx', e = True, tx = self.core.getScripDescription(scriptName))
        
    def addCustomScript(self, *args):
        scriptName = mc.textScrollList('allScriptTx', q = True, si = True)
        for i in scriptName:
            mc.textScrollList('customScriptTx', e = True, append = i)
            mc.textScrollList('customScriptTx', e = True, da = True)
            mc.textScrollList('customScriptTx', e = True, si = i)
        
    def removeTxLs(self, *args):
        selScript = mc.textScrollList('customScriptTx', q = True, si = True)
        for i in selScript:
            mc.textScrollList('customScriptTx', e = True, ri = i)
        
    def moveUpTxLs(self, *args):
        selIndex = mc.textScrollList('customScriptTx', q = True, sii = True)
        allItem = mc.textScrollList('customScriptTx', q = True, ai = True)
        for i in selIndex:
            if i != 1:
                mc.textScrollList('customScriptTx', e = True, rii = i)
                mc.textScrollList('customScriptTx', e = True, ap = [i-1, allItem[i-1]])
                mc.textScrollList('customScriptTx', e = True, sii = i-1)
        
    def moveDownTxLs(self, *args):
        count = mc.textScrollList('customScriptTx', q = True, ni = True)
        selIndex = mc.textScrollList('customScriptTx', q = True, sii = True)
        allItem = mc.textScrollList('customScriptTx', q = True, ai = True)
        selIndex.reverse()
        for i in selIndex:
            if i != count:
                mc.textScrollList('customScriptTx', e = True, rii = i)
                mc.textScrollList('customScriptTx', e = True, ap = [i+1, allItem[i-1]])
                mc.textScrollList('customScriptTx', e = True, sii = i+1)
        
    def okBtn(self, *args):
        self.core.savePref("customScriptBtn", mc.textScrollList('customScriptTx', q = True, ai = True))
        mc.deleteUI('setBtnWin')
        LayoutToolUI()
        
    def cancelBtn(self, *args):
        mc.deleteUI('setBtnWin')
