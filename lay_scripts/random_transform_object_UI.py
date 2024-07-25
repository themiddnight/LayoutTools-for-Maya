'''For randoming Translate, Rotate or Scale of the objects.'''

# import pymel.core as pm
import maya.cmds as mc
import random
    
def addObjLs(*args):
    mc.textScrollList('objTxLs', e = True, ra = True)
    mc.textScrollList('objTxLs', e = True, append = mc.ls(sl = True))

def selObjList(*args):
    mc.select(mc.textScrollList('objTxLs', q = True, si = True))
    
def createLoc(*args):
    if mc.ls('randLoc_A'):
        mc.delete(mc.ls('randLoc_A'))
    if mc.ls('randLoc_B'):
        mc.delete(mc.ls('randLoc_B'))
    tminLoc = mc.spaceLocator(n = 'randLoc_A')[0]
    mc.xform(tminLoc, t=[1,0,1])
    mc.setAttr("%s.overrideEnabled" %tminLoc, 1)
    mc.setAttr("%s.overrideColor" %tminLoc, 13)
    tmaxLoc = mc.spaceLocator(n = 'randLoc_B')[0]
    mc.xform(tmaxLoc, t=[-1,0,-1])
    mc.setAttr("%s.overrideEnabled" %tmaxLoc, 1)
    mc.setAttr("%s.overrideColor" %tmaxLoc, 6)

def doApply(*args):
    if mc.ls(sl = True):
        objListApply = mc.ls(sl = True)
    else:    
        objListApply = mc.ls(mc.textScrollList('objTxLs', q = True, ai = True))
    if mc.checkBox('Tcbox', q = True, v = True) == 1:
        if mc.radioButtonGrp('inputTypeRdo', q = True, sl = True) == 1:
            TXa = mc.getAttr('randLoc_A.translateX')
            TYa = mc.getAttr('randLoc_A.translateY')
            TZa = mc.getAttr('randLoc_A.translateZ')
            TXb = mc.getAttr('randLoc_B.translateX')
            TYb = mc.getAttr('randLoc_B.translateY')
            TZb = mc.getAttr('randLoc_B.translateZ')    
        elif mc.radioButtonGrp('inputTypeRdo', q = True, sl = True) == 2:
            TXa = mc.floatField('TXmin', q = True, v = True)
            TYa = mc.floatField('TYmin', q = True, v = True)
            TZa = mc.floatField('TZmin', q = True, v = True)
            TXb = mc.floatField('TXmax', q = True, v = True)
            TYb = mc.floatField('TYmax', q = True, v = True)
            TZb = mc.floatField('TZmax', q = True, v = True)    
        for i in objListApply:
            ranTX = random.uniform(TXa, TXb)
            ranTY = random.uniform(TYa, TYb)
            ranTZ = random.uniform(TZa, TZb)
            if mc.optionMenu('spaceModeCmb', q = True, v = True) == '2D Space':
                if mc.radioButtonGrp('axisRdo', q = True, sl = True) == 1:
                    avgTY = (TYa + TYb) / 2
                    mc.xform(i, t=[ranTX, avgTY, ranTZ])
                if mc.radioButtonGrp('axisRdo', q = True, sl = True) == 2:
                    avgTZ = (TZa + TZb) / 2
                    mc.xform(i, t=[ranTX, ranTY, avgTZ])
                if mc.radioButtonGrp('axisRdo', q = True, sl = True) == 3:
                    avgTX = (TXa + TXb) / 2
                    mc.xform(i, t=[avgTX, ranTY, ranTZ])
            if mc.optionMenu('spaceModeCmb', q = True, v = True) == '3D Space':
                mc.xform(i, t=[ranTX, ranTY, ranTZ])
    
    if mc.checkBox('Rcbox', q = True, v = True) == 1:
        RXa = mc.floatField('RXmin', q = True, v = True)
        RYa = mc.floatField('RYmin', q = True, v = True)
        RZa = mc.floatField('RZmin', q = True, v = True)
        RXb = mc.floatField('RXmax', q = True, v = True)
        RYb = mc.floatField('RYmax', q = True, v = True)
        RZb = mc.floatField('RZmax', q = True, v = True)    
        for m in objListApply:
            ranRX = random.uniform(RXa, RXb)
            ranRY = random.uniform(RYa, RYb)
            ranRZ = random.uniform(RZa, RZb)
            mc.xform(m, ro=[ranRX, ranRY, ranRZ])
    
    if mc.checkBox('Scbox', q = True, v = True) == 1:
        SXa = mc.floatField('SXmin', q = True, v = True)
        SYa = mc.floatField('SYmin', q = True, v = True)
        SZa = mc.floatField('SZmin', q = True, v = True)
        SXb = mc.floatField('SXmax', q = True, v = True)
        SYb = mc.floatField('SYmax', q = True, v = True)
        SZb = mc.floatField('SZmax', q = True, v = True)  
        if mc.checkBox('maintScbox', q = True, v = True) == 0:  
            for n in objListApply:
                ranSX = random.uniform(SXa, SXb)
                ranSY = random.uniform(SYa, SYb)
                ranSZ = random.uniform(SZa, SZb)
                mc.xform(n, s=[ranSX, ranSY, ranSZ])
        else:
            for n in objListApply:
                ranSX = random.uniform(SXa, SXb)
                mc.xform(n, s=[ranSX, ranSX, ranSX])

