##########################################################
#       Library Includes
##########################################################
## UI Libraries
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
## Functionality Libraries
from aris_utils import file_info as ARIS_File
import aris_utils.error_description as err
import os
import cv2
import json
import numpy as np
import matplotlib.pyplot as plt
from skimage.transform import rescale


def run():
    cwd = os.getcwd()
    app = QApplication(sys.argv)
    MainWindow = FWelcomeScreen()
    sys.exit(app.exec_())

run()
