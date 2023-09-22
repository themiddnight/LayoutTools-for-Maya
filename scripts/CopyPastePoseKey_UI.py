'''Copy pose key to the same rigging character in the scene.
- Select ctrl of the original character and press "Copy"
- Select the same ctrl of another character and press "Paste"'''

import pymel.core as pm

ctrlLs = []

def copyKeyframe(*args):
    global ctrlLs
    sel = pm.ls(sl = True)
    pm.setKeyframe(sel)
    time = pm.currentTime()
    pm.copyKey(sel, time = '%s:%s' %(time, time), hierarchy = 0, controlPoints = 0, shape = 0)
    
    for i in sel:
        a = i.split(':')[-1]
        ctrlLs.append(a)
        
def pasteKeyframe(*args):
    global ctrlLs
    selTar = pm.ls(sl = True)[0]
    tarNs = selTar.split(':')[0]
    pm.select(cl = True)
    for i in ctrlLs:
        pm.select('%s:%s' %(tarNs, i), add = True)
    selTar = pm.ls(sl = True)
    time = pm.currentTime()
    pm.pasteKey (selTar, time = '%s:%s' %(time, time+1), option = 'replace', copies = 1, connect = 0, timeOffset = 0, floatOffset = 0, valueOffset = 0)
    
def copyKeyUI():
    if pm.window('copyKeyWin', exists = True):
        pm.deleteUI('copyKeyWin')
    pm.window('copyKeyWin', t = 'Copy Key', mxb = False)
    pm.columnLayout(adj = True, rs = 5, cat = ['both', 5])
    pm.button(l = 'Copy Pose Key', c = copyKeyframe)
    pm.button(l = 'Paste Pose Key', c = pasteKeyframe)
    pm.showWindow('copyKeyWin')
    
def run():
    copyKeyUI()