"""If you can't delete some objects, try to run this."""

from pymel.core import *

def run(): 
    allNodes = ls()
    for node in allNodes:
        lockNode(node, l = False)
