'''For randoming Translate, Rotate or Scale of the objects.'''

import pymel.core as pm
import random

def randomObjUI():
    if pm.window('randomObjWin', exists = True):
        pm.deleteUI('randomObjWin')
    pm.window('randomObjWin', t = 'Random Objects', mxb = False)
    
    def spaceSW(*args):
        if pm.optionMenu('spaceModeCmb', q = True, v = True) == '3D Space':
            pm.radioButtonGrp('axisRdo', e = True, en = False)
        else:
            pm.radioButtonGrp('axisRdo', e = True, en = True)
    def locatorSW(*args):
        if pm.radioButtonGrp('inputTypeRdo', q = True, sl = True) == 1:
            pm.rowColumnLayout('randTLay', e = True, en = False)
            pm.button('createLocBtn', e = True, en = True)
        else:
            pm.rowColumnLayout('randTLay', e = True, en = True)
            pm.button('createLocBtn', e = True, en = False)
    def enTranslate(*args):
        if pm.checkBox('Tcbox', q = True, v = True) == 1:
            Tlay = pm.columnLayout('Tlay', e = True, en = True)
        else:
            Tlay = pm.columnLayout('Tlay', e = True, en = False)
    def enRotate(*args):
        if pm.checkBox('Rcbox', q = True, v = True) == 1:
            Tlay = pm.columnLayout('Rlay', e = True, en = True)
        else:
            Tlay = pm.columnLayout('Rlay', e = True, en = False)
    def enScale(*args):
        if pm.checkBox('Scbox', q = True, v = True) == 1:
            Tlay = pm.columnLayout('Slay', e = True, en = True)
        else:
            Tlay = pm.columnLayout('Slay', e = True, en = False)
    def enMainScale(*args):
        if pm.checkBox('maintScbox', q = True, v = True) == 0:
            pm.text('syTX', e = True, en = True)
            pm.text('szTX', e = True, en = True)
            pm.floatField('SYmin', e = True, en = True)
            pm.floatField('SZmin', e = True, en = True)
            pm.floatField('SYmax', e = True, en = True)
            pm.floatField('SZmax', e = True, en = True)
        else:
            pm.text('syTX', e = True, en = False)
            pm.text('szTX', e = True, en = False)
            pm.floatField('SYmin', e = True, en = False)
            pm.floatField('SZmin', e = True, en = False)
            pm.floatField('SYmax', e = True, en = False)
            pm.floatField('SZmax', e = True, en = False)
        
    mainLay = pm.columnLayout(adj = True, rs = 5, cat = ['both',5])
    with mainLay:
        pm.separator(style = 'none')
        listFrame = pm.frameLayout(l = 'Object List', cl = True, cll = True)
        with listFrame:
            pm.textScrollList('objTxLs', w = 100, ams = True, sc = selObjList)
        pm.button(l = 'Add to Random Object List', c = addObjLs)
        pm.separator(style = 'in')
        pm.checkBox('Tcbox', l = 'Translation', al = 'left', v = True, cc = enTranslate)
        Tlay = pm.columnLayout('Tlay', adj = True, rs = 5)
        with Tlay:
            pm.optionMenu('spaceModeCmb', cc = spaceSW)
            pm.menuItem(l = '2D Space')
            pm.menuItem(l = '3D Space')
            pm.radioButtonGrp('axisRdo', la3 = ['XZ', 'XY', 'ZY'], nrb = 3, sl = 1, cw3 = [70,70,70], en = True)
            pm.radioButtonGrp('inputTypeRdo', la2 = ['Locator', 'Input Value'], nrb = 2, sl = 1, cc = locatorSW)
            randTLay = pm.rowColumnLayout('randTLay', nc = 4, en = False)
            with randTLay:
                pm.text(l = ' ')
                pm.text(l = 'TX')
                pm.text(l = 'TY')
                pm.text(l = 'TZ')
                pm.text(l = 'Min: ', al = 'right')
                pm.floatField('TXmin')
                pm.floatField('TYmin')
                pm.floatField('TZmin')
                pm.text(l = 'Max: ', al = 'right')
                pm.floatField('TXmax')
                pm.floatField('TYmax')
                pm.floatField('TZmax')
            pm.button('createLocBtn', l = 'Create Locator', en = True, c = createLoc)
        pm.separator(style = 'in')
        pm.checkBox('Rcbox', l = 'Rotation', al = 'left', v = 1, cc = enRotate)
        Rlay = pm.columnLayout('Rlay', adj = True, rs = 5, en = True)
        with Rlay:
            randRLay = pm.rowColumnLayout(nc = 4)
            with randRLay:
                pm.text(l = ' ')
                pm.text(l = 'RX')
                pm.text(l = 'RY')
                pm.text(l = 'RZ')
                pm.text(l = 'Min: ', al = 'right')
                pm.floatField('RXmin')
                pm.floatField('RYmin')
                pm.floatField('RZmin')
                pm.text(l = 'Max: ', al = 'right')
                pm.floatField('RXmax')
                pm.floatField('RYmax', v = 360)
                pm.floatField('RZmax')
        pm.separator(style = 'in')
        pm.checkBox('Scbox', l = 'Scale', al = 'left', v = 0, cc = enScale)
        Slay = pm.columnLayout('Slay', adj = True, rs = 5, en = False)
        with Slay:
            randSLay = pm.rowColumnLayout(nc = 4)
            with randSLay:
                pm.text(l = ' ')
                pm.text('sxTX', l = 'SX')
                pm.text('syTX', l = 'SY', en = False)
                pm.text('szTX', l = 'SZ', en = False)
                pm.text(l = 'Min: ', al = 'right')
                pm.floatField('SXmin', v = 1)
                pm.floatField('SYmin', v = 1, en = False)
                pm.floatField('SZmin', v = 1, en = False)
                pm.text(l = 'Max: ', al = 'right')
                pm.floatField('SXmax', v = 2)
                pm.floatField('SYmax', v = 2, en = False)
                pm.floatField('SZmax', v = 2, en = False)
            randSrow1 = pm.rowLayout(nc = 2, cw = [1,26])
            with randSrow1:
                pm.text(l = ' ')
                pm.checkBox('maintScbox', l = 'Maintain Ratio', al = 'left', v = 1, cc = enMainScale)
        pm.separator(style = 'in')
        pm.button(l = 'Apply', c = doApply)
        pm.separator(style = 'none')
        
    pm.showWindow('randomObjWin')
    
def addObjLs(*args):
    pm.textScrollList('objTxLs', e = True, ra = True)
    pm.textScrollList('objTxLs', e = True, append = pm.ls(sl = True))

def selObjList(*args):
    pm.select(pm.textScrollList('objTxLs', q = True, si = True))
    
def createLoc(*args):
    if pm.ls('randLoc_A'):
        pm.delete(pm.ls('randLoc_A'))
    if pm.ls('randLoc_B'):
        pm.delete(pm.ls('randLoc_B'))
    tminLoc = pm.spaceLocator(n = 'randLoc_A')
    tminLoc.setTranslation([1,0,1])
    tminLoc.setAttr('overrideEnabled', 1)
    tminLoc.setAttr('overrideColor', 13)
    tmaxLoc = pm.spaceLocator(n = 'randLoc_B')
    tmaxLoc.setTranslation([-1,0,-1])
    tmaxLoc.setAttr('overrideEnabled', 1)
    tmaxLoc.setAttr('overrideColor', 6)

def doApply(*args):
    if pm.ls(sl = True):
        objListApply = pm.ls(sl = True)
    else:    
        objListApply = pm.ls(pm.textScrollList('objTxLs', q = True, ai = True))
    if pm.checkBox('Tcbox', q = True, v = True) == 1:
        if pm.radioButtonGrp('inputTypeRdo', q = True, sl = True) == 1:
            TXa = pm.getAttr('randLoc_A.translateX')
            TYa = pm.getAttr('randLoc_A.translateY')
            TZa = pm.getAttr('randLoc_A.translateZ')
            TXb = pm.getAttr('randLoc_B.translateX')
            TYb = pm.getAttr('randLoc_B.translateY')
            TZb = pm.getAttr('randLoc_B.translateZ')    
        elif pm.radioButtonGrp('inputTypeRdo', q = True, sl = True) == 2:
            TXa = pm.floatField('TXmin', q = True, v = True)
            TYa = pm.floatField('TYmin', q = True, v = True)
            TZa = pm.floatField('TZmin', q = True, v = True)
            TXb = pm.floatField('TXmax', q = True, v = True)
            TYb = pm.floatField('TYmax', q = True, v = True)
            TZb = pm.floatField('TZmax', q = True, v = True)    
        for l in objListApply:
            ranTX = random.uniform(TXa, TXb)
            ranTY = random.uniform(TYa, TYb)
            ranTZ = random.uniform(TZa, TZb)
            if pm.optionMenu('spaceModeCmb', q = True, v = True) == '2D Space':
                if pm.radioButtonGrp('axisRdo', q = True, sl = True) == 1:
                    avgTY = (TYa + TYb) / 2
                    l.setTranslation([ranTX, avgTY, ranTZ])
                if pm.radioButtonGrp('axisRdo', q = True, sl = True) == 2:
                    avgTZ = (TZa + TZb) / 2
                    l.setTranslation([ranTX, ranTY, avgTZ])
                if pm.radioButtonGrp('axisRdo', q = True, sl = True) == 3:
                    avgTX = (TXa + TXb) / 2
                    l.setTranslation([avgTX, ranTY, ranTZ])
            if pm.optionMenu('spaceModeCmb', q = True, v = True) == '3D Space':
                l.setTranslation([ranTX, ranTY, ranTZ])
    
    if pm.checkBox('Rcbox', q = True, v = True) == 1:
        RXa = pm.floatField('RXmin', q = True, v = True)
        RYa = pm.floatField('RYmin', q = True, v = True)
        RZa = pm.floatField('RZmin', q = True, v = True)
        RXb = pm.floatField('RXmax', q = True, v = True)
        RYb = pm.floatField('RYmax', q = True, v = True)
        RZb = pm.floatField('RZmax', q = True, v = True)    
        for m in objListApply:
            ranRX = random.uniform(RXa, RXb)
            ranRY = random.uniform(RYa, RYb)
            ranRZ = random.uniform(RZa, RZb)
            m.setRotation([ranRX, ranRY, ranRZ])
    
    if pm.checkBox('Scbox', q = True, v = True) == 1:
        SXa = pm.floatField('SXmin', q = True, v = True)
        SYa = pm.floatField('SYmin', q = True, v = True)
        SZa = pm.floatField('SZmin', q = True, v = True)
        SXb = pm.floatField('SXmax', q = True, v = True)
        SYb = pm.floatField('SYmax', q = True, v = True)
        SZb = pm.floatField('SZmax', q = True, v = True)  
        if pm.checkBox('maintScbox', q = True, v = True) == 0:  
            for n in objListApply:
                ranSX = random.uniform(SXa, SXb)
                ranSY = random.uniform(SYa, SYb)
                ranSZ = random.uniform(SZa, SZb)
                n.setScale([ranSX, ranSY, ranSZ])
        else:
            for n in objListApply:
                ranSX = random.uniform(SXa, SXb)
                n.setScale([ranSX, ranSX, ranSX])
            
def run():
    randomObjUI()
