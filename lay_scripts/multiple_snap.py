'''Snap multiple objects to one target.
- Select any objects, then select the last object as target and run.'''

import sys, os
path = os.environ['layout_tool_path'] + '/lay_modules/'
if path not in sys.path: sys.path.append(path)

import maya.cmds as cmds
import snap_mod

def run():
    sel = cmds.ls(sl = True)
    snap_mod.snap(sel)