from pymel.core import *

def run():
    selLs = ls(sl = True)
    for i in selLs:
        sel = i.split(':')[-1]
        select(ls('*:%s' %sel, r = True), add = True)
