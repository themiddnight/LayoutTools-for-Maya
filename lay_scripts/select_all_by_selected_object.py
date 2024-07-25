'''Select all ctrl that is the same of the selected.

Ex. "shoulder_R_ctrl" of a character is selected. Run this script to select all "shoulder_R_ctrl" of every character in the scene.'''

import maya.cmds as mc

def run():
    selLs = mc.ls(sl = True)
    for i in selLs:
        sel = i.split(':')[-1]
        mc.select(mc.ls('*:%s' %sel, r = True), add = True)
