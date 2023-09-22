'''Remove the namespace of the selected object.'''

import pymel.core as pm

def doRemoveNS(*args):
    pm.namespace(set = ':')
    sel = pm.ls(sl = True)
    nsRaw = []
    for i in sel:
        if ':' in i:
            nsRaw.append(i.split(':')[0])
    ns = list(dict.fromkeys(nsRaw))
    
    for i in ns:
        pm.namespace(mv = (i, ':'), force = True)
        pm.namespace(removeNamespace = i)
    
def run():
    doRemoveNS()
