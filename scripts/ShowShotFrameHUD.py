'''Display the frame number of the current shot.'''

import pymel.core as pm

def run():
    def countShotFrame(*args):
        currentShot = pm.sequenceManager(q = True, cs = True)
        shotFrameStart = pm.shot(currentShot, q = True, sst = True)
        shotFrameEnd = pm.shot(currentShot, q = True, set = True)
        duration = shotFrameEnd - shotFrameStart + 1
        currentFrame = pm.currentTime()
        frameStart = currentFrame - (shotFrameStart - 1)
        return str(int(frameStart)) + '/' + str(int(duration))
    
    if pm.headsUpDisplay( 'HUDFrameCount', exists = True ):
        pm.headsUpDisplay( 'HUDFrameCount', rem = True )
    else:
        pm.headsUpDisplay( 'HUDFrameCount', 
                            section = 5, 
                            block = 1, 
                            blockSize = 'medium', 
                            label = 'SG Shot Frame:', 
                            labelFontSize = 'large', 
                            command = countShotFrame, 
                            event = 'timeChanged' 
                          )
