from pymel.core import *

def doFlip(*args):
    rgtIndx = textField('rgtIndxTx', q = True, tx = True)
    lftIndx = textField('lftIndxTx', q = True, tx = True)
    fkIndx = textField('fkIndxTx', q = True, tx = True)
    ikIndx = textField('ikIndxTx', q = True, tx = True)
    
    sel = ls(sl = True)
    for i in sel:
        if i.find(rgtIndx) != -1:
            for j in sel:
                if j.find(lftIndx) != -1:
                    RctrlNIndx = i.find(rgtIndx)
                    LctrlNIndx = j.find(lftIndx)
                    if i[0:RctrlNIndx] == j[0:LctrlNIndx]:
                        rotR = xform(i, q = True, ro = True, ws = False)
                        rotL = xform(j, q = True, ro = True, ws = False)
                        posR = xform(i, q = True, t = True, ws = False)
                        posL = xform(j, q = True, t = True, ws = False)
                        if i.find(ikIndx) !=1 and i.find(ikIndx) != -1:
                            posR[0] *= -1
                            posL[0] *= -1
                        xform(i, ro = rotL, ws = False)
                        xform(j, ro = rotR, ws = False)
                        xform(i, t = posL, ws = False)
                        xform(j, t = posR, ws = False)
                  
        elif i.find(lftIndx) == -1 and i.find(rgtIndx) == -1:
            print i
            Rot = xform(i, q = True, ro = True, ws = False)
            Pos = xform(i, q = True, t = True, ws = False)
            Rot[1] *= -1
            Rot[2] *= -1
            Pos[0] *= -1
            xform(i, ro = Rot, ws = False)
            xform(i, t = Pos, ws = False)
            
def flipPoseUI():
    if window('flipPoseWin', exists = True):
        deleteUI('flipPoseWin')
    window('flipPoseWin', t = 'Mirror Pose', mxb = False)
    
    mainLay = columnLayout(adj = True, rs = 5, cat = ['both', 5])
    with mainLay:
        col01 = rowColumnLayout(nc = 2)
        with col01:
            text(l = 'Left side index: ')
            textField('lftIndxTx', tx = 'LFT')
            text(l = 'Right side index: ')
            textField('rgtIndxTx', tx = 'RGT')
            text(l = 'FK index: ')
            textField('fkIndxTx', tx = 'fk')
            text(l = 'IK index: ')
            textField('ikIndxTx', tx = 'ik')
        button(l = 'Flip Pose', c = doFlip)
        
    showWindow('flipPoseWin')
    
def run():
    flipPoseUI()
