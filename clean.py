import os
import shutil

def clean():
    rootDir = '.'
    for dirName in os.walk(rootDir):
        if("venv" in dirName
            or "vscode" in dirName 
            or "git" in dirName):
            continue
        if ("__pycache__" in dirName):
            shutil.rmtree(dirName)
            print("Removed directory: {}".format(dirName))
