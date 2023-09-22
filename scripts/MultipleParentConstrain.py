'''Contraining multiple objects to one target object. The last selected object is the target.'''

from pymel.core import *

def run():
    sel = ls(sl = True)
    constrainTo = sel.pop(-1)
    for i in sel:
        parentConstraint(constrainTo, i, mo = True)
