'''The tool for creating shots with cameras assigned and naming.'''

# from pymel.core import *
# from maya.cmds import file
import maya.cmds as mc

def getData(*args):
    filePath = mc.textField('camPathTxt', q = True, tx = True)
    prefix = mc.textField('prefixTxt', q = True, tx = True)
    startNumInt = mc.intField('startNumInt', q = True, v = True)
    countNumInt = mc.intField('countInt', q = True, v = True)
    
    numPad = mc.optionMenu('padCmb', q = True, v = True)
    numDigit = mc.optionMenu('digitCmb', q = True, v = True)
    
    return filePath, prefix, startNumInt, countNumInt, numPad, numDigit
        
    
def camName(*args):
    _, prefix, startNumInt, countNumInt, numPad, numDigit = getData()
    endNumInt = (startNumInt - 1) + countNumInt
    
    if numPad == '3':
        if numDigit == '1':
            startNum = '%s%03d' %(prefix, startNumInt)
            endNum = '%s%03d' %(prefix, endNumInt)
        elif numDigit == '10':
            startNum = '%s%02d0' %(prefix, startNumInt)
            endNum = '%s%02d0' %(prefix, endNumInt)
    elif numPad == '4':
        if numDigit == '1':
            startNum = '%s%04d' %(prefix, startNumInt)
            endNum = '%s%04d' %(prefix, endNumInt)
        elif numDigit == '10':
            startNum = '%s%03d0' %(prefix, startNumInt)
            endNum = '%s%03d0' %(prefix, endNumInt)
            
    return startNum, endNum
    
def doImport(*args):
    filePath, prefix, startNumInt, countNumInt, numPad, numDigit = getData()
    
    for i in range(countNumInt):
        num = i + startNumInt
        if numPad == '3':
            if numDigit == '1':
                camNameStr = '%s%03d' %(prefix, num)
            elif numDigit == '10':
                camNameStr = '%s%02d0' %(prefix, num)
        elif numPad == '4':
            if numDigit == '1':
                camNameStr = '%s%04d' %(prefix, num)
            elif numDigit == '10':
                camNameStr = '%s%03d0' %(prefix, num)
                
        mc.file(filePath, r = True, ns = camNameStr)

def run():
    if mc.window('createCamWin', exists = True):
        mc.deleteUI('createCamWin')
    mc.window('createCamWin', t = 'Create Cameras', mxb = False)
    
    def displayCamName(*args):
        startNum, endNum = camName()
        mc.text('camNameDis', e = True, l = '%s - %s' %(startNum, endNum))
    
    mc.columnLayout(adj = True, rs = 5, cat = ['both', 5])
    mc.rowColumnLayout(nc = 2, cw = [2,200], cal = [1,'right'], cs = [1,5], rs = [1,5])
    
    mc.text(l = 'Camera file path: ')
    mc.textField('camPathTxt')
    mc.text(l = 'Start num: ')
    mc.intField('startNumInt', v = 1, cc = displayCamName)
    mc.text(l = 'Count: ')
    mc.intField('countInt', v = 10, cc = displayCamName)
    mc.text(l = 'Name prefix: ')
    mc.textField('prefixTxt', tx = 'cam_', cc = displayCamName)
    mc.text(l = 'Pad: ')
    mc.optionMenu('padCmb', cc = displayCamName)
    mc.menuItem(l = '3')
    mc.menuItem(l = '4')
    mc.text(l = 'Digit: ')
    mc.optionMenu('digitCmb', cc = displayCamName)
    mc.menuItem(l = '1')
    mc.menuItem(l = '10')
    mc.setParent('..')

    mc.text('camNameDis', l = 'test')
    mc.button(l = 'Create', c = doImport)
    mc.setParent('..')

    mc.optionMenu('padCmb', e = True, sl = 2)
    mc.optionMenu('digitCmb', e = True, sl = 2)
    mc.showWindow('createCamWin')
    
    displayCamName()