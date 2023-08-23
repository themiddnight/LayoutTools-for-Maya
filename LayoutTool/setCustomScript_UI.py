import pymel.core as pm
import LayoutTool_core as LT
reload(LT)

def runMainUI():
    import LayoutTool_UI
    reload(LayoutTool_UI)
    LayoutTool_UI.initial()

def getScriptDescription(*args):
    reload(LT)
    scriptName = pm.textScrollList('allScriptTx', q = True, si = True)[0]
    pm.scrollField('descriptionTx', e = True, cl = True)
    pm.scrollField('descriptionTx', e = True, tx = LT.getScripDescription(scriptName))
    
def addCustomScript(*args):
    scriptName = pm.textScrollList('allScriptTx', q = True, si = True)
    for i in scriptName:
        pm.textScrollList('customScriptTx', e = True, append = i)
        pm.textScrollList('customScriptTx', e = True, da = True)
        pm.textScrollList('customScriptTx', e = True, si = i)
    
def removeTxLs(*args):
    selScript = pm.textScrollList('customScriptTx', q = True, si = True)
    for i in selScript:
        pm.textScrollList('customScriptTx', e = True, ri = i)
    
def moveUpTxLs(*args):
    selIndex = pm.textScrollList('customScriptTx', q = True, sii = True)
    allItem = pm.textScrollList('customScriptTx', q = True, ai = True)
    for i in selIndex:
        if i != 1:
            pm.textScrollList('customScriptTx', e = True, rii = i)
            pm.textScrollList('customScriptTx', e = True, ap = [i-1, allItem[i-1]])
            pm.textScrollList('customScriptTx', e = True, sii = i-1)
    
def moveDownTxLs(*args):
    count = pm.textScrollList('customScriptTx', q = True, ni = True)
    selIndex = pm.textScrollList('customScriptTx', q = True, sii = True)
    allItem = pm.textScrollList('customScriptTx', q = True, ai = True)
    selIndex.reverse()
    for i in selIndex:
        if i != count:
            pm.textScrollList('customScriptTx', e = True, rii = i)
            pm.textScrollList('customScriptTx', e = True, ap = [i+1, allItem[i-1]])
            pm.textScrollList('customScriptTx', e = True, sii = i+1)
    
def okBtn(*args):
    LT.savePref("customScriptBtn", pm.textScrollList('customScriptTx', q = True, ai = True))
    pm.deleteUI('setBtnWin')
    runMainUI()
    
def cancelBtn(*args):
    pm.deleteUI('setBtnWin')
    
def UI():
    scriptLs = LT.getScripts()
    btnLs = LT.getPref("customScriptBtn")
    scrollWidth = 200
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
                
                pm.textScrollList('allScriptTx', w = scrollWidth, append = scriptLs, ams = True, sc = getScriptDescription, dcc = addCustomScript)
                pm.text(l = '->')
                pm.textScrollList('customScriptTx', w = scrollWidth, append = btnLs, ams = True)
                
                pm.button(l = 'Add ->', c = addCustomScript)
                pm.separator(style = 'none')
                row1 = pm.rowLayout(nc = 3, adj = 3, cat = (2, 'right', 5))
                with row1:
                    pm.button(l = '^', w = 30, c = moveUpTxLs)
                    pm.button(l = 'v', w = 30, c = moveDownTxLs)
                    pm.button(l = 'Remove', c = removeTxLs)
                
                pm.text(l = 'Description', al = 'left')
                pm.separator(style = 'none')
                pm.separator(style = 'none')
                
                pm.scrollField('descriptionTx', w = scrollWidth, ed = False, ww = True, bgc = [0.22,0.22,0.22])
                pm.separator(style = 'none')
                col2 = pm.columnLayout(adj = True, rs = 5)
                with col2:
                    pm.separator(h = 150, style = 'none')
                    pm.button(l = 'OK', c = okBtn)
                    pm.button(l = 'Cancel', c = cancelBtn)
                    pm.separator(style = 'none')
            pm.separator(style = 'none', h = 5)
                    
UI()