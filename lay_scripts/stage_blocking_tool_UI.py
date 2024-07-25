'''The tool for stage-blocking work.'''

# import pymel.core as pm
import maya.cmds as mc
import os
import re
import xml.etree.ElementTree as ET
import sys 
sys.path.append("W:\yggpipe\lay\modules")
import snap_mod
reload(snap_mod)

# get env
def getEnv():
    subpjDict = {
                'PNTY':'series'
                }
    pj = os.environ['YGG_PROJECT']
    subpj = subpjDict[pj]
    return subpj, pj

def getSeqInfo():
    shot = mc.ls(type = 'shot')[0]
    shotName = mc.getAttr('%s.shotName' %shot)
    ep = shotName.split('_')[1]
    sq = shotName.split('_')[2]
    return ep, sq

# get dummy files, return path and list of files
def getDummyPath():
    subpj, pj = getEnv()
    dummyPath = "T:/%s/%s/private/[ Layout/Dummy assets" %(subpj, pj)
    dummyList = os.listdir(dummyPath)
    lgtPath = "T:/%s/%s/private/[ Layout/LGT_TOD" %(subpj, pj)
    lgtList = os.listdir(lgtPath)
    return dummyPath, dummyList, lgtPath, lgtList
    
# get all shots
def getAllShots():
    shots = mc.ls(type = 'shot')
    return shots

# import xml
def importXML(*args):
    subpj, pj = getEnv()
    xmlPath = mc.fileDialog(dm = 'T:/%s/%s/publish/edit/*' %(subpj, pj))
    xmlFile = xmlPath.split('/')[-1]
    ep = xmlFile.split('_')[1]
    sq = xmlFile.split('_')[2].split('.')[0]
    tree = ET.parse(xmlPath)
    root = tree.getroot()
    match = '[A-Z]+_[0-9]+_[A-Z0-9]+_[0-9]+'
    
    for item in root.findall('.//clipitem'):
        nameRaw = '%s_%s_%s' %(pj, ep, item.find('name').text)
        print(nameRaw, sq)
        if 'S' in item.find('name').text:
            name = '%s_%s_%s_%s' %(pj, ep, sq, item.find('name').text.split('_')[1])
            sTime = int(item.find('start').text) + 1001
            eTime = int(item.find('end').text) + 1000
            
            mc.shot(name, st = sTime, et = eTime)
            mc.shot(name, e = True, sst = sTime)
            
# import func
def importDummy(fileName, type):
    if type == 0:
        path = "%s/%s" %(getDummyPath()[0], fileName)
    elif type == 1:
        path = "%s/%s" %(getDummyPath()[2], fileName)
    mc.file(path, i = True)

# set shot to dummy cam
def setDummyCam(*args):
    shots = getAllShots()
    cam = 'camera_dummy'
    for i in shots:
        mc.shot(i, e = True, cc = cam)

# set shot to rig cam
def setRigCam(*args):
    shots = getAllShots()
    for i in shots:
        shotName = mc.getAttr('%s.shotName' %i)
        camName = shotName + ':camera'
        mc.shot(i, e = True, cc = camName)
        
# export
def exportDummies(*args):
    subpj, pj = getEnv()
    ep, sq = getSeqInfo()
    mc.select(mc.ls('*_dummy'))
    
    fullPath = "T:/%s/%s/work/shot/%s/%s/0000/lay/maya/scenes/%s_%s_%s_0000_lay_blockingExported.ma" %(subpj, pj, ep, sq, pj, ep, sq)
    exportPath = mc.fileDialog2(fileMode = 0, caption = 'Export', fileFilter = 'MayaAscii (*ma)', dir = fullPath)
    mc.file(exportPath, force = True, typ = "mayaAscii", es = True)

# import
def importDummies(*args):
    subpj, pj = getEnv()
    ep, sq = getSeqInfo()
    fullPath = "T:/%s/%s/work/shot/%s/%s/0000/lay/maya/scenes/*" %(subpj, pj, ep, sq)
    dummyPath = mc.fileDialog(dm = fullPath)
    if dummyPath != '':
        mc.file(dummyPath, i = True)
    
def snapCam(*args):
    shotLs = getAllShots()
    for i in shotLs:
        shotName = mc.getAttr('%s.shotName' %i)
        camCtrl = shotName + ':placement_ctrl'
        sTime = mc.shot(i, q = True, st = True)
        mc.currentTime(sTime)
        snap_mod.snap([camCtrl,'camera_dummy'])
        print(camCtrl, sTime)

def snapRig(*args):    
    shotLs = mc.ls(type = 'shot')
    sel = mc.ls(sl = True)
    obj = sel[0]
    target = sel[-1]
    
    animTime = mc.keyframe(target, q = True, tc = True)
    animTime = list(dict.fromkeys(animTime))
    animTime.sort()
    
    for time in animTime:
        mc.currentTime(time)
        snap_mod.snap([obj, target])
        mc.setKeyframe(obj)
    
# UI
def run():
    fileDummyList = getDummyPath()[1]
    fileLgtList = getDummyPath()[3]
    
    if mc.window('setCamShotWin', exists = True):
        mc.deleteUI('setCamShotWin')
    mc.window('setCamShotWin', t = 'Stage Block Tool', mxb = False)
    
    mainLay = mc.columnLayout(adj = True, rs = 5, cat = ['both',2])
    with mainLay:
        mc.separator(style = 'none')
        
        stageLay = mc.frameLayout(l = 'Stage Blocking', mw = 10, mh = 5, bgs = True, cll = True)
        with stageLay:
            mc.text(l = 'Import XML:', al = 'left')
            mc.button(l = 'Import XML', c = importXML)
            mc.separator()
            
            mc.text(l = 'Import dummies:', al = 'left')
            importLay = mc.columnLayout(adj = True, rs = 5)
            with importLay:
                for i in fileDummyList:
                    if i.endswith('.ma'):
                        mc.button(l = i, c = lambda x, fileName = i: importDummy(fileName, 0))    # 0 = dummy, 1 = light
            mc.separator()
            
            mc.text(l = 'Import scene light:', al = 'left')
            importLay = mc.columnLayout(adj = True, rs = 5)
            with importLay:
                for i in fileLgtList:
                    if i.endswith('.ma'):
                        mc.button(l = i, c = lambda x, fileName = i: importDummy(fileName, 1))
            mc.separator()
            
            mc.button(l = 'Export Stage Blocking', bgc = (0.5,0.5,0.5), h = 50, c = exportDummies)
        mc.separator()
        mc.text(l = 'Assign cam to shots:', al = 'left')
        mc.button(l = 'Dummy Cam', bgc = (0.2,0.2,0.2), c = setDummyCam)
        mc.button(l = 'Rig Cam', bgc = (0.2,0.2,0.2), c = setRigCam)
        mc.separator()
        
        layLay = mc.frameLayout(l = 'Start Layout', mw = 10, mh = 0, bgs = True, cll = True)
        with layLay:
            mc.separator(style = 'none')
            mc.button(l = 'Import Stage Blocking', bgc = (0.5,0.5,0.5), h = 50, c = importDummies)
            mc.separator()
            mc.button(l = 'Snap all Cam Rigs to Dummy Cam', c = snapCam)
            mc.button(l = 'Snap and key selected ctrl to Dummy Char', c = snapRig)
            mc.separator(style = 'none')
    
    mc.showWindow('setCamShotWin')