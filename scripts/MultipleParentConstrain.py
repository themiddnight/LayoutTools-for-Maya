from pymel.core import *

def run():
    sel = ls(sl = True)
    constrainTo = sel.pop(-1)
    for i in sel:
        parentConstraint(constrainTo, i, mo = True)
