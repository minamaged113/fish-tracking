##########################################################
#       Library Includes
##########################################################

import sys
import PyQt5.QtWidgets as pyqtWidgets
## Functionality Libraries
import os
import clean

_MAIN_DIRECTORY = os.getcwd()
sys.path.append(os.path.join(_MAIN_DIRECTORY, "UI"))
import UI_handler as ui
import file_handler as fh



def run():
    app = pyqtWidgets.QApplication(sys.argv)
    MainWindow = ui.FMainContainer()
    app.exec_()
    clean.clean()
    return

run()