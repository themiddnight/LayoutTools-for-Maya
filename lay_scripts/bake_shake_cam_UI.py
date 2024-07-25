'''Bake camera auto shake into "fly_ctrl" or "camera_localAim_ctrl" animation.'''

import sys, os
path = os.environ['layout_tool_path'] + '/lay_modules/'
if path not in sys.path: sys.path.append(path)

import maya.cmds as mc
import bake_cam_shake_mod

def doBake(*args):
    targetOption = mc.radioButtonGrp('bakeTo', q = True, sl = True)
    cam = mc.ls(sl = True)
    camNamespace = cam[0].split(':')[0]
    startTime = mc.playbackOptions(q = True, ast = True)
    endTime = mc.playbackOptions(q = True, aet = True)
    bake_cam_shake_mod.bakeCamShake(camNamespace, startTime, endTime, targetOption)

def run():
    if mc.window('bakeShakeCamWin', exists = True):
        mc.deleteUI('bakeShakeCamWin')
    mc.window('bakeShakeCamWin', t = 'Bake Shaking Cameras', mxb = False)
    
    mc.columnLayout(adj = True, rs = 5, cat = ['both', 5])
    mc.text(l = 'Select any camera controller first...')
    mc.text(l = 'Bake shake to: ', al = 'left')
    mc.radioButtonGrp('bakeTo', la2 = ['allLocal (rotate)', 'camera_localAim (translate)'], nrb = 2, sl = 1)
    mc.button(l = 'Bake', c = doBake)
        
    mc.showWindow('bakeShakeCamWin')