"""If you can't delete some objects, try to run this."""

import maya.cmds as mc

def run(): 
    allNodes = mc.ls()
    for node in allNodes:
        mc.lockNode(node, l = False)
