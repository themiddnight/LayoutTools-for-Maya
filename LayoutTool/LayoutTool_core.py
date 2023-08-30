import pymel.core as pm
import maya.mel as mel
import os
import json
import re
import scripts
import logScriptUsage
reload(scripts)
reload(logScriptUsage)


class LayoutToolCore:
    def __init__(self, *args, **kwargs):

        with open(__file__.split('\\')[0] + '/data/settings.json', 'r') as f:
            settings = json.load(f)
        self.logging = settings["loggingData"]

        self.pref_default = {"refCam": "persp", 
                        "customScriptBtn": ["RxPlacementToOffset",
                                            "BakeShakeCam_UI",
                                            "DeleteShot",
                                            "PublishCheckTool_UI"], 
                        "lensList": [24, 28, 35, 50, 85, 135]}

        self.pref_path = os.path.join(os.getenv('USERPROFILE'), 'Documents\\maya\\')
        self.scripts_path = os.path.dirname(scripts.__file__) + '/'
        self.root = self.scripts_path.split('\\')[0]
            

    def getPref(self, data):
        def setDefault():
            with open(self.pref_path + 'LayoutTool_pref.json', 'w') as file:
                json.dump(self.pref_default, file)
            with open(self.pref_path + 'LayoutTool_pref.json', 'r') as file:
                pref = json.load(file)
                value = pref[data]
            return value
        try:
            with open(self.pref_path + 'LayoutTool_pref.json', 'r') as file:
                pref = json.load(file)
                value = pref[data]
        except IOError:
            value = setDefault()
        except ValueError:
            dialog = pm.confirmDialog(
                title = 'Confirm', 
                message = 'The preference file is invalid. Do you want to set to default?', 
                button=['OK','Cancel'], defaultButton='OK', 
                cancelButton='Cancel', dismissString='No')
            if dialog == 'OK':
                value = setDefault()
            else:
                pass
        return value


    def openCustomDir(self, *args):
        os.startfile('%s/manuals' %self.root)
            

    def savePref(self, data, value):
        with open(self.pref_path + 'LayoutTool_pref.json', 'r') as file:
            pref = json.load(file)
        pref[data] = value
        with open(self.pref_path + 'LayoutTool_pref.json', 'w') as file:
            json.dump(pref, file)
            

    def getScripts(self):
        scriptsPath = os.listdir(self.scripts_path)
        scripts = list(i.split('.')[0] for i in scriptsPath if '.pyc' not in i and '__init__' not in i)
        return scripts
        

    def getScripDescription(self, scriptName):
        with open(self.scripts_path + scriptName + '.py') as f:
            txt = f.read()
        matchA = "'''([\\w\\W]*?)'''"
        matchB = '"""([\\w\\W]*?)"""'
        if re.findall(matchA, txt) and txt[:3] == "'''":
            return re.findall(matchA, txt)[0]
        elif re.findall(matchB, txt) and txt[:3] == '"""':
            return re.findall(matchB, txt)[0]
        else:
            return ''


    def runScript(self, scriptName, runfrom):
        reload(logScriptUsage)
        pyCmd = '''from scripts import %s \nreload(%s) \n%s.run()''' %(
            scriptName, scriptName, scriptName)
        exec(pyCmd)
        self.logData(scriptName, runfrom) # if don't want to log usage data, disable this


    def logData(self, scriptName, runfrom):
        if self.logging == True:
            logScriptUsage.LogScriptUsage().addData(scriptName, runfrom)
        

    def addScriptToShelf(self, scriptName):
        current_shelf = mel.eval("$shelves = `tabLayout -q -selectTab $gShelfTopLevel`")
        pyCmd = """root = '%s' 
import sys
if root not in sys.path: sys.path.append(root)
from LayoutTool import LayoutTool_core
reload(LayoutTool_core)
LayoutTool_core.LayoutToolCore().runScript('%s', 'shelf')""" %(self.root, scriptName)
        pm.shelfButton(
            image = 'pythonFamily.png',
            command = pyCmd,
            label = scriptName,
            ann = scriptName + '\n\n' + self.getScripDescription(scriptName),
            iol = scriptName,
            parent = current_shelf
        )
