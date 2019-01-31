from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

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


class FMainContainer(QMainWindow):
    """This class holds the welcome window which will be used to 
    open ARIS and DIDSON files and show statistics and information
    about the project and the developers.
    
    Arguments:
        QMainWindow {Class} -- inheriting from QMainWindow class.
    """
    def __init__(self):
        """Initializes the window and displays the main container
        which contains:
            - status bar
            - main menu (File-Edit-Help)
        """

        ##  UI elements description
        QMainWindow.__init__(self)
        self.initUI()
        return
        
        

    def initUI(self):
        self.setWindowIcon(QIcon(FGetIcon("salmon", OS = sys.platform)))
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
        self.FStatusBar = QStatusBar()
        self.FStatusBarFrameNumber = QLabel()
        self.FStatusBarFrameNumber.setText("No File Loaded")
        self.FStatusBarMousePos = QLabel()
        self.FStatusBar.addPermanentWidget(self.FStatusBarMousePos)
        self.FStatusBar.addPermanentWidget(self.FStatusBarFrameNumber)
        self.setStatusBar(self.FStatusBar)
        return