def run():
    if mc.window('randomObjWin', exists = True):
        mc.deleteUI('randomObjWin')
    mc.window('randomObjWin', t = 'Random Objects', mxb = False)
    
    def spaceSW(*args):
        if mc.optionMenu('spaceModeCmb', q = True, v = True) == '3D Space':
            mc.radioButtonGrp('axisRdo', e = True, en = False)
        else:
            mc.radioButtonGrp('axisRdo', e = True, en = True)
    def locatorSW(*args):
        if mc.radioButtonGrp('inputTypeRdo', q = True, sl = True) == 1:
            mc.rowColumnLayout('randTLay', e = True, en = False)
            mc.button('createLocBtn', e = True, en = True)
        else:
            mc.rowColumnLayout('randTLay', e = True, en = True)
            mc.button('createLocBtn', e = True, en = False)
    def enTranslate(*args):
        if mc.checkBox('Tcbox', q = True, v = True) == 1:
            Tlay = mc.columnLayout('Tlay', e = True, en = True)
        else:
            Tlay = mc.columnLayout('Tlay', e = True, en = False)
    def enRotate(*args):
        if mc.checkBox('Rcbox', q = True, v = True) == 1:
            Tlay = mc.columnLayout('Rlay', e = True, en = True)
        else:
            Tlay = mc.columnLayout('Rlay', e = True, en = False)
    def enScale(*args):
        if mc.checkBox('Scbox', q = True, v = True) == 1:
            Tlay = mc.columnLayout('Slay', e = True, en = True)
        else:
            Tlay = mc.columnLayout('Slay', e = True, en = False)
    def enMainScale(*args):
        if mc.checkBox('maintScbox', q = True, v = True) == 0:
            mc.text('syTX', e = True, en = True)
            mc.text('szTX', e = True, en = True)
            mc.floatField('SYmin', e = True, en = True)
            mc.floatField('SZmin', e = True, en = True)
            mc.floatField('SYmax', e = True, en = True)
            mc.floatField('SZmax', e = True, en = True)
        else:
            mc.text('syTX', e = True, en = False)
            mc.text('szTX', e = True, en = False)
            mc.floatField('SYmin', e = True, en = False)
            mc.floatField('SZmin', e = True, en = False)
            mc.floatField('SYmax', e = True, en = False)
            mc.floatField('SZmax', e = True, en = False)
        
    mainLay = mc.columnLayout(adj = True, rs = 5, cat = ['both',5])
    # with mainLay:
    mc.separator(style = 'none')
    listFrame = mc.frameLayout(l = 'Object List', cl = True, cll = True)
    # with listFrame:
    mc.textScrollList('objTxLs', w = 100, ams = True, sc = selObjList)
    mc.setParent('..')

    mc.button(l = 'Add to Random Object List', c = addObjLs)
    mc.separator(style = 'in')
    mc.checkBox('Tcbox', l = 'Translation', al = 'left', v = True, cc = enTranslate)
    Tlay = mc.columnLayout('Tlay', adj = True, rs = 5)
    # with Tlay:
    mc.optionMenu('spaceModeCmb', cc = spaceSW)
    mc.menuItem(l = '2D Space')
    mc.menuItem(l = '3D Space')
    mc.radioButtonGrp('axisRdo', la3 = ['XZ', 'XY', 'ZY'], nrb = 3, sl = 1, cw3 = [70,70,70], en = True)
    mc.radioButtonGrp('inputTypeRdo', la2 = ['Locator', 'Input Value'], nrb = 2, sl = 1, cc = locatorSW)
    randTLay = mc.rowColumnLayout('randTLay', nc = 4, en = False)
    # with randTLay:
    mc.text(l = ' ')
    mc.text(l = 'TX')
    mc.text(l = 'TY')
    mc.text(l = 'TZ')
    mc.text(l = 'Min: ', al = 'right')
    mc.floatField('TXmin')
    mc.floatField('TYmin')
    mc.floatField('TZmin')
    mc.text(l = 'Max: ', al = 'right')
    mc.floatField('TXmax')
    mc.floatField('TYmax')
    mc.floatField('TZmax')
    mc.setParent('..')
    mc.button('createLocBtn', l = 'Create Locator', en = True, c = createLoc)
    mc.setParent('..')

    mc.separator(style = 'in')
    mc.checkBox('Rcbox', l = 'Rotation', al = 'left', v = 1, cc = enRotate)
    Rlay = mc.columnLayout('Rlay', adj = True, rs = 5, en = True)
    # with Rlay:
    randRLay = mc.rowColumnLayout(nc = 4)
    # with randRLay:
    mc.text(l = ' ')
    mc.text(l = 'RX')
    mc.text(l = 'RY')
    mc.text(l = 'RZ')
    mc.text(l = 'Min: ', al = 'right')
    mc.floatField('RXmin')
    mc.floatField('RYmin')
    mc.floatField('RZmin')
    mc.text(l = 'Max: ', al = 'right')
    mc.floatField('RXmax')
    mc.floatField('RYmax', v = 360)
    mc.floatField('RZmax')
    mc.setParent('..')
    mc.setParent('..')

    mc.separator(style = 'in')
    mc.checkBox('Scbox', l = 'Scale', al = 'left', v = 0, cc = enScale)
    Slay = mc.columnLayout('Slay', adj = True, rs = 5, en = False)
    # with Slay:
    randSLay = mc.rowColumnLayout(nc = 4)
    # with randSLay:
    mc.text(l = ' ')
    mc.text('sxTX', l = 'SX')
    mc.text('syTX', l = 'SY', en = False)
    mc.text('szTX', l = 'SZ', en = False)
    mc.text(l = 'Min: ', al = 'right')
    mc.floatField('SXmin', v = 1)
    mc.floatField('SYmin', v = 1, en = False)
    mc.floatField('SZmin', v = 1, en = False)
    mc.text(l = 'Max: ', al = 'right')
    mc.floatField('SXmax', v = 2)
    mc.floatField('SYmax', v = 2, en = False)
    mc.floatField('SZmax', v = 2, en = False)
    mc.setParent('..')

    mc.rowLayout(nc = 2, cw = [1,26])
    mc.text(l = ' ')
    mc.checkBox('maintScbox', l = 'Maintain Ratio', al = 'left', v = 1, cc = enMainScale)
    mc.setParent('..')
    mc.setParent('..')
    
    mc.separator(style = 'in')
    mc.button(l = 'Apply', c = doApply)
    mc.separator(style = 'none')
        
    mc.showWindow('randomObjWin')