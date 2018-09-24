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

##########################################################
#       UI elements
##########################################################

def FGetIcon(icon):
    ## TODO
    """get icon path.
    """

    pass

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
        self.setWindowIcon(QIcon("/home/mghobria/Desktop/fish-tracking/UI/UI_presentation/salmon/salmon_16"))
        self.setWindowTitle("Fisher - Welcome Screen")

        self.FMainMenu_init()
        self.showMaximized() 
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
        self.setStatusBar(self.FStatusBar)
        self.FStatusBarFrameNumber = QLabel()
        self.FStatusBarFrameNumber.setText("No File Loaded")
        self.FStatusBar.addPermanentWidget(self.FStatusBarFrameNumber)
        return

    def FFileMenu_init(self):
        ## TODO : add signal handler to open user files
        openFileAction = QAction("Open File", self)
        openFileAction.setShortcut("Ctrl+O")
        openFileAction.setStatusTip("Loads a new file to the program.")
        openFileAction.triggered.connect(self.FOpenFile)

        ## TODO : load a folder for a day processing
        openFolderAction = QAction("Open Folder", self)
        openFolderAction.setShortcut("Ctrl+Shift+O")
        openFolderAction.setStatusTip("Opens a whole folder and loads it to the program.")
        openFolderAction.triggered.connect(lambda : self.print_stat_msg("Open Folder pressed."))

        ## TODO : add signal handler to save file after editing.
        saveFileAction = QAction("Save", self)
        saveFileAction.setShortcut("Ctrl+S")
        saveFileAction.setStatusTip("Saves the current file.")
        saveFileAction.triggered.connect(lambda : self.print_stat_msg("save file pressed."))

        ## TODO : add signal handler to save file as new file 
        saveFileAsAction = QAction("Save as ...", self)
        saveFileAsAction.setShortcut("Ctrl+Shift+S")
        saveFileAsAction.setStatusTip("Saves current work as new file.")
        saveFileAsAction.triggered.connect(lambda : self.print_stat_msg("Save file as pressed."))

        exitAction = QAction("Exit", self)
        exitAction.setShortcut("Ctrl+Q")
        exitAction.setStatusTip("Exits the application.")
        exitAction.triggered.connect(QCoreApplication.instance().quit)

        fileMenu = self.mainMenu.addMenu("&File")
        fileMenu.addAction(openFileAction)
        fileMenu.addAction(openFolderAction)
        fileMenu.addAction(saveFileAction)
        fileMenu.addAction(saveFileAsAction)
        fileMenu.addSeparator()
        fileMenu.addAction(exitAction)

    def FHelpMenu_init(self):
        ## TODO : add signal handler to open webpage
        aboutAction = QAction("About", self)
        aboutAction.setStatusTip("Opens a webpage contains all info about the project.")
        aboutAction.triggered.connect(lambda: self.print_stat_msg("About pressed"))

        ## TODO : add signal handler to check for updates
        checkForUpdatesAction = QAction("Check for updates", self)
        checkForUpdatesAction.setStatusTip("Check for updates online")
        checkForUpdatesAction.triggered.connect(lambda: self.print_stat_msg("Check for updates pressed."))

        ## TODO : add signal handler to show license file.
        viewLicenseAction = QAction("View License", self)
        viewLicenseAction.setStatusTip("Shows the licenses for the whole software.")
        viewLicenseAction.triggered.connect(lambda: self.print_stat_msg("view license pressed."))

        ## TODO : add signal handler to report an issue with the software
        reportAction = QAction("Report Issue", self)
        reportAction.setStatusTip("Report an issue to the developers.")
        reportAction.triggered.connect(lambda : self.print_stat_msg("reprot issure pressed."))
        
        ## TODO : add signal handler to show statistics
        showStatisticsAction = QAction("Statistics", self)
        showStatisticsAction.setStatusTip("Shows statistics about old processed files.")
        showStatisticsAction.triggered.connect(lambda : self.print_stat_msg("Statistics pressed."))


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


        pass
    
    def print_stat_msg(self, text):
        print(text)

    def FOpenFile(self):
        filePathTuple = QFileDialog.getOpenFileName(self, "Open File", "/home", "Sonar Files (*.aris *.ddf)")
        if filePathTuple[0] != "" : 
            self.FFilePath = filePathTuple[0]
            self.FCentralScreen = FMainWindow(self)
            self.setCentralWidget(self.FCentralScreen)
            self.setWindowTitle("Fisher - " + self.FFilePath)

