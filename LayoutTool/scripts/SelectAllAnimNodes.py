import maya.cmds as cmd

def run():
    animNodes = cmd.ls(type = 'animCurve')
    cmd.select(animNodes)
