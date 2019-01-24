"""
This module is used to initialize `Edit` drop down menu
that is placed in the main menu bar.

Functions used are available in the `UI_utils` module.

Takes an instance of class `QMainWindow` which in this case
is called `FMainContainer`
"""

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from UI.UI_utils import *

def FEditMenu_init(FMainContainer):
    ## TODO : implement undo function
    FMainContainer.undoAction = QAction("Undo", FMainContainer)
    FMainContainer.undoAction.setShortcut("Ctrl+Z")
    FMainContainer.undoAction.setStatusTip("Undoes the last action.")
    FMainContainer.undoAction.triggered.connect(lambda: print_stat_msg("Undo pressed."))

    ## TODO : implement redo function
    FMainContainer.redoAction = QAction("Redo", FMainContainer)
    FMainContainer.redoAction.setShortcut("Ctrl+Y")
    FMainContainer.redoAction.setStatusTip("Redoes the last action.")
    FMainContainer.redoAction.triggered.connect(lambda: print_stat_msg("Redo pressed."))

    FMainContainer.editMenu = FMainContainer.mainMenu.addMenu("&Edit")
    FMainContainer.editMenu.addAction(FMainContainer.undoAction)
    FMainContainer.editMenu.addAction(FMainContainer.redoAction)

