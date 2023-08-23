def run():
    path = 'C:/Users/themi/Documents/GitHub/LayoutTools-for-Maya'
    import sys
    if path not in sys.path: 
        sys.path.append(path)
    from LayoutTool import LayoutTool_UI
    reload(LayoutTool_UI)
    
    LayoutTool_UI.LayoutToolUI()
	
run()