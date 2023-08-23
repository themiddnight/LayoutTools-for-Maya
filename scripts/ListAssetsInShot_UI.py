import pymel.core as pm

def doListAsset(*args):
    currentShot = pm.ls(pm.sequenceManager(q = True, currentShot = True))[0]
    currentCam = pm.shot(currentShot, q = True, cc = True).split(':')[0]
    currentList = pm.scrollField('shotAssetLsTx', q = True, text = True)
    
    objLs = []
    sel = pm.ls(sl = True)
    for i in sel:
        if ':' in i:
            objLs.append(i.split(':')[0].split('_')[0])
    assetList = list(set(objLs))
    assetList.sort()
    
    if not currentList:
        pm.scrollField('shotAssetLsTx', e = True, text = currentCam + "\n" + "\n".join(assetList))
    else:
        pm.scrollField('shotAssetLsTx', e = True, text = currentList + "\n" + "\n" + currentCam + "\n" + "\n".join(assetList))
        
    extractData()

def extractData(*args):
    dataRaw = pm.scrollField('shotAssetLsTx', q = True, text = True)
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
        
    pm.scrollField('assetShotLsTx', e = True, text = output)

def listAssetUI():
    if pm.window('listAssetWin', exists = True):
        pm.deleteUI('listAssetWin')
    pm.window('listAssetWin', t = 'Shot Asset List')
    mainLay = pm.columnLayout(adj = True,cal = 'left', co = ['both', 10], rs = 10)
    with mainLay:
        pm.separator(style = 'none')
        txField = pm.rowColumnLayout(nc = 2, cs = [2,5], rs = [2,5])
        with txField:
            pm.text(l = 'Shot based:', al = 'left')
            pm.text(l = 'Asset based:', al = 'left')
            pm.scrollField('shotAssetLsTx', editable = True, wordWrap = False, h = 300, w = 200)
            pm.scrollField('assetShotLsTx', editable = False, wordWrap = False, h = 300, w = 200, bgc = [0.22,0.22,0.22])
        pm.button(l = 'List', c = doListAsset)
        pm.button(l = 'Refresh', c = extractData)
        pm.separator(style = 'none')
    pm.showWindow('listAssetWin')

def run():
    listAssetUI()
