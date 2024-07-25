'''For randoming vertice position of the object. Can do it entirely object or on the selected vertice.'''

import maya.cmds as mc
import random

def doRand(*args):
    rand = mc.floatField('vtxRandFloat', q = True, v = True)
    randPos = rand
    randNeg = -rand
    sel = mc.ls(selection=True)[0]
    if sel:
        if mc.objectType(sel) == 'mesh': # Vertices are selected
            doRandVtx(randPos, randNeg)
        else: # Objects are selected
            doRandObj(randPos, randNeg)
    else:
        print("No object or vertices selected.")

def doRandVtx(randPos, randNeg):
    selection = mc.ls(selection=True, flatten=True)
    for vertex in selection:
        mc.move(random.uniform(randNeg, randPos), random.uniform(randNeg, randPos), random.uniform(randNeg, randPos), vertex, relative=True)
    
def doRandObj(randPos, randNeg):
    selected_obj = mc.ls(selection = True)[0]
    vertices = mc.ls(selected_obj + '.vtx[*]', flatten = True)
    
    for vert in vertices:
        current_pos = mc.pointPosition(vert, world=True)
        offset = (random.uniform(randNeg, randPos), random.uniform(randNeg, randPos), random.uniform(randNeg, randPos))
        new_pos = [current_pos[i] + offset[i] for i in range(3)]
        mc.xform(vert, worldSpace = True, translation = new_pos)

def run():
    if mc.window('randVtxWin', exists = True):
        mc.deleteUI('randVtxWin')
    mc.window('randVtxWin', t = 'Random Vertice Position', mxb = False, w = 100)
    mc.columnLayout(adj = True, rs = 5, cat = ['both', 5])
    
    mc.text(l = 'Input random vertice position value:', al = 'left')
    mc.floatField('vtxRandFloat', v = 1)
    mc.button(l = 'Random', c = doRand)
    
    mc.showWindow('randVtxWin')