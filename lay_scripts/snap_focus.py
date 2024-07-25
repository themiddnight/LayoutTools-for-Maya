'''When the depth of field enabled, select the object you want to focus, the camera of the current shot will focus on it. 
Select on the ctrl is recommended.'''

import maya.cmds as mc
from math import pow, sqrt

def run():
    # get current cam
    currentShot = mc.sequenceManager(q = True, cs = True)
    currentCam = mc.shot(currentShot, q = True, cc = True)
    posCam = mc.xform(currentCam, q = True, t = True, ws = True)
    
    # get cam shape
    currentCamShape = mc.listRelatives(currentCam, typ = 'shape')[0]
    
    # get obj location
    sel = mc.ls(sl = True)[0]
    posObj = mc.xform(str(sel), q = True, t = True, ws = True)
    
    # read distance
    distance = sqrt(pow(posCam[0] - posObj[0], 2) + pow(posCam[1] - posObj[1], 2) + pow(posCam[2] - posObj[2], 2))
    
    # set focal point to cam
    mc.setAttr('%s.depthOfField' %currentCamShape, 1)
    mc.setAttr('%s.focusDistance' %currentCamShape, distance)