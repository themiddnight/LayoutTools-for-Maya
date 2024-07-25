'''To flip the pose horizontally. Select all ctrl of the character and flip it.

- Set the index name by the ctrl naming.'''

import maya.cmds as mc

def doFlip(*args):
    rgtIndx = mc.textField('rgtIndxTx', q = True, tx = True)
    lftIndx = mc.textField('lftIndxTx', q = True, tx = True)
    fkIndx = mc.textField('fkIndxTx', q = True, tx = True)
    ikIndx = mc.textField('ikIndxTx', q = True, tx = True)
    
    sel = mc.ls(sl = True)
    for i in sel:
        if i.find(rgtIndx) != -1:
            for j in sel:
                if j.find(lftIndx) != -1:
                    RctrlNIndx = i.find(rgtIndx)
                    LctrlNIndx = j.find(lftIndx)
                    if i[0:RctrlNIndx] == j[0:LctrlNIndx]:
                        rotR = mc.xform(i, q = True, ro = True, ws = False)
                        rotL = mc.xform(j, q = True, ro = True, ws = False)
                        posR = mc.xform(i, q = True, t = True, ws = False)
                        posL = mc.xform(j, q = True, t = True, ws = False)
                        if i.find(ikIndx) !=1 and i.find(ikIndx) != -1:
                            posR[0] *= -1
                            posL[0] *= -1
                        mc.xform(i, ro = rotL, ws = False)
                        mc.xform(j, ro = rotR, ws = False)
                        mc.xform(i, t = posL, ws = False)
                        mc.xform(j, t = posR, ws = False)
                  
        elif i.find(lftIndx) == -1 and i.find(rgtIndx) == -1:
            print(i)
            Rot = mc.xform(i, q = True, ro = True, ws = False)
            Pos = mc.xform(i, q = True, t = True, ws = False)
            Rot[1] *= -1
            Rot[2] *= -1
            Pos[0] *= -1
            mc.xform(i, ro = Rot, ws = False)
            mc.xform(i, t = Pos, ws = False)
            
def run():
    if mc.window('flipPoseWin', exists = True):
        mc.deleteUI('flipPoseWin')
    mc.window('flipPoseWin', t = 'Mirror Pose', mxb = False)
    
    mc.columnLayout(adj = True, rs = 5, cat = ['both', 5])
    mc.rowColumnLayout(nc = 2)
    mc.text(l = 'Left side index: ')
    mc.textField('lftIndxTx', tx = 'LFT')
    mc.text(l = 'Right side index: ')
    mc.textField('rgtIndxTx', tx = 'RGT')
    mc.text(l = 'FK index: ')
    mc.textField('fkIndxTx', tx = 'fk')
    mc.text(l = 'IK index: ')
    mc.textField('ikIndxTx', tx = 'ik')
    mc.setParent('..')

    mc.button(l = 'Flip Pose', c = doFlip)
        
    mc.showWindow('flipPoseWin')