'''For randoming vertice position of the object. Can do it entirely object or on the selected vertice.'''

import pymel.core as pm
import random

def doRand(*args):
    rand = pm.floatField('vtxRandFloat', q = True, v = True)
    randPos = rand
    randNeg = -rand
    sel = pm.ls(selection=True)[0]
    if sel:
        if pm.objectType(sel) == 'mesh': # Vertices are selected
            doRandVtx(randPos, randNeg)
        else: # Objects are selected
            doRandObj(randPos, randNeg)
    else:
        print("No object or vertices selected.")

def doRandVtx(randPos, randNeg):
    selection = pm.ls(selection=True, flatten=True)
    for vertex in selection:
        pm.move(random.uniform(randNeg, randPos), random.uniform(randNeg, randPos), random.uniform(randNeg, randPos), vertex, relative=True)
    
def doRandObj(randPos, randNeg):
    selected_obj = pm.ls(selection = True)[0]
    vertices = pm.ls(selected_obj + '.vtx[*]', flatten = True)
    
    for vert in vertices:
        current_pos = pm.pointPosition(vert, world=True)
        offset = (random.uniform(randNeg, randPos), random.uniform(randNeg, randPos), random.uniform(randNeg, randPos))
        new_pos = [current_pos[i] + offset[i] for i in range(3)]
        pm.xform(vert, worldSpace = True, translation = new_pos)

def run():
    if pm.window('randVtxWin', exists = True):
        pm.deleteUI('randVtxWin')
    pm.window('randVtxWin', t = 'Random Vertice Position', mxb = False, w = 100)
    pm.columnLayout(adj = True, rs = 5, cat = ['both', 5])
    
    pm.text(l = 'Input random vertice position value:', al = 'left')
    pm.floatField('vtxRandFloat', v = 1)
    pm.button(l = 'Random', c = doRand)
    
    pm.showWindow('randVtxWin')
    
run()