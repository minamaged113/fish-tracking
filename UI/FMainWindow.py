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
import time

class FMainWindow(QDialog):
    """This class holds the main window which will be used to 
    show the SONAR images, analyze them and edit images.
    
    Arguments:
        QDialog {Class} -- inheriting from QDialog class.
    """
    BGS_Threshold = 25
    fgbg = cv2.createBackgroundSubtractorMOG2(varThreshold = BGS_Threshold)
    UI_FRAME_INDEX = 0
    FRAMES_LIST = list()
    subtractBackground = False
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
        
        self.F_BGS_BTN = QPushButton(self)
        self.F_BGS_BTN.setObjectName("Subtract Background")
        self.F_BGS_BTN.setFlat(True)
        self.F_BGS_BTN.setCheckable(True)
        self.F_BGS_BTN.setIcon(QIcon("/home/mghobria/Desktop/fish-tracking/UI/icons/background_subtraction/black_32.png"))
        self.F_BGS_BTN.clicked.connect(self.FBackgroundSubtract)
        # self.F_BGS_BTN.setShortcut(Qt.Key_Left)

        self.F_BGS_Slider = QSlider(Qt.Vertical)
        self.F_BGS_Slider.setMinimum(0)
        self.F_BGS_Slider.setMaximum(100)
        self.F_BGS_Slider.setTickPosition(QSlider.TicksRight)
        self.F_BGS_Slider.setTickInterval(10)
        self.F_BGS_Slider.setValue(self.BGS_Threshold)
        self.F_BGS_Slider.valueChanged.connect(self.F_BGS_SliderValueChanged)
        self.F_BGS_Slider.setDisabled(True)

        self.FFigure = Figure()
        self.FCanvas = FigureCanvas(self.FFigure)
        self.FToolbar = NavigationToolbar(self.FCanvas, self)
        self.FToolbar.addWidget(self.F_BGS_BTN)
        self.FToolbar.addWidget(self.F_BGS_Slider)
        self.FToolbar.setOrientation(Qt.Vertical)
        self.FToolbar.setFixedWidth(self.FToolbar.minimumSizeHint().width())
        
        self.FSlider = QSlider(Qt.Horizontal)
        self.FSlider.setMinimum(1)
        self.FSlider.setMaximum(self.File.frameCount)
        self.FSlider.setTickPosition(QSlider.TicksBelow)
        self.FSlider.setTickInterval(int(0.05*self.File.frameCount))
        self.FSlider.valueChanged.connect(self.FSliderValueChanged)
        
        
        
        self.FLayout.setContentsMargins(0,0,0,0)
        self.FLayout.addWidget(self.FToolbar,0,0,3,1)
        self.FLayout.setColumnStretch(0,0)
        # self.FLayout.setColumnMinimumWidth(0, 0)
        self.FLayout.addWidget(self.FCanvas,0,1,1,2)
        self.FLayout.addWidget(self.FSlider,1,1,1,2)
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
        
        self.FSlider.setValue(self.UI_FRAME_INDEX)
        tick1 = time.time()
        self.FFrames = self.File.getFrame(self.UI_FRAME_INDEX)
        tick2 = time.time()
        self.FDisplayImage()
        tick3 = time.time()
        print('time to fetch frame = ', tick2-tick1)
        print('time to show frame = ', tick3-tick2)

    def FShowPreviousImage(self):
        """Show the previous frame image
        """

        self.UI_FRAME_INDEX -= 1
        if (self.UI_FRAME_INDEX < 0 ):
            self.UI_FRAME_INDEX = self.File.frameCount-1

        self.FSlider.setValue(self.UI_FRAME_INDEX)
        tick1 = time.time()
        self.FFrames = self.File.getFrame(self.UI_FRAME_INDEX)
        tick2 = time.time()
        self.FDisplayImage()
        tick3 = time.time()
        print('time to fetch frame = ', tick2-tick1)
        print('time to show frame = ', tick3-tick2)

    def FDisplayImage(self):
        if(self.subtractBackground):
            self.FFigure.clf()
            ax = self.FFigure.add_subplot(122)
            # ax.remove()
            ax.clear()
            ax.set_title("Original")
            ax.imshow(self.FFrames, cmap = 'gray')
            fgbg_FFrames = self.fgbg.apply(self.FFrames)
            ax = self.FFigure.add_subplot(121)
            ax.set_title("Background removed")
            ax.imshow(fgbg_FFrames, cmap = 'gray')
        else:
            self.FFigure.clf()
            ax = self.FFigure.add_subplot(111)
            ax.clear()
            ax.set_title("Original")
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
    
    def FBackgroundSubtract(self):
        """
        This function enables and disables background
        subtraction in the UI.
        it is called from F_BGS_BTN QPushButton.
        """
        if (self.F_BGS_BTN.isChecked()):
            self.subtractBackground = True
            self.F_BGS_Slider.setDisabled(False)
            self.FDisplayImage()
        else:
            self.subtractBackground = False
            self.F_BGS_Slider.setDisabled(True)
            self.FDisplayImage()

    def FSliderValueChanged(self):
        self.UI_FRAME_INDEX = self.FSlider.value()
        self.FFrames = self.File.getFrame(self.UI_FRAME_INDEX)
        self.FDisplayImage()

    def F_BGS_SliderValueChanged(self):
        value = self.F_BGS_Slider.value()
        self.fgbg.setVarThreshold(value)