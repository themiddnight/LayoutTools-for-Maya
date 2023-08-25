# Put script's dir below, run this in maya
path = 'C:/Users/pathompong/Downloads/LayoutTools-for-Maya' 
import sys
if path not in sys.path: sys.path.append(path)
from imp import reload
import LayoutTool_run
reload(LayoutTool_run)
LayoutTool_run.run()