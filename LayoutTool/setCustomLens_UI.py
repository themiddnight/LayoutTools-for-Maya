import pymel.core as pm
from LayoutTool import LayoutTool_core as LT
reload(LT)

def runMainUI():
    import LayoutTool_UI
    reload(LayoutTool_UI)
    LayoutTool_UI.initial()
    
def okBtn(*args):
    lensLs = []
    lensLs.append(pm.intField('int1', q = True, v = True))
    lensLs.append(pm.intField('int2', q = True, v = True))
    lensLs.append(pm.intField('int3', q = True, v = True))
    lensLs.append(pm.intField('int4', q = True, v = True))
    lensLs.append(pm.intField('int5', q = True, v = True))
    lensLs.append(pm.intField('int6', q = True, v = True))
    LT.savePref("lensList", lensLs)
    pm.deleteUI('setLensWin')
    runMainUI()
    
def cancelBtn(*args):
    pm.deleteUI('setLensWin')

def UI():
    lensLs = LT.getPref("lensList")
    
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
                pm.button(l = 'OK', w = 100, c = okBtn)
                pm.button(l = 'Cancel', w = 100, c = cancelBtn)
    
    pm.showWindow('setLensWin')
    
UI()