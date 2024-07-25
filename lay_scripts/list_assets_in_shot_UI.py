'''For listing assets in shots.
- Go to the shot.
- Select the assets in the view and press "List".
- Do it repeatly, it will be added to the list.'''

import maya.cmds as mc

def doListAsset(*args):
    currentShot = mc.ls(mc.sequenceManager(q = True, currentShot = True))[0]
    currentCam = mc.shot(currentShot, q = True, cc = True).split(':')[0]
    currentList = mc.scrollField('shotAssetLsTx', q = True, text = True)
    
    objLs = []
    sel = mc.ls(sl = True)
    for i in sel:
        if ':' in i:
            objLs.append(i.split(':')[0].split('_')[0])
    assetList = list(set(objLs))
    assetList.sort()
    
    if not currentList:
        mc.scrollField('shotAssetLsTx', e = True, text = currentCam + "\n" + "\n".join(assetList))
    else:
        mc.scrollField('shotAssetLsTx', e = True, text = currentList + "\n" + "\n" + currentCam + "\n" + "\n".join(assetList))
        
    extractData()

def extractData(*args):
    dataRaw = mc.scrollField('shotAssetLsTx', q = True, text = True)
    shotGroup = dataRaw.split("\n\n")
    data = {}
    result = {}
    output = ""
    
    # separate shot name and asset list, and append to dict
    for i in shotGroup:
        shotLs = i.split("\n")
        shotName = shotLs.pop(0)
        data[shotName] = shotLs
    
    # extract data
    for key, value in data.items():
        for v in value:
            if v not in result:
                result[v] = [key]
            else:
                result[v].append(key)
    
    # convert dict data to string
    for key, value in sorted(result.items()):
        value.sort()
        output += key + "\n"
        for i in value:
            output += i + "\n"
        output += "\n"
        
    mc.scrollField('assetShotLsTx', e = True, text = output)

def run():
    if mc.window('listAssetWin', exists = True):
        mc.deleteUI('listAssetWin')

    mc.window('listAssetWin', t = 'Shot Asset List')
    mc.columnLayout(adj = True,cal = 'left', co = ['both', 10], rs = 10)
    mc.separator(style = 'none')
    mc.rowColumnLayout(nc = 2, cs = [2,5], rs = [2,5])
    mc.text(l = 'Shot based:', al = 'left')
    mc.text(l = 'Asset based:', al = 'left')
    mc.scrollField('shotAssetLsTx', editable = True, wordWrap = False, h = 300, w = 200)
    mc.scrollField('assetShotLsTx', editable = False, wordWrap = False, h = 300, w = 200, bgc = [0.22,0.22,0.22])
    mc.setParent('..')

    mc.button(l = 'List', c = doListAsset)
    mc.button(l = 'Refresh', c = extractData)
    mc.separator(style = 'none')

    mc.showWindow('listAssetWin')