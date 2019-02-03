##########################################################
#       Library Includes
##########################################################

import sys
import PyQt5.QtWidgets as pyqtWidgets
## Functionality Libraries
import os
import UI_handler as ui
import file_handler as fh



def run():
    cwd = os.getcwd()
    app = pyqtWidgets.QApplication(sys.argv)
    MainWindow = ui.FMainContainer()
    app.exec_()
    return

run()
