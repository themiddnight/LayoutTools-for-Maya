'''Set the Rotate X of the selected ctrl to the inner to maintain the Rotate Y axis of the inner.'''

import pymel.core as pm

def run():
    camSel = pm.ls(sl = True)
    for i in camSel:
        camNs = i.split(':')[0]
        if i.split(':')[-1] == 'offset_ctrl':
            rx = pm.getAttr('%s:offset_ctrl.rotateX' %camNs)
            pm.setAttr('%s:fly_ctrl.rotateX' %camNs, rx)
            pm.setAttr('%s:offset_ctrl.rotateX' %camNs, 0)
        else:
            rx = pm.getAttr('%s:placement_ctrl.rotateX' %camNs)
            pm.setAttr('%s:offset_ctrl.rotateX' %camNs, rx)
            pm.setAttr('%s:placement_ctrl.rotateX' %camNs, 0)