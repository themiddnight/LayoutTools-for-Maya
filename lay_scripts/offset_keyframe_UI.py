'''Offset all animation keyframes in the selected range'''

import maya.cmds as cmds
import sys

import sys, os
path = os.environ['layout_tool_path'] + '/lay_modules/'
if path not in sys.path: sys.path.append(path)

import offset_key_mod

class IntInput:
    def __init__(
            self, label='', value=0, check=False, isCheck=False, 
            labelW=100, fieldW=100, parent=None):
        self.__check = check
        row = cmds.rowLayout(nc=3, p=parent)
        self.__label = cmds.text(l=label, al='right', w=labelW, p=row)
        self.__field = cmds.intField(
                        v=value, w=fieldW, p=row, 
                        en=isCheck if check == True else True)
        if self.__check:
            self.__checkBox = cmds.checkBox(
                                l=label, v=isCheck, p=row, 
                                cc=self.__setEnabling)
        
    def __setEnabling(self, *args):
        isChecked = cmds.checkBox(self.__checkBox, q=True, v=True)
        cmds.intField(self.__field, e=True, en=isChecked)
            
    def getValue(self, *args):
        if self.__check:
            isCheck = cmds.checkBox(self.__checkBox, q=True, v=True)
            return cmds.intField(self.__field, q=True, v=True) \
                        if isCheck == True else None
        return cmds.intField(self.__field, q=True, v=True)


def doShiftFrame(start, end, offset):
    offset_key_mod.offsetKeyframe(offset, start, end)


# ----- UI ------

def run():
    if cmds.window('offsetKeyWin', q=True, exists=True):
        cmds.deleteUI('offsetKeyWin')
    
    cmds.window('offsetKeyWin', t='Offset Keyframe')
    main = cmds.columnLayout(adj=True)
    startField = IntInput(
                    label='Start bound', value=1001, check=True, 
                    isCheck=False, parent=main)
    endField = IntInput(
                    label='End bound', value=1024, check=True, 
                    isCheck=False, parent=main)
    offsetField = IntInput(label='Offset', parent=main)
    cmds.button( 
        l='Apply', p=main, 
        c=lambda x: doShiftFrame( 
                        startField.getValue(),
                        endField.getValue(),
                        offsetField.getValue() ) )
    
    cmds.showWindow('offsetKeyWin')