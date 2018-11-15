from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

## Other windows connected to this one
from UI.FWelcomeInfo import *
from UI.FViewer import *


## Other entities dealing with the UI
#   - File handler for opening SONAR Files
from file_handler import *
from pathlib import Path

import os
import cv2

class FWelcomeScreen(QMainWindow):
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
        
        

    def initUI(self):
        self.setWindowIcon(QIcon("/home/mghobria/Desktop/fish-tracking/UI/icons/salmon/salmon_64"))
        self.setWindowTitle("Fisher - Welcome Screen")

        self.FMainMenu_init()
        self.showNormal()
        self.width = 640
        self.height = 400
        self.left = 10
        self.top = 10
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
        self.FStatusBar.addPermanentWidget(self.FStatusBarFrameNumber)
        self.setStatusBar(self.FStatusBar)
        return

    def FFileMenu_init(self):
        openFileAction = QAction("Open File", self)
        openFileAction.setShortcut("Ctrl+O")
        openFileAction.setStatusTip("Loads a new file to the program.")
        openFileAction.triggered.connect(self.FOpenFile)

        ## TODO : load a folder for a day processing
        openFolderAction = QAction("Open Folder", self)
        openFolderAction.setShortcut("Ctrl+Shift+O")
        openFolderAction.setStatusTip("Opens a whole folder and loads it to the program.")
        openFolderAction.triggered.connect(lambda : self.print_stat_msg("Open Folder pressed."))
        openFolderAction.setEnabled(False)

        ## TODO : add signal handler to save file after editing.
        saveFileAction = QAction("Save", self)
        saveFileAction.setShortcut("Ctrl+S")
        saveFileAction.setStatusTip("Saves the current file.")
        saveFileAction.triggered.connect(lambda : self.print_stat_msg("save file pressed."))
        saveFileAction.setEnabled(False)

        ## TODO : add signal handler to save file as new file 
        saveFileAsAction = QAction("Save as ...", self)
        saveFileAsAction.setShortcut("Ctrl+Shift+S")
        saveFileAsAction.setStatusTip("Saves current work as new file.")
        saveFileAsAction.triggered.connect(lambda : self.print_stat_msg("Save file as pressed."))
        saveFileAsAction.setEnabled(False)

        ## TODO : setEnabled(True) only when the user opens a new file.
        exportAsJPGAction = QAction("Export as JPG", self)
        exportAsJPGAction.setStatusTip("Saves number of images on the drive in a given directory.")
        exportAsJPGAction.triggered.connect(self.exportAsJPGActionFunction)
        exportAsJPGAction.setEnabled(True)

        ## TODO : setEnabled(True) only when the user opens a new file.
        export_BGS_AsJPGAction = QAction("Export BGS as JPG", self)
        export_BGS_AsJPGAction.setStatusTip("Saves number of backgrounf subtracted images on the drive in a given directory.")
        export_BGS_AsJPGAction.triggered.connect(self.export_BGS_AsJPGActionFunction)
        exportAsJPGAction.setEnabled(True)

        exitAction = QAction("Exit", self)
        exitAction.setShortcut("Ctrl+Q")
        exitAction.setStatusTip("Exits the application.")
        exitAction.triggered.connect(QCoreApplication.instance().quit)

        fileMenu = self.mainMenu.addMenu("&File")
        fileMenu.addAction(openFileAction)
        fileMenu.addAction(openFolderAction)
        fileMenu.addAction(saveFileAction)
        fileMenu.addAction(saveFileAsAction)
        fileMenu.addAction(exportAsJPGAction)
        fileMenu.addAction(export_BGS_AsJPGAction)
        fileMenu.addSeparator()
        fileMenu.addAction(exitAction)

    def FHelpMenu_init(self):
        ## TODO : add signal handler to open webpage
        aboutAction = QAction("About", self)
        aboutAction.setStatusTip("Opens a webpage contains all info about the project.")
        aboutAction.triggered.connect(lambda: self.print_stat_msg("About pressed"))
        aboutAction.setEnabled(False)

        ## TODO : add signal handler to check for updates
        checkForUpdatesAction = QAction("Check for updates", self)
        checkForUpdatesAction.setStatusTip("Check for updates online")
        checkForUpdatesAction.triggered.connect(lambda: self.print_stat_msg("Check for updates pressed."))
        checkForUpdatesAction.setEnabled(False)

        ## TODO : add signal handler to show license file.
        viewLicenseAction = QAction("View License", self)
        viewLicenseAction.setStatusTip("Shows the licenses for the whole software.")
        viewLicenseAction.triggered.connect(lambda: self.print_stat_msg("view license pressed."))
        viewLicenseAction.setEnabled(False)

        ## TODO : add signal handler to report an issue with the software
        reportAction = QAction("Report Issue", self)
        reportAction.setStatusTip("Report an issue to the developers.")
        reportAction.triggered.connect(lambda : self.print_stat_msg("reprot issure pressed."))
        reportAction.setEnabled(False)
        
        ## TODO : add signal handler to show statistics
        showStatisticsAction = QAction("Statistics", self)
        showStatisticsAction.setStatusTip("Shows statistics about old processed files.")
        showStatisticsAction.triggered.connect(lambda : self.print_stat_msg("Statistics pressed."))
        showStatisticsAction.setEnabled(False)

        helpMenu = self.mainMenu.addMenu("&Help")
        helpMenu.addAction(showStatisticsAction)
        helpMenu.addSeparator()
        helpMenu.addAction(reportAction)
        helpMenu.addAction(viewLicenseAction)
        helpMenu.addAction(checkForUpdatesAction)
        helpMenu.addSeparator()
        helpMenu.addAction(aboutAction)


    def FEditMenu_init(self):
        ## TODO : implement undo function
        undoAction = QAction("Undo", self)
        undoAction.setShortcut("Ctrl+Z")
        undoAction.setStatusTip("Undoes the last action.")
        undoAction.triggered.connect(lambda: self.print_stat_msg("Undo pressed."))

        ## TODO : implement redo function
        redoAction = QAction("Redo", self)
        redoAction.setShortcut("Ctrl+Y")
        redoAction.setStatusTip("Redoes the last action.")
        redoAction.triggered.connect(lambda: self.print_stat_msg("Redo pressed."))

        editMenu = self.mainMenu.addMenu("&Edit")
        editMenu.addAction(undoAction)
        editMenu.addAction(redoAction)



    
    def print_stat_msg(self, text):
        ## TODO : delete this function
        print(text)

    def FOpenFile(self):
        ## DEBUG : remove filePathTuple and uncomment filePathTuple
        home = str(Path.home())
        # filePathTuple = ('/home/mghobria/Documents/work/data/data.aris',) # laptop
        filePathTuple = ('data.aris',) # Home PC
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
