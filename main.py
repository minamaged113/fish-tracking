##########################################################
#       Library Includes
##########################################################

import sys
## Functionality Libraries
import os
import cv2
import json
import numpy as np
from UI_handler import *
from file_handler import *



def run():
    cwd = os.getcwd()
    app = QApplication(sys.argv)
    MainWindow = FMainContainer()
    app.exec_()
    #sys.exit()
    return

run()
