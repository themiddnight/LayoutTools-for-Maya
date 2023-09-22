'''When the depth of field enabled, select the object you want to focus, the camera of the current shot will focus on it. 
Select on the ctrl is recommended.'''

import pymel.core as pm
from maya.cmds import xform
from math import pow, sqrt

def snapFocus():
    # get current cam
    currentShot = pm.sequenceManager(q = True, cs = True)
    currentCam = pm.shot(currentShot, q = True, cc = True)
    posCam = xform(currentCam, q = True, t = True, ws = True)
    
    # get cam shape
    currentCamShape = pm.listRelatives(currentCam, typ = 'shape')[0]
    
    # get obj location
    sel = pm.ls(sl = True)[0]
    posObj = xform(str(sel), q = True, t = True, ws = True)
    
    # read distance
    distance = sqrt(pow(posCam[0] - posObj[0], 2) + pow(posCam[1] - posObj[1], 2) + pow(posCam[2] - posObj[2], 2))
    
    # set focal point to cam
    pm.setAttr('%s.depthOfField' %currentCamShape, 1)
    pm.setAttr('%s.focusDistance' %currentCamShape, distance)
    
def run():
    snapFocus()