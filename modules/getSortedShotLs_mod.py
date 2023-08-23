import pymel.core as pm

def getShotLs():
    shotNameLs = []
    shots = pm.ls(type = 'shot')
    for shot in shots:
        shotNameLs.append(pm.shot(shot, q = True, sn = True))
        
    shotNameSorted = sorted(shotNameLs)
    
    shotSortedLs = []
    for shotName in shotNameSorted:
        for shot in shots:
            shotNameR = pm.shot(shot, q = True, sn = True)
            if shotName == shotNameR:
                shotSortedLs.append(shot)
                
    return shotSortedLs