def run():
    import sys
    from imp import reload
    path = 'C:/Users/themi/Documents/GitHub/LayoutTools-for-Maya' # <--- put script's dir here
    if path not in sys.path: sys.path.append(path)
    from LayoutTool import LayoutTool_UI
    reload(LayoutTool_UI)
    LayoutTool_UI.LayoutToolUI()
	
run()