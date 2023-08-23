# Snap multiple objects to one target
# Select any objects, then select the last object as target and run
### ENDDESCRIPTION

import sys
import maya.cmds as cmds
from modules import snap_mod
reload(snap_mod)

def run():
    sel = cmds.ls(sl = True)
    snap_mod.snap(sel)