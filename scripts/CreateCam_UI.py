'''The tool for creating shots with cameras assigned and naming.'''

from pymel.core import *
from maya.cmds import file

def createCamUI():
    if window('createCamWin', exists = True):
        deleteUI('createCamWin')
    window('createCamWin', t = 'Create Cameras', mxb = False)
    
    def displayCamName(*args):
        startNum, endNum = camName()
        text('camNameDis', e = True, l = '%s - %s' %(startNum, endNum))
    
    mainLay = columnLayout(adj = True, rs = 5, cat = ['both', 5])
    with mainLay:
        settingLay = rowColumnLayout(nc = 2, cw = [2,200], cal = [1,'right'], cs = [1,5], rs = [1,5])
        with settingLay:
            text(l = 'Camera file path: ')
            textField('camPathTxt')
            text(l = 'Start num: ')
            intField('startNumInt', v = 1, cc = displayCamName)
            text(l = 'Count: ')
            intField('countInt', v = 10, cc = displayCamName)
            text(l = 'Name prefix: ')
            textField('prefixTxt', tx = 'cam_', cc = displayCamName)
            text(l = 'Pad: ')
            optionMenu('padCmb', cc = displayCamName)
            menuItem(l = '3')
            menuItem(l = '4')
            text(l = 'Digit: ')
            optionMenu('digitCmb', cc = displayCamName)
            menuItem(l = '1')
            menuItem(l = '10')
        text('camNameDis', l = 'test')
        button(l = 'Create', c = doImport)
    optionMenu('padCmb', e = True, sl = 2)
    optionMenu('digitCmb', e = True, sl = 2)
    showWindow('createCamWin')
    
    displayCamName()

def getData(*args):
    filePath = textField('camPathTxt', q = True, tx = True)
    prefix = textField('prefixTxt', q = True, tx = True)
    startNumInt = intField('startNumInt', q = True, v = True)
    countNumInt = intField('countInt', q = True, v = True)
    
    numPad = optionMenu('padCmb', q = True, v = True)
    numDigit = optionMenu('digitCmb', q = True, v = True)
    
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
                
        file(filePath, r = True, ns = camNameStr)
        
    
def run():
    createCamUI()