class FMainWindow(QDialog):
    """This class holds the main window which will be used to 
    show the SONAR images, analyze them and edit images.
    
    Arguments:
        QDialog {Class} -- inheriting from QDialog class.
    """
    fgbg = cv2.createBackgroundSubtractorMOG2()
    UI_FRAME_INDEX = 0
    FRAMES_LIST = list()
    SCALE = 1.0/3.0
    def __init__(self, parent):
        """Initializes the window and loads the first frame and
        places the UI elements, each in its own place.
        """
        self.FParent = parent
        
        ##  Reading the file
        self.FLoadARISFile(self.FParent.FFilePath)
        self.FParent.FStatusBarFrameNumber.setText("Frame : "+str(self.UI_FRAME_INDEX+1)+"/"+str(self.File.frameCount))
        QDialog.__init__(self)
        self.setWindowTitle("Fisher - " + self.FFilePath)
        self.FLayout = QGridLayout()

        FNextBTN = QPushButton("Next",self)
        FNextBTN.clicked.connect(self.FShowNextImage)
        FNextBTN.setShortcut(Qt.Key_Right)
        
        FPreviousBTN = QPushButton("Previous",self)
        FPreviousBTN.clicked.connect(self.FShowPreviousImage)
        FPreviousBTN.setShortcut(Qt.Key_Left)

        self.FLayout.addWidget(FNextBTN,1,1)
        self.FLayout.addWidget(FPreviousBTN,1,0)
       
        self.FDisplayImage()

        self.setLayout(self.FLayout)



    def FShowNextImage(self):
        """Show the next frame image.
        """

        self.UI_FRAME_INDEX +=1
        if (self.UI_FRAME_INDEX > self.File.frameCount-1):
            self.UI_FRAME_INDEX = 0
        self.FDisplayImage()


    def FShowPreviousImage(self):
        """Show the previous frame image
        """

        self.UI_FRAME_INDEX -= 1
        if (self.UI_FRAME_INDEX < 0 ):
            self.UI_FRAME_INDEX = self.File.frameCount-1
        self.FDisplayImage()

    def FDisplayImage(self):
        # self.Frame = self.File.readFrame(self.UI_FRAME_INDEX)
        self.origImage = self.FFrames[self.UI_FRAME_INDEX]
        self.qformat =QImage.Format_Grayscale8
        
        self.origImage = rescale(self.origImage, self.SCALE, anti_aliasing=True)
        self.origImage = (self.origImage*255).astype(np.uint8)
        
        self.image = QImage(self.origImage,
                            self.origImage.shape[1],
                            self.origImage.shape[0],
                            self.origImage.strides[0],
                            self.qformat)
        self.imageLabel = QLabel()
        self.imageLabel.setPixmap(QPixmap.fromImage(self.image))
        
        self.FLayout.addWidget(self.imageLabel,0,0,1,2, Qt.AlignCenter)
        self.FParent.FStatusBarFrameNumber.setText("Frame : "+str(self.UI_FRAME_INDEX+1)+"/"+str(self.File.frameCount))


    def FLoadARISFile(self, filePath):
        self.FFilePath = filePath
        self.File = ARIS_File.ARIS_File(self.FFilePath)
        if(self.File.fileVersion()):
            print("file loaded successfully")
        else:
            print("some error happened")
        self.FLoadARISFileProgress = QProgressDialog("Loading File...", "Cancel!",0, self.File.frameCount,self.FParent)
        self.FLoadARISFileProgress.setWindowTitle("Open File")
        self.FFrames = self.File.getImages()
        # print(json.dumps(self.File.getInfo(), indent = 4))
        # print(self.File.__repr__())

        # frame = file1.readFrame(46)
        # frame.showImage()
        # for i in range(file1.frameCount):
        #     frame = file1.readFrame(i)
        #     # frame.showImage()
        #     ## uncomment the next part to save images on disk
        #     image = frame.FRAME_DATA
        #     image = np.array(image, dtype= np.uint8)
        #     cv2.imwrite("frame_"+ str(i)+ "_data.jpg", image)

    def loadFrameList(self):
        """Function that loads frames before and after the current
        Frame into the memory for faster processing.
        Every time the user presses `Next` or `Previous` it modifies
        the list to maintain the number of loaded frames.

            range: {integer} -- defines number of frames loaded into
                    the memory.

        """

        framesIndices = list()
        range = 10
        if range > (self.File.FRAME_COUNT+1):
            range = self.File.FRAME_COUNT
        for i in range(range):
            framesIndices.append()
            
        pass

class FWelcomeInfo(QDialog):
    """This class will hold information screen about the software
    and its owners and developers.
    
    Arguments:
        QDialog {[Class]} -- PyQt parent class
    """
    
    def __init__(self, parent):
        QDialog.__init__(self)
        self.FParent = parent
        self.FLayout = QGridLayout()

        FOpenFileBTN = QPushButton("OPEN FILE", self)
        FOpenFileBTN.clicked.connect(self.FParent.FOpenFile)

        FShowStatsBTN = QPushButton("STATISTICS", self)
        FShowStatsBTN.clicked.connect(self.FShowStats)

        FAboutBTN = QPushButton("ABOUT", self)
        FAboutBTN.clicked.connect(self.FAbout)

        FInfo = QLabel()
        FInfo.setText("Fisher is an open-source software developed by the University of Oulu, Finland \
in collaboration with the Natural Resources Institute in Finland.")
        FInfo.setWordWrap(True)

        self.FLayout.addWidget(FOpenFileBTN, 0, 0)
        self.FLayout.addWidget(FShowStatsBTN, 1, 0)
        self.FLayout.addWidget(FAboutBTN, 2,0)
        self.FLayout.addWidget(FInfo, 0,1, 3,1)

        self.FLayout.setColumnStretch(0, 1)
        self.FLayout.setColumnStretch(1, 4)
        self.setLayout(self.FLayout)

    def FShowStats(self):
        ## TODO : Implement function to show statistics.
        """Intended statistics include, but not limited to,
            + number of files opened (.ddf, .aris)
            + number of fish captured
            + days with the highest and lowest number of fish
            + Water levels and temperatures

        """

        pass

    def FAbout(self):
        ## TODO : Implement a function to show About information.
        """
        Should either be opening a new window to show information
        about the software and its owners or show a webpage with
        all the information.
        """
        pass


    


def run():
    cwd = os.getcwd()
    app = QApplication(sys.argv)
    MainWindow = FWelcomeScreen()
    sys.exit(app.exec_())

run()
