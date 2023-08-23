import pymel.core as pm
import maya.mel as mel
import os
import sys
import json

class LayoutToolCore:
    def __init__(self):
        self.pref_default = {"refCam": "persp", 
                        "customScriptBtn": ["RxPlacementToOffset", "BakeShakeCam_UI", "DeleteShot", "PublishCheckTool_UI"], 
                        "lensList": [24, 28, 35, 50, 85, 135]}

        self.documents_path = os.path.join(os.getenv('USERPROFILE'), 'Documents\\maya\\')
        self.scripts_path = 'C:/Users/themi/Documents/GitHub/LayoutTools-for-Maya/scripts/'
            
    def getPref(self, data):
        def setDefault():
            with open(self.documents_path + 'LayoutTool_pref.json', 'w') as file:
                json.dump(self.pref_default, file)
            with open(self.documents_path + 'LayoutTool_pref.json', 'r') as file:
                pref = json.load(file)
                value = pref[data]
            return value
        try:
            with open(self.documents_path + 'LayoutTool_pref.json', 'r') as file:
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
            
    def savePref(self, data, value):
        with open(self.documents_path + 'LayoutTool_pref.json', 'r') as file:
            pref = json.load(file)
        pref[data] = value
        with open(self.documents_path + 'LayoutTool_pref.json', 'w') as file:
            json.dump(pref, file)
            
    def getScripts(self):
        scriptsPath = os.listdir(self.scripts_path)
        scripts = list(i.split('.')[0] for i in scriptsPath if '.pyc' not in i and '__init__' not in i and '.DS_Store' not in i)
        return scripts
        
    def getScripDescription(self, scriptName):
        descriptionTxLs = []
        with open(self.scripts_path + scriptName + '.py') as script:
            for i in script.readlines():
                if '### ENDDESCRIPTION' in i or 'import' in i:
                    break
                descriptionTxLs.append(i)
        return ''.join(descriptionTxLs)

    def runScript(self, scriptName):
        pyCmd = '''from scripts import %s \nreload(%s) \n%s.run()''' %(scriptName, scriptName, scriptName)
        exec(pyCmd)
        
    def addScriptToShelf(self, scriptName):
        current_shelf = mel.eval("$shelves = `tabLayout -q -selectTab $gShelfTopLevel`")
        """from LayoutTool import scriptUsage
            from scripts import %s 
            reload(scriptUsage)
            reload(%s) 
            script = '%s'
            runfrom = 'shelf'
            %s.run()"""
        pyCmd = """
from scripts import %s 
reload(%s) 
script = '%s'
runfrom = 'shelf'
%s.run()""" %(scriptName, scriptName, scriptName, scriptName)
        pm.shelfButton(
            image = 'pythonFamily.png',
            command = pyCmd,
            label = scriptName,
            ann = scriptName,
            iol = scriptName,
            parent = current_shelf
        )