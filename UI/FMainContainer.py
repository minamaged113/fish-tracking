from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

## Other windows connected to this one
from UI.FWelcomeInfo import *
from UI.FViewer import *
from UI.iconsLauncher import *

## Other entities dealing with the UI
#   - File handler for opening SONAR Files
from file_handler import *
from pathlib import Path

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
        """Initializes the window and displays brief information
        about LUKE and University of Oulu.
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
        self.FFileMenu_init()
        self.FEditMenu_init()
        self.FHelpMenu_init()
        self.FStatusBar = QStatusBar()
        self.FStatusBarFrameNumber = QLabel()
        self.FStatusBarFrameNumber.setText("No File Loaded")
        self.FStatusBarMousePos = QLabel()
        self.FStatusBar.addPermanentWidget(self.FStatusBarMousePos)
        self.FStatusBar.addPermanentWidget(self.FStatusBarFrameNumber)
        self.setStatusBar(self.FStatusBar)
        return

    def FFileMenu_init(self):
        self.openFileAction = QAction("Open File", self)
        self.openFileAction.setShortcut("Ctrl+O")
        self.openFileAction.setStatusTip("Loads a new file to the program.")
        self.openFileAction.triggered.connect(self.FOpenFile)

        ## TODO : load a folder for a day processing
        self.openFolderAction = QAction("Open Folder", self)
        self.openFolderAction.setShortcut("Ctrl+Shift+O")
        self.openFolderAction.setStatusTip("Opens a whole folder and loads it to the program.")
        self.openFolderAction.triggered.connect(lambda : self.print_stat_msg("Open Folder pressed."))
        self.openFolderAction.setEnabled(False)

        ## TODO : add signal handler to save file after editing.
        self.saveFileAction = QAction("Save", self)
        self.saveFileAction.setShortcut("Ctrl+S")
        self.saveFileAction.setStatusTip("Saves the current file.")
        self.saveFileAction.triggered.connect(lambda : self.print_stat_msg("save file pressed."))
        self.saveFileAction.setEnabled(False)

        ## TODO : add signal handler to save file as new file 
        self.saveFileAsAction = QAction("Save as ...", self)
        self.saveFileAsAction.setShortcut("Ctrl+Shift+S")
        self.saveFileAsAction.setStatusTip("Saves current work as new file.")
        self.saveFileAsAction.triggered.connect(lambda : self.print_stat_msg("Save file as pressed."))
        self.saveFileAsAction.setEnabled(False)

        ## TODO : setEnabled(True) only when the user opens a new file.
        self.exportAsJPGAction = QAction("Export as JPG", self)
        self.exportAsJPGAction.setStatusTip("Saves number of images on the drive in a given directory.")
        self.exportAsJPGAction.triggered.connect(self.exportAsJPGActionFunction)
        self.exportAsJPGAction.setEnabled(True)

        ## TODO : setEnabled(True) only when the user opens a new file.
        self.export_BGS_AsJPGAction = QAction("Export BGS as JPG", self)
        self.export_BGS_AsJPGAction.setStatusTip("Saves number of backgrounf subtracted images on the drive in a given directory.")
        self.export_BGS_AsJPGAction.triggered.connect(self.export_BGS_AsJPGActionFunction)
        self.exportAsJPGAction.setEnabled(True)

        self.exitAction = QAction("Exit", self)
        self.exitAction.setShortcut("Ctrl+Q")
        self.exitAction.setStatusTip("Exits the application.")
        self.exitAction.triggered.connect(QCoreApplication.instance().quit)

        self.fileMenu = self.mainMenu.addMenu("&File")
        self.fileMenu.addAction(self.openFileAction)
        self.fileMenu.addAction(self.openFolderAction)
        self.fileMenu.addAction(self.saveFileAction)
        self.fileMenu.addAction(self.saveFileAsAction)
        self.fileMenu.addAction(self.exportAsJPGAction)
        self.fileMenu.addAction(self.export_BGS_AsJPGAction)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.exitAction)

    def FHelpMenu_init(self):
        ## TODO : add signal handler to open webpage
        self.aboutAction = QAction("About", self)
        self.aboutAction.setStatusTip("Opens a webpage contains all info about the project.")
        self.aboutAction.triggered.connect(lambda: self.print_stat_msg("About pressed"))
        self.aboutAction.setEnabled(False)

        ## TODO : add signal handler to check for updates
        self.checkForUpdatesAction = QAction("Check for updates", self)
        self.checkForUpdatesAction.setStatusTip("Check for updates online")
        self.checkForUpdatesAction.triggered.connect(lambda: self.print_stat_msg("Check for updates pressed."))
        self.checkForUpdatesAction.setEnabled(False)

        ## TODO : add signal handler to show license file.
        self.viewLicenseAction = QAction("View License", self)
        self.viewLicenseAction.setStatusTip("Shows the licenses for the whole software.")
        self.viewLicenseAction.triggered.connect(lambda: self.print_stat_msg("view license pressed."))
        self.viewLicenseAction.setEnabled(False)

        ## TODO : add signal handler to report an issue with the software
        self.reportAction = QAction("Report Issue", self)
        self.reportAction.setStatusTip("Report an issue to the developers.")
        self.reportAction.triggered.connect(lambda : self.print_stat_msg("reprot issure pressed."))
        self.reportAction.setEnabled(False)
        
        ## TODO : add signal handler to show statistics
        self.showStatisticsAction = QAction("Statistics", self)
        self.showStatisticsAction.setStatusTip("Shows statistics about old processed files.")
        self.showStatisticsAction.triggered.connect(lambda : self.print_stat_msg("Statistics pressed."))
        self.showStatisticsAction.setEnabled(False)

        self.helpMenu = self.mainMenu.addMenu("&Help")
        self.helpMenu.addAction(self.showStatisticsAction)
        self.helpMenu.addSeparator()
        self.helpMenu.addAction(self.reportAction)
        self.helpMenu.addAction(self.viewLicenseAction)
        self.helpMenu.addAction(self.checkForUpdatesAction)
        self.helpMenu.addSeparator()
        self.helpMenu.addAction(self.aboutAction)


    def FEditMenu_init(self):
        ## TODO : implement undo function
        self.undoAction = QAction("Undo", self)
        self.undoAction.setShortcut("Ctrl+Z")
        self.undoAction.setStatusTip("Undoes the last action.")
        self.undoAction.triggered.connect(lambda: self.print_stat_msg("Undo pressed."))

        ## TODO : implement redo function
        self.redoAction = QAction("Redo", self)
        self.redoAction.setShortcut("Ctrl+Y")
        self.redoAction.setStatusTip("Redoes the last action.")
        self.redoAction.triggered.connect(lambda: self.print_stat_msg("Redo pressed."))

        self.editMenu = self.mainMenu.addMenu("&Edit")
        self.editMenu.addAction(self.undoAction)
        self.editMenu.addAction(self.redoAction)



    
    def print_stat_msg(self, text):
        ## TODO : delete this function
        print(text)

    def FOpenFile(self):
        ## DEBUG : remove filePathTuple and uncomment filePathTuple
        home = str(Path.home())
        # filePathTuple = ('/home/mghobria/Documents/work/data/data.aris',) # laptop
        filePathTuple = ('data.aris',) # Home PC & windows Laptop
        # filePathTuple = ('/home/mghobria/Documents/work/data/data 1/data.aris',) # work PC
        # filePathTuple = ("C:\\Users\\mghobria\\Downloads\\data.aris",) # Home PC windows
        # filePathTuple = QFileDialog.getOpenFileName(self, "Open File", home, "Sonar Files (*.aris *.ddf)")
        if filePathTuple[0] != "" : 
            self.FFilePath = filePathTuple[0]
            self.FCentralScreen = FViewer(self)
            self.setCentralWidget(self.FCentralScreen)
            self.setWindowTitle("Fisher - " + self.FFilePath)

    def exportAsJPGActionFunction(self):
        name = QFileDialog.getSaveFileName(self, 'Save all frames')[0]
        if not os.path.exists(name):
            os.makedirs(name)
        file = FOpenSonarFile(self.FFilePath)
        numberOfImagesToSave = file.frameCount
        numOfDigits = str(len(str(numberOfImagesToSave)))
        fileName = os.path.splitext(os.path.basename(file.FILE_PATH))[0]
        
        for i in range(numberOfImagesToSave):
        
            frame = file.getFrame(i)
            imgNmbr = format(i, "0"+numOfDigits+"d")
            cv2.imwrite((os.path.join( name,  fileName+ "_"+imgNmbr+".jpg")), frame)
            print("Saving : ", str(i))

        return

    def export_BGS_AsJPGActionFunction(self):
        file = FOpenSonarFile(self.FFilePath)
        numberOfImagesToSave = file.frameCount
        imagesExportDirectory = "/home/mghobria/Pictures/SONAR_Images"
        BGS_Threshold = 25
        fgbg = cv2.createBackgroundSubtractorMOG2(varThreshold = BGS_Threshold)
        for i in range(numberOfImagesToSave):
            frame = file.getFrame(i)
            frame = fgbg.apply(frame)
            cv2.imwrite((os.path.join( imagesExportDirectory, "IMG_BGS_"+str(i)+".jpg")), frame)
            print("Saving : ", str(i))

        return
