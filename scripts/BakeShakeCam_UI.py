'''Bake camera auto shake into "fly_ctrl" or "camera_localAim_ctrl" animation.'''

import pymel.core as pm
import sys 
from modules import bakeCamShake_mod
reload(bakeCamShake_mod)

def doBake(*args):
    targetOption = pm.radioButtonGrp('bakeTo', q = True, sl = True)
    cam = pm.ls(sl = True)
    camNamespace = cam[0].split(':')[0]
    startTime = pm.playbackOptions(q = True, ast = True)
    endTime = pm.playbackOptions(q = True, aet = True)
    bakeCamShake_mod.bakeCamShake(camNamespace, startTime, endTime, targetOption)

def bakeShakeCamUI():
    if pm.window('bakeShakeCamWin', exists = True):
        pm.deleteUI('bakeShakeCamWin')
    pm.window('bakeShakeCamWin', t = 'Bake Shaking Cameras', mxb = False)
    
    mainLay = pm.columnLayout(adj = True, rs = 5, cat = ['both', 5])
    with mainLay:
        pm.text(l = 'Select any camera controller first...')
        pm.text(l = 'Bake shake to: ', al = 'left')
        pm.radioButtonGrp('bakeTo', la2 = ['allLocal (rotate)', 'camera_localAim (translate)'], nrb = 2, sl = 1)
        pm.button(l = 'Bake', c = doBake)
        
    pm.showWindow('bakeShakeCamWin')
    
def run():    
    bakeShakeCamUI()