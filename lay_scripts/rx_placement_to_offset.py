'''Set the Rotate X of the selected ctrl to the inner to maintain the Rotate Y axis of the inner.'''

import maya.cmds as mc

def run():
    camSel = mc.ls(sl = True)
    for i in camSel:
        camNs = i.split(':')[0]
        if i.split(':')[-1] == 'offset_ctrl':
            rx = mc.getAttr('%s:offset_ctrl.rotateX' %camNs)
            mc.setAttr('%s:fly_ctrl.rotateX' %camNs, rx)
            mc.setAttr('%s:offset_ctrl.rotateX' %camNs, 0)
        else:
            rx = mc.getAttr('%s:placement_ctrl.rotateX' %camNs)
            mc.setAttr('%s:offset_ctrl.rotateX' %camNs, rx)
            mc.setAttr('%s:placement_ctrl.rotateX' %camNs, 0)