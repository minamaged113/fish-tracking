import PyQt5.QtCore as pyqtCore
import PyQt5.QtGui as pyqtGUI
import PyQt5.QtWidgets as pyqtWidgets

## Other windows connected to this one
from UI.FWelcomeInfo import *
from UI.FViewer import *
from UI.iconsLauncher import *
import UI.fileMainMenu
import UI.editMainMenu
import UI.helpMainMenu


## Other entities dealing with the UI
import os
import sys
import cv2


class FMainContainer(pyqtWidgets.QMainWindow):
    """This class holds the welcome window which will be used to 
    open ARIS and DIDSON files and show statistics and information
    about the project and the developers.
    
    Arguments:
        pyqtWidgets.QMainWindow {Class} -- inheriting from 
                PyQt5.QtWidgets.QMainWindow class.
    """
    def __init__(self):
        """Initializes the window and displays the main container
        which contains:
            - status bar
            - main menu (File-Edit-Help)
        """

        ##  UI elements description
        pyqtWidgets.QMainWindow.__init__(self)
        self.initUI()
        return
        
        

    def initUI(self):
        self.setWindowIcon(pyqtGUI.QIcon(FGetIcon("salmon", OS = sys.platform)))
        self.setWindowTitle("Fisher - Welcome Screen")

        self.FMainMenu_init()
        self.showNormal()
        self.width = 640
        self.height = 600
        self.left = 100
        self.top = 100
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.FWelcomeInfo = FWelcomeInfo(self)
        self.setCentralWidget(self.FWelcomeInfo)

        
    def FMainMenu_init(self):
        """initializes the main menu for the application.
        """
        self.mainMenu = self.menuBar()
        UI.fileMainMenu.FFileMenu_init(self)
        UI.editMainMenu.FEditMenu_init(self)
        UI.helpMainMenu.FHelpMenu_init(self)
        self.FStatusBar = pyqtWidgets.QStatusBar()
        self.FStatusBarFrameNumber = pyqtWidgets.QLabel()
        self.FStatusBarFrameNumber.setText("No File Loaded")
        self.FStatusBarMousePos = pyqtWidgets.QLabel()
        self.FStatusBar.addPermanentWidget(self.FStatusBarMousePos)
        self.FStatusBar.addPermanentWidget(self.FStatusBarFrameNumber)
        self.setStatusBar(self.FStatusBar)
        return

