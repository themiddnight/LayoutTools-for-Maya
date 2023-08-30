'''Select all ctrl that is the same of the selected.

Ex. "shoulder_R_ctrl" of a character is selected. Run this script to select all "shoulder_R_ctrl" of every character in the scene.'''

from pymel.core import *

def run():
    selLs = ls(sl = True)
    for i in selLs:
        sel = i.split(':')[-1]
        select(ls('*:%s' %sel, r = True), add = True)
