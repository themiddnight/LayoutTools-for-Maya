def run():
	from lay_app import lay_app_UI
	try:
		reload(lay_app_UI)
	except:
		import importlib
		importlib.reload(lay_app_UI)

	lay_app_UI.LayoutToolUI()