'''Remove the namespace of the selected object.'''

import maya.cmds as mc

def main(*args):
    mc.namespace(set = ':')
    sel = mc.ls(sl = True)
    nsRaw = []
    for i in sel:
        if ':' in i:
            nsRaw.append(i.split(':')[0])
    ns = list(dict.fromkeys(nsRaw))
    
    for i in ns:
        mc.namespace(mv = (i, ':'), force = True)
        mc.namespace(removeNamespace = i)
