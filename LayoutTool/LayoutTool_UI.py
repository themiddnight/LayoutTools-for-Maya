from imp import reload
import pymel.core as pm
import LayoutTool_core
import LayoutTool_ctrlList
reload(LayoutTool_core)
reload(LayoutTool_ctrlList)


################################

class LayoutToolUI:
    def __init__(self, *args, **kwargs):

        self.selMode = False
        self.shakeValue = []
        self.core = LayoutTool_core.LayoutToolCore()
        self.ctrl = LayoutTool_ctrlList.LayoutToolCtrl()

        self.camLs, self.assetLs = self.ctrl.getNameList()
        self.scriptLs = self.core.getScripts()
        
        if pm.window('layoutToolsWin', q = True, exists = True):
            pm.deleteUI('layoutToolsWin')
            
        self.app = pm.window('layoutToolsWin', t = 'Layout Tools')
        self.tabs = pm.tabLayout(imw = 5, imh = 5)
        
        ################################
        
        self.colMain1 = pm.columnLayout(adj = True, rs = 5)
        with self.colMain1:
            pm.separator(style = 'none')
            self.row1 = pm.rowLayout(nc = 3,  adj = 2, columnAttach = [(1,'both',5),(2,'both',5),(3,'both',5)])
            with self.row1:
                pm.text(l = 'Ref. camera: ')
                pm.text('refCamTx', l = '%s' %self.core.getPref("refCam"), fn = 'boldLabelFont', w = 80, ww = True)
                pm.button(l = 'Set', w = 70, c = self.setRefCamName)
            self.row4 = pm.rowLayout(nc = 2, adj = 1)
            with self.row4:
                pm.text(l = 'Ref. cam lens (mm):  ', al = 'left')
                pm.button(l = '...', h = 15, c = SetCustomLensUI)
            self.rowCol2 = pm.rowColumnLayout(nc = 3, cw = ([1,81],[2,81],[3,81]), cs = ([2,5],[3,5]), rs = ([1,5]))
            with self.rowCol2:
                for i in self.core.getPref("lensList"):
                    pm.button(l = str(i) + ' mm', c = lambda x, fl = i: self.setsetRefCamFocal(fl))
            pm.separator()
            self.rowCol1 = pm.rowColumnLayout(nc = 2, cw = ([1,130],[2,120]), cs = [2,5], rs = ([1,5]))
            with self.rowCol1:
                pm.text(l = 'Camera:', al = 'left')
                pm.text(l = 'Controller:', al = 'left')
                pm.textScrollList('camNameTx', ams = True, h = 200, 
                                  append = self.camLs, 
                                  sc = self.selectCamCtrl)
                pm.textScrollList('camCtrlTx', ams = True, h = 200, 
                                  append = self.ctrl.camCtrlLs, 
                                  lf = self.ctrl.camCtrlFn, 
                                  sc = self.selectCamCtrl)
                pm.button(l = 'Current Shot', c = self.selectCurrentShot)
                pm.button(l = 'Snap to Ref. Cam', c = self.snapToRefCam)
            pm.separator()
            self.rowCol3 = pm.rowColumnLayout(nc = 2, cw = ([1,130],[2,120]), cs = [2,5], rs = ([1,5]))
            with self.rowCol3:
                pm.text(l = 'Asset:', al = 'left')
                pm.text(l = 'Controller:', al = 'left')
                pm.textScrollList('assetNameTx', ams = True, h = 200, 
                                  append = self.assetLs, 
                                  sc = self.selectAssetCtrl)
                pm.textScrollList('assetCtrlTx', ams = True, h = 200, 
                                  append = self.ctrl.assetCtrlLs, 
                                  lf = self.ctrl.assetCtrlFn, 
                                  sc = self.selectAssetCtrl)
                pm.checkBox('multiSelChk', l = 'Multi-selection', cc = self.setSelectionMode)
                pm.button(l = 'Clear Selection', c = self.clearSelection)
            pm.separator()
            self.row3 = pm.rowLayout(nc = 2, adj = 1)
            with self.row3:
                pm.text(l = 'Shortcuts  ', al = 'left', fn = 'boldLabelFont')
                pm.button(l = '...', h = 15, c = SetCustomScriptBtnUI)
            self.rowCol4 = pm.rowColumnLayout(nc = 2, cw = ([1,125],[2,125]), cs = ([2,5]), rs = ([1,5]))
            with self.rowCol4:
                pm.button(l = 'Copy Shake Value', c = self.copyShake)
                pm.button(l = 'Paste Shake Value', c = self.pasteShake)
                for i in self.core.getPref("customScriptBtn"):
                    pm.button(l = i, c = lambda x, i = i: self.runScriptBtn(i))
                
        ################################
        
        colMain2 = pm.columnLayout(adj = True, rs = 5, cat = ('both', 5))
        with colMain2:
            pm.separator(style = 'none')
            pm.text(l = 'Scripts:', al = 'left')
            pm.textScrollList('scriptsTx', h = 400, w = 100, 
                              append = self.scriptLs, 
                              sc = self.getScriptDescription, 
                              dcc = self.runScriptTx)
            pm.text(l = 'Descriptions:', al = 'left')
            pm.scrollField('scriptDescriptionTx', w = 100, h = 200, ww = True, ed = False, bgc = [0.22,0.22,0.22])
            row2 = pm.rowLayout(nc = 3, adj = 2, columnAttach = [(1,'both',2),(2,'both',2),(3,'both',2)])
            with row2:
                pm.button(l = 'Run', w = 100, c = self.runScriptTx)
                pm.button(l = 'Add to Shelf', c = self.addScriptToShelf)
                pm.button(l = '?', w = 25, c = self.core.openCustomDir)
                
        ################################
        
        with self.app:
            pm.tabLayout(self.tabs, e = True, tabLabel = ((self.colMain1, 'Layout'), (colMain2, 'Scripts')))
    
        pm.showWindow('layoutToolsWin')
        
    # -------- basic ui process
        
    def getScriptDescription(self, *args):
        scriptName = pm.textScrollList('scriptsTx', q = True, si = True)[0]
        pm.scrollField('scriptDescriptionTx', e = True, cl = True)
        pm.scrollField('scriptDescriptionTx', e = True, tx = self.core.getScripDescription(scriptName))
        
    def runScriptTx(self, *args):
        scriptName = pm.textScrollList('scriptsTx', q = True, si = True)[0]
        self.core.runScript(scriptName, 'tool')
        
    def runScriptBtn(self, scriptName):
        self.core.runScript(scriptName, 'button')
        
    def addScriptToShelf(self, *args):
        scriptName = pm.textScrollList('scriptsTx', q = True, si = True)[0]
        self.core.addScriptToShelf(scriptName)
        
    # -------- ref cam
    def setRefCamName(self, *args):
        refCamStr = str(pm.ls(sl = True)[0])
        self.core.savePref("refCam", refCamStr)
        pm.text('refCamTx', e = True, l = '%s' %refCamStr)
        
    def setsetRefCamFocal(self, fl):
        refCam = pm.text('refCamTx', q = True, l = True)
        refCamShape = pm.ls(refCam)
        pm.setAttr(refCamShape[-1].focalLength, fl)
        
    # -------- ctrl selection
    def selectCtrl(self, *args):
        camName = pm.textScrollList('camNameTx', q = True, si = True)
        camCtrl = pm.textScrollList('camCtrlTx', q = True, si = True)
        assetName = pm.textScrollList('assetNameTx', q = True, si = True)
        assetCtrl = pm.textScrollList('assetCtrlTx', q = True, si = True)
        self.ctrl.selectControllers(self.selMode, camName, camCtrl, assetName, assetCtrl)
        
    def selectCamCtrl(self, *args):
        if not self.selMode:
            pm.textScrollList('assetNameTx', e = True, da = True)
            pm.textScrollList('assetCtrlTx', e = True, da = True)
        self.selectCtrl(self.selMode)
        
    def selectAssetCtrl(self, *args):
        if not self.selMode:
            pm.textScrollList('camNameTx', e = True, da = True)
            pm.textScrollList('camCtrlTx', e = True, da = True)
        self.selectCtrl(self.selMode)

    def setSelectionMode(self, *args):
        mode = pm.checkBox('multiSelChk', q = True, v = True)
        if mode:
            self.selMode = True
        else:
            self.selMode = False
        
    def selectCurrentShot(self, *args):
        pm.textScrollList('camCtrlTx', e = True, da = True)
        currentShotName, shotStart, shotEnd = self.ctrl.currentShot()
        pm.textScrollList('camNameTx', e = True, da = True, si = currentShotName)
        pm.playbackOptions(ast = shotStart, min = shotStart, aet = shotEnd, max = shotEnd)
        
    def snapToRefCam(self, *args):
        refCam = pm.text('refCamTx', q = True, l = True)
        focal = pm.getAttr('%s.focalLength' %refCam)
        camName = pm.textScrollList('camNameTx', q = True, si = True)[-1]
        camCtrl = pm.textScrollList('camCtrlTx', q = True, si = True)[-1]
        self.ctrl.snapToRefCam(camName, camCtrl, refCam, focal)
        
    def clearSelection(self, *args):
        pm.textScrollList('camNameTx', e = True, da = True)
        pm.textScrollList('camCtrlTx', e = True, da = True)
        pm.textScrollList('assetNameTx', e = True, da = True)
        pm.textScrollList('assetCtrlTx', e = True, da = True)
        self.selectCtrl(self.selMode)
        
    # -------- copy/paste shake
    
    def copyShake(self, *args):
        self.ctrl.copyShakeProc()
        
    def pasteShake(self, *args):
        self.ctrl.pasteShakeProc()


class SetCustomLensUI(LayoutToolUI):
    def __init__(self, *args, **kwargs):

        self.core = LayoutTool_core.LayoutToolCore()
        self.ctrl = LayoutTool_ctrlList.LayoutToolCtrl()

        lensLs = self.core.getPref("lensList")
        
        if pm.window('setLensWin', q = True, exists = True):
            pm.deleteUI('setLensWin')

        app = pm.window('setLensWin', t = 'Set Ref. Cam Lens')

        with app:
            main = pm.columnLayout()
            with main:
                lensField = pm.rowColumnLayout(nc = 3)
                with lensField:
                    pm.intField('int1', v = lensLs[0])
                    pm.intField('int2', v = lensLs[1])
                    pm.intField('int3', v = lensLs[2])
                    pm.intField('int4', v = lensLs[3])
                    pm.intField('int5', v = lensLs[4])
                    pm.intField('int6', v = lensLs[5])
                row1 = pm.rowLayout(nc = 2)
                with row1:
                    pm.button(l = 'OK', w = 100, c = self.okBtn)
                    pm.button(l = 'Cancel', w = 100, c = self.cancelBtn)
        
        #pm.showWindow('setLensWin')
    
    def okBtn(self, *args):
        lensLs = []
        lensLs.append(pm.intField('int1', q = True, v = True))
        lensLs.append(pm.intField('int2', q = True, v = True))
        lensLs.append(pm.intField('int3', q = True, v = True))
        lensLs.append(pm.intField('int4', q = True, v = True))
        lensLs.append(pm.intField('int5', q = True, v = True))
        lensLs.append(pm.intField('int6', q = True, v = True))
        self.core.savePref("lensList", lensLs)
        pm.deleteUI('setLensWin')
        LayoutToolUI()
        
    def cancelBtn(self, *args):
        pm.deleteUI('setLensWin')


class SetCustomScriptBtnUI(LayoutToolUI):
    def __init__(self, *args, **kwargs):

        self.core = LayoutTool_core.LayoutToolCore()
        self.ctrl = LayoutTool_ctrlList.LayoutToolCtrl()

        scriptLs = self.core.getScripts()
        btnLs = self.core.getPref("customScriptBtn")
        scroll_w = 200
        scroll_h = 200
        btnWidth = 100
        if pm.window('setBtnWin', q = True, exists = True):
            pm.deleteUI('setBtnWin')
        
        app = pm.window('setBtnWin', t = 'Set Custom Script Button')
        with app:
            main = pm.columnLayout(adj = True)
            with main:
                pm.separator(style = 'none', h = 5)
                col1 = pm.rowColumnLayout(nc = 3, cat = ([1,'both',5],[3,'both',5]), rs = ([1,5]))
                with col1:
                    pm.text(l = 'Scripts', al = 'left')
                    pm.separator(style = 'none')
                    pm.text(l = 'Custom Buttons', al = 'left')
                    
                    pm.textScrollList('allScriptTx', w = scroll_w, h = scroll_h,
                                      append = scriptLs, ams = True, 
                                      sc = self.getScriptDescription, 
                                      dcc = self.addCustomScript)
                    pm.text(l = '->')
                    pm.textScrollList('customScriptTx', w = scroll_w, h = scroll_h, append = btnLs, ams = True)
                    
                    pm.button(l = 'Add ->', c = self.addCustomScript)
                    pm.separator(style = 'none')
                    row1 = pm.rowLayout(nc = 3, adj = 3, cat = (2, 'right', 5))
                    with row1:
                        pm.button(l = '^', w = 30, c = self.moveUpTxLs)
                        pm.button(l = 'v', w = 30, c = self.moveDownTxLs)
                        pm.button(l = 'Remove', c = self.removeTxLs)
                    
                    pm.text(l = 'Description', al = 'left')
                    pm.separator(style = 'none')
                    pm.separator(style = 'none')
                    
                    pm.scrollField('descriptionTx', w = scroll_w, h = scroll_h, ed = False, ww = True, bgc = [0.22,0.22,0.22])
                    pm.separator(style = 'none')
                    col2 = pm.columnLayout(adj = True, rs = 5)
                    with col2:
                        pm.separator(h = 150, style = 'none')
                        pm.button(l = 'OK', c = self.okBtn)
                        pm.button(l = 'Cancel', c = self.cancelBtn)
                        pm.separator(style = 'none')
                pm.separator(style = 'none', h = 5)

        #pm.showWindow('setBtnWin')

    def getScriptDescription(self, *args):
        reload(LayoutTool_core)
        scriptName = pm.textScrollList('allScriptTx', q = True, si = True)[0]
        pm.scrollField('descriptionTx', e = True, cl = True)
        pm.scrollField('descriptionTx', e = True, tx = self.core.getScripDescription(scriptName))
        
    def addCustomScript(self, *args):
        scriptName = pm.textScrollList('allScriptTx', q = True, si = True)
        for i in scriptName:
            pm.textScrollList('customScriptTx', e = True, append = i)
            pm.textScrollList('customScriptTx', e = True, da = True)
            pm.textScrollList('customScriptTx', e = True, si = i)
        
    def removeTxLs(self, *args):
        selScript = pm.textScrollList('customScriptTx', q = True, si = True)
        for i in selScript:
            pm.textScrollList('customScriptTx', e = True, ri = i)
        
    def moveUpTxLs(self, *args):
        selIndex = pm.textScrollList('customScriptTx', q = True, sii = True)
        allItem = pm.textScrollList('customScriptTx', q = True, ai = True)
        for i in selIndex:
            if i != 1:
                pm.textScrollList('customScriptTx', e = True, rii = i)
                pm.textScrollList('customScriptTx', e = True, ap = [i-1, allItem[i-1]])
                pm.textScrollList('customScriptTx', e = True, sii = i-1)
        
    def moveDownTxLs(self, *args):
        count = pm.textScrollList('customScriptTx', q = True, ni = True)
        selIndex = pm.textScrollList('customScriptTx', q = True, sii = True)
        allItem = pm.textScrollList('customScriptTx', q = True, ai = True)
        selIndex.reverse()
        for i in selIndex:
            if i != count:
                pm.textScrollList('customScriptTx', e = True, rii = i)
                pm.textScrollList('customScriptTx', e = True, ap = [i+1, allItem[i-1]])
                pm.textScrollList('customScriptTx', e = True, sii = i+1)
        
    def okBtn(self, *args):
        self.core.savePref("customScriptBtn", pm.textScrollList('customScriptTx', q = True, ai = True))
        pm.deleteUI('setBtnWin')
        LayoutToolUI()
        
    def cancelBtn(self, *args):
        pm.deleteUI('setBtnWin')