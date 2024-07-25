'''Copy pose key to the same rigging character in the scene.
- Select ctrl of the original character and press "Copy"
- Select the same ctrl of another character and press "Paste"'''

import maya.cmds as mc

ctrlLs = []

def copyKeyframe(*args):
    global ctrlLs
    sel = mc.ls(sl = True)
    mc.setKeyframe(sel)
    time = mc.currentTime()
    mc.copyKey(sel, time = '%s:%s' %(time, time), hierarchy = 0, controlPoints = 0, shape = 0)
    
    for i in sel:
        a = i.split(':')[-1]
        ctrlLs.append(a)
        
def pasteKeyframe(*args):
    global ctrlLs
    selTar = mc.ls(sl = True)[0]
    tarNs = selTar.split(':')[0]
    mc.select(cl = True)
    for i in ctrlLs:
        mc.select('%s:%s' %(tarNs, i), add = True)
    selTar = mc.ls(sl = True)
    time = mc.currentTime()
    mc.pasteKey (selTar, time = '%s:%s' %(time, time+1), option = 'replace', copies = 1, connect = 0, timeOffset = 0, floatOffset = 0, valueOffset = 0)
    
def run():
    if mc.window('copyKeyWin', exists = True):
        mc.deleteUI('copyKeyWin')
    mc.window('copyKeyWin', t = 'Copy Key', mxb = False)
    mc.columnLayout(adj = True, rs = 5, cat = ['both', 5])
    mc.button(l = 'Copy Pose Key', c = copyKeyframe)
    mc.button(l = 'Paste Pose Key', c = pasteKeyframe)
    mc.showWindow('copyKeyWin')