import maya.cmds as mc

def getShotLs():
    shotNameLs = []
    shots = mc.ls(type = 'shot')
    for shot in shots:
        shotNameLs.append(mc.shot(shot, q = True, sn = True))
        
    shotNameSorted = sorted(shotNameLs)
    
    shotSortedLs = []
    for shotName in shotNameSorted:
        for shot in shots:
            shotNameR = mc.shot(shot, q = True, sn = True)
            if shotName == shotNameR:
                shotSortedLs.append(shot)
                
    return shotSortedLs