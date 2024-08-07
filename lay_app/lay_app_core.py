import maya.cmds as mc
import maya.mel as mm
import os
import json
import ast


class LayoutToolCore:
    def __init__(self, *args, **kwargs):

        self.pref_path = os.path.join(os.getenv('USERPROFILE'), 'Documents\\maya\\')
        self.root = os.environ['layout_tool_path']
        self.scripts_path = self.root + '/lay_scripts/'

        self.pref_default = {
            "refCam": "persp", 
            "customScriptBtn": [], 
            "lensList": [24, 28, 35, 50, 85, 135]
        }
            

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
            dialog = mc.confirmDialog(
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
        scripts = []
        for file in scriptsPath:
            if '.py' in file \
            and '.pyc' not in file \
            and '__init__' not in file:
                scripts.append(file.split('.')[0])
        return scripts
        

    def getScripDescription(self, scriptName):
        with open(self.scripts_path + scriptName + '.py') as f:
            txt = f.read()
        module = ast.parse(txt)
        docstring = ast.get_docstring(module)
        if not docstring:
            docstring = ""
        return docstring


    def runScript(self, scriptName):
        pyCmd = '''
from lay_scripts import %s
try:
    reload(%s)
except:
    import importlib
    importlib.reload(%s)
%s.run()
''' %(scriptName, scriptName, scriptName, scriptName)
        exec(pyCmd)
        

    def addScriptToShelf(self, scriptName):
        app_path = os.environ['layout_tool_path']
        pyCmd = "import os\nos.environ['layout_tool_path'] = '%s'\n" %(app_path)
        with open(self.scripts_path + scriptName + ".py", "r") as file:
            pyCmd += file.read() + "\n\nrun()"
            
        current_shelf = mm.eval("$shelves = `tabLayout -q -selectTab $gShelfTopLevel`")
        mc.shelfButton(
            image = 'pythonFamily.png',
            command = pyCmd,
            label = scriptName,
            ann = scriptName + '\n\n' + self.getScripDescription(scriptName),
            iol = scriptName,
            parent = current_shelf
        )