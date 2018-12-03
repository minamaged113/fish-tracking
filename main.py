##########################################################
#       Library Includes
##########################################################

import sys
## Functionality Libraries
import os
import cv2
import json
import numpy as np
import matplotlib.pyplot as plt
from skimage.transform import rescale
from UI_handler import *
from file_handler import *



def run():
    cwd = os.getcwd()
    app = QApplication(sys.argv)
    MainWindow = FMainContainer()
    sys.exit(app.exec_())
    return

run()
