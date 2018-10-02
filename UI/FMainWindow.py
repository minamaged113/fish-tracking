from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import cv2

## library for reading SONAR files
# SF: SONAR File
import file_handler as SF
from skimage.transform import rescale
import numpy as np

## For showing images in matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from matplotlib.pyplot import imshow

class FMainWindow(QDialog):
    """This class holds the main window which will be used to 
    show the SONAR images, analyze them and edit images.
    
    Arguments:
        QDialog {Class} -- inheriting from QDialog class.
    """
    fgbg = cv2.createBackgroundSubtractorMOG2()
    UI_FRAME_INDEX = 0
    FRAMES_LIST = list()
    subtractBackground = 0
    def __init__(self, parent):
        """Initializes the window and loads the first frame and
        places the UI elements, each in its own place.
        """
        self.FParent = parent
        
        ##  Reading the file
        self.FLoadSONARFile(self.FParent.FFilePath)
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
        
        self.FFigure = Figure()
        self.FCanvas = FigureCanvas(self.FFigure)
        self.FToolbar = NavigationToolbar(self.FCanvas, self)
        self.FToolbar.setOrientation(Qt.Vertical)
        self.FToolbar.setMinimumSize(self.FToolbar.minimumSize())
        self.FSlider = QSlider(Qt.Horizontal)
        

        self.FLayout.addWidget(self.FToolbar,0,0,3,1, Qt.AlignLeft)
        self.FLayout.addWidget(self.FCanvas,0,1,1,2)
        self.FLayout.addWidget(self.FSlider,1,1,1,2, Qt.AlignBottom)
        self.FLayout.addWidget(FNextBTN,2,2)
        self.FLayout.addWidget(FPreviousBTN,2,1)
        

       
        self.FDisplayImage()

        self.setLayout(self.FLayout)



    def FShowNextImage(self):
        """Show the next frame image.
        """

        self.UI_FRAME_INDEX +=1
        if (self.UI_FRAME_INDEX > self.File.frameCount-1):
            self.UI_FRAME_INDEX = 0
        
        self.FFrames = self.File.getFrame(self.UI_FRAME_INDEX)
        self.FDisplayImage()
        self.FDisplayImage()

    def FShowPreviousImage(self):
        """Show the previous frame image
        """

        self.UI_FRAME_INDEX -= 1
        if (self.UI_FRAME_INDEX < 0 ):
            self.UI_FRAME_INDEX = self.File.frameCount-1

        self.FFrames = self.File.getFrame(self.UI_FRAME_INDEX)
        self.FDisplayImage()

    def FDisplayImage(self):
        if not (self.FLayout.isEmpty):
            print("empty")
            self.FLayout.removeWidget(0,0)
        if(self.subtractBackground):
            self.FFrames = self.fgbg.apply(self.FFrames)
        ax = self.FFigure.add_subplot(111)
        ax.clear()
        ax.imshow(self.FFrames, cmap = 'gray')
        self.FCanvas.draw()
        self.FParent.FStatusBarFrameNumber.setText("Frame : "+str(self.UI_FRAME_INDEX+1)+"/"+str(self.File.frameCount))


    def FLoadSONARFile(self, filePath):
        self.FFilePath = filePath
        # SF: Sonar File Library
        self.File = SF.FOpenSonarFile(filePath)
        self.FFrames = self.File.FRAMES
        

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
