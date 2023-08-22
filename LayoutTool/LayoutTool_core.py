import pymel.core as pm
import maya.mel as mel
import os
import sys
import json

pref_default = {"refCam": "persp", 
                "customScriptBtn": ["RxPlacementToOffset", "BakeShakeCam_UI", "DeleteShot", "PublishCheckTool_UI"], 
                "lensList": [24, 28, 35, 50, 85, 135]}

user_home = os.getenv('USERPROFILE')
documents_path = os.path.join(user_home, 'Documents\\maya\\')
      
def getPref(data):
    def setDefault():
        with open(documents_path + 'LayoutTool_pref.json', 'w') as file:
            json.dump(pref_default, file)
        with open(documents_path + 'LayoutTool_pref.json', 'r') as file:
            pref = json.load(file)
            value = pref[data]
        return value
    try:
        with open(documents_path + 'LayoutTool_pref.json', 'r') as file:
            pref = json.load(file)
            value = pref[data]
    except IOError:
        value = setDefault()
    except ValueError:
        dialog = pm.confirmDialog(title = 'Confirm', 
                                  message = 'The preference file is invalid. Dou you want to set to default?', 
                                  button=['OK','Cancel'], defaultButton='OK', 
                                  cancelButton='Cancel', dismissString='No')
        if dialog == 'OK':
            value = setDefault()
        else:
            pass
    return value
    
def savePref(data, value):
    with open(documents_path + 'LayoutTool_pref.json', 'r') as file:
        pref = json.load(file)
    pref[data] = value
    with open(documents_path + 'LayoutTool_pref.json', 'w') as file:
        json.dump(pref, file)
          
def getScripts():
    return [i.split('.')[0] for i in os.listdir(root + '/scripts') if '.pyc' not in i]
    
def getScripDescription(scriptName):
    descriptionTxLs = []
    with open('LayoutTool/' + scriptName + '.py') as script:
        for i in script.readlines():
            if '### ENDDESCRIPTION' in i or 'import' in i:
                break
            descriptionTxLs.append(i)
    return ''.join(descriptionTxLs)

def runScript(scriptName):
    pyCmd = '''import %s \nreload(%s) \n%s.run()''' %(scriptName, scriptName, scriptName)
    exec(pyCmd)
    
def addScriptToShelf(scriptName):
    current_shelf = mel.eval("$shelves = `tabLayout -q -selectTab $gShelfTopLevel`")
    pyCmd = '''from LayoutTool import scriptUsage
import %s 
reload(scriptUsage)
reload(%s) 
script = '%s'
runfrom = 'shelf'
%s.run()
scriptUsage.addData(script, runfrom)''' %(scriptName, scriptName, scriptName, scriptName)
    pm.shelfButton(
        image = 'pythonFamily.png',
        command = pyCmd,
        label = scriptName,
        ann = scriptName,
        iol = scriptName,
        parent = current_shelf
    )