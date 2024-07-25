'''Display the frame number of the current shot.'''

import maya.cmds as mc

def run():
    def countShotFrame(*args):
        currentShot = mc.sequenceManager(q = True, cs = True)
        shotFrameStart = mc.shot(currentShot, q = True, sst = True)
        shotFrameEnd = mc.shot(currentShot, q = True, set = True)
        duration = shotFrameEnd - shotFrameStart + 1
        currentFrame = mc.currentTime(q=True)
        frameStart = currentFrame - (shotFrameStart - 1)
        return str(int(frameStart)) + '/' + str(int(duration))
    
    if mc.headsUpDisplay( 'HUDFrameCount', exists = True ):
        mc.headsUpDisplay( 'HUDFrameCount', rem = True )
    else:
        mc.headsUpDisplay( 'HUDFrameCount', 
                            section = 5, 
                            block = 1, 
                            blockSize = 'medium', 
                            label = 'SG Shot Frame:', 
                            labelFontSize = 'large', 
                            command = countShotFrame, 
                            event = 'timeChanged' 
                          )
