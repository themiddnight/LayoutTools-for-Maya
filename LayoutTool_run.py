def run():
	import json
	from LayoutTool import LayoutTool_UI, logScriptUsage
	reload(LayoutTool_UI)
	reload(logScriptUsage)

	if __name__ == 'LayoutTool_run':
		LayoutTool_UI.LayoutToolUI()

		with open(__file__.split('\\')[0] + '/data/settings.json', 'r') as f:
			settings = json.load(f)
		uiLogging = settings["loggingUiData"]

		if uiLogging == True:
			logging = logScriptUsage.LogScriptUsage()
			logging.addUiData('MainUI', '')