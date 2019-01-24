"""
This module is used to initialize `File` drop down menu
that is placed in the main menu bar.

Functions used are available in the `UI_utils` module.

Takes an instance of class `QMainWindow` which in this case
is called `FMainContainer`
"""

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from UI.UI_utils import *

def FFileMenu_init(FMainContainer):
    FMainContainer.openFileAction = QAction("Open File", FMainContainer)
    FMainContainer.openFileAction.setShortcut("Ctrl+O")
    FMainContainer.openFileAction.setStatusTip("Loads a new file to the program.")
    FMainContainer.openFileAction.triggered.connect(lambda : FOpenFile(FMainContainer.centralWidget()))

    ## TODO : load a folder for a day processing
    FMainContainer.openFolderAction = QAction("Open Folder", FMainContainer)
    FMainContainer.openFolderAction.setShortcut("Ctrl+Shift+O")
    FMainContainer.openFolderAction.setStatusTip("Opens a whole folder and loads it to the program.")
    FMainContainer.openFolderAction.triggered.connect(lambda : print_stat_msg("Open Folder pressed."))
    FMainContainer.openFolderAction.setEnabled(False)

    ## TODO : add signal handler to save file after editing.
    FMainContainer.saveFileAction = QAction("Save", FMainContainer)
    FMainContainer.saveFileAction.setShortcut("Ctrl+S")
    FMainContainer.saveFileAction.setStatusTip("Saves the current file.")
    FMainContainer.saveFileAction.triggered.connect(lambda : print_stat_msg("save file pressed."))
    FMainContainer.saveFileAction.setEnabled(False)

    ## TODO : add signal handler to save file as new file 
    FMainContainer.saveFileAsAction = QAction("Save as ...", FMainContainer)
    FMainContainer.saveFileAsAction.setShortcut("Ctrl+Shift+S")
    FMainContainer.saveFileAsAction.setStatusTip("Saves current work as new file.")
    FMainContainer.saveFileAsAction.triggered.connect(lambda : print_stat_msg("Save file as pressed."))
    FMainContainer.saveFileAsAction.setEnabled(False)

    ## TODO : setEnabled(True) only when the user opens a new file.
    FMainContainer.exportAsJPGAction = QAction("Export as JPG", FMainContainer)
    FMainContainer.exportAsJPGAction.setStatusTip("Saves number of images on the drive in a given directory.")
    FMainContainer.exportAsJPGAction.triggered.connect(exportAsJPGActionFunction)
    FMainContainer.exportAsJPGAction.setEnabled(True)

    ## TODO : setEnabled(True) only when the user opens a new file.
    FMainContainer.export_BGS_AsJPGAction = QAction("Export BGS as JPG", FMainContainer)
    FMainContainer.export_BGS_AsJPGAction.setStatusTip("Saves number of backgrounf subtracted images on the drive in a given directory.")
    FMainContainer.export_BGS_AsJPGAction.triggered.connect(export_BGS_AsJPGActionFunction)
    FMainContainer.exportAsJPGAction.setEnabled(True)

    FMainContainer.exitAction = QAction("Exit", FMainContainer)
    FMainContainer.exitAction.setShortcut("Ctrl+Q")
    FMainContainer.exitAction.setStatusTip("Exits the application.")
    FMainContainer.exitAction.triggered.connect(QCoreApplication.instance().quit)

    FMainContainer.fileMenu = FMainContainer.mainMenu.addMenu("&File")
    FMainContainer.fileMenu.addAction(FMainContainer.openFileAction)
    FMainContainer.fileMenu.addAction(FMainContainer.openFolderAction)
    FMainContainer.fileMenu.addAction(FMainContainer.saveFileAction)
    FMainContainer.fileMenu.addAction(FMainContainer.saveFileAsAction)
    FMainContainer.fileMenu.addAction(FMainContainer.exportAsJPGAction)
    FMainContainer.fileMenu.addAction(FMainContainer.export_BGS_AsJPGAction)
    FMainContainer.fileMenu.addSeparator()
    FMainContainer.fileMenu.addAction(FMainContainer.exitAction)