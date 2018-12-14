from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import cv2
from UI.iconsLauncher import *
import project

## library for reading SONAR files
# SF: SONAR File
import file_handler as SF
import numpy as np
import time

class checkPlayBTNThread(QThread):
    def __init__(self, cls):
        QThread.__init__(self)
        self.parent = cls

    def __del__(self):
        self.wait()

    def run(self):
        if (not self.parent.FPlayBTN.isChecked()):
            self.parent.FPlayBTN.setIcon(QIcon(FGetIcon('play')))
            self.parent.FLayout.addWidget(self.parent.FPlayBTN, 2, 2)
            self.parent.FPlayThread.terminate()
        
class FPlayThread(QThread):
    repaintSignal = pyqtSignal()
    listOfAllThreads = list()
    def __init__(self, cls):
        QThread.__init__(self)
        self.parent = cls

    def __del__(self):
        self.wait()

    def run(self):
        self.listOfAllThreads.append(self)
        while(self.parent.UI_FRAME_INDEX<self.parent.File.frameCount) and (self.parent.FPlayBTN.isChecked()):
            self.parent.FShowNextImage()
            self.parent.FFigure.update()
            # self.repaintSignal.connect(self.FRepaint)
            # self.repaintSignal.emit()
        # self.parent.FPlayBTN.setIcon(QIcon(FGetIcon('play')))
        # self.parent.FLayout.addWidget(self.parent.FPlayBTN, 2, 2)
        # self.destruct()
        # self.terminate()
                # break
            
        return

    def FRepaint(self):
        self.parent.FFigure.repaint()

    def destruct(self):
        for i in self.listOfAllThreads:
            if(i.isRunning()):
                continue
            i.terminate()
        return


class FFishListItem():
    def __init__(self, cls, inputDict, fishNumber):
        self.fishNumber = fishNumber
        self.inputDict = inputDict
        self.listItem = QListWidgetItem()
        self.FWdiget = QWidget()
        self.FWdigetText = QLabel("Fish #{}".format(self.fishNumber))
        self.FWdigetBTN = QPushButton("Show")
        self.FWdigetBTN.clicked.connect(lambda: cls.showFish(self.fishNumber, self.inputDict))
        self.FWdigetLayout = QVBoxLayout()
        self.FWdigetLayout.addWidget(self.FWdigetText)
        self.FWdigetLayout.addWidget(self.FWdigetBTN)
        self.FWdigetLayout.addStretch()
        self.FWdigetLayout.setSizeConstraint(QLayout.SetFixedSize)
        self.FWdiget.setLayout(self.FWdigetLayout)
        self.listItem.setSizeHint(self.FWdiget.sizeHint())


    


class FViewer(QDialog):
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
    postAnalysisViewer = False
    play = False

    def __init__(self, parent, resultsView = False, results=False):
        """Initializes the window and loads the first frame and
        places the UI elements, each in its own place.
        """
        self.postAnalysisViewer = resultsView
        self.FDetectedDict = results
        self.FParent = parent
        ##  Reading the file
        self.FLoadSONARFile(self.FParent.FFilePath)
        self.FParent.FStatusBarFrameNumber.setText("Frame : "+str(self.UI_FRAME_INDEX+1)+"/"+str(self.File.frameCount))
        QDialog.__init__(self)
        self.setWindowTitle("Fisher - " + self.FFilePath)
        self.FLayout = QGridLayout()

        FNextBTN = QPushButton(self)
        FNextBTN.clicked.connect(self.FShowNextImage)
        FNextBTN.setShortcut(Qt.Key_Right)
        FNextBTN.setIcon(QIcon(FGetIcon('next')))
        
        FPreviousBTN = QPushButton(self)
        FPreviousBTN.clicked.connect(self.FShowPreviousImage)
        FPreviousBTN.setShortcut(Qt.Key_Left)
        FPreviousBTN.setIcon(QIcon(FGetIcon('previous')))
        
        self.FPlayBTN = QPushButton(self)
        self.FPlayBTN.clicked.connect(self.FPlay)
        self.FPlayBTN.setShortcut(Qt.Key_Space)
        self.FPlayBTN.setIcon(QIcon(FGetIcon('play')))
        self.FPlayBTN.setCheckable(True)
        
        

        self.F_BGS_BTN = QPushButton(self)
        self.F_BGS_BTN.setObjectName("Subtract Background")
        self.F_BGS_BTN.setFlat(True)
        self.F_BGS_BTN.setCheckable(True)
        self.F_BGS_BTN.setIcon(QIcon(FGetIcon("background_subtraction")))
        self.F_BGS_BTN.clicked.connect(self.FBackgroundSubtract)

        self.F_BGS_Slider = QSlider(Qt.Vertical)
        self.F_BGS_Slider.setMinimum(0)
        self.F_BGS_Slider.setMaximum(100)
        self.F_BGS_Slider.setTickPosition(QSlider.TicksRight)
        self.F_BGS_Slider.setTickInterval(10)
        self.F_BGS_Slider.setValue(self.BGS_Threshold)
        self.F_BGS_Slider.valueChanged.connect(self.F_BGS_SliderValueChanged)
        self.F_BGS_Slider.setDisabled(True)

        self.FFigure = QLabel("Frame Viewer", self)
        self.FFigure.setUpdatesEnabled(True)
        self.FToolbar = QToolBar(self)
        self.FToolbar.addWidget(self.F_BGS_BTN)
        # self.FToolbar.add
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
        self.FLayout.addWidget(self.FFigure,0,1,1,3)
        self.FLayout.addWidget(self.FSlider,1,1,1,3)
        self.FLayout.addWidget(FPreviousBTN,2,1)
        self.FLayout.addWidget(self.FPlayBTN, 2, 2)
        self.FLayout.addWidget(FNextBTN,2,3)
        if self.postAnalysisViewer:
            self.FListDetected()

       
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
        # return

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
        self.FFigure.clear()

        qformat = QImage.Format_Indexed8

        if len(self.FFrames.shape)==3:
            if self.FFrames.shape[2]==4:
                qformat = QImage.Format_RGBA8888
            else:
                qformat = QImage.Format_RGB888
        
        if(self.subtractBackground):
            
            frameBlur = cv2.blur(self.FFrames, (5,5))
            mask = self.fgbg.apply(frameBlur)
            mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, self.kernel)
            mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, self.kernel)
            mask = cv2.threshold(mask, 128, 255, cv2.THRESH_BINARY)[1]
        
            img = np.hstack((mask, self.FFrames))
            img = QImage(img, img.shape[1], img.shape[0], img.strides[0], qformat)
        
        else:    
            img = QImage(self.FFrames, self.FFrames.shape[1], self.FFrames.shape[0], self.FFrames.strides[0], qformat)
        
        img = img.rgbSwapped()
        self.FFigure.setPixmap(QPixmap.fromImage(img).scaled(self.FFigure.width(), self.FFigure.height(), Qt.KeepAspectRatio))
        self.FFigure.setAlignment(Qt.AlignCenter)
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
        ## TODO
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
            self.kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (10,2))
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

    def FPlay(self):
        ## problem
        self.play = not self.play
        if self.play:
            self.FPlayBTN.setIcon(QIcon(FGetIcon('pause')))
            self.FLayout.addWidget(self.FPlayBTN, 2, 2)
            # while(self.UI_FRAME_INDEX<self.File.frameCount):
            #     self.FShowNextImage()
            #     self.FFigure.repaint()
                
            # self.FDetectedDict = project.FAnalyze(self)
            # if(len(self.FDetectedDict)):
            #     self.FResultsViewer = FViewer(self.FParent, resultsView= True, results=self.FDetectedDict)
            #     self.FParent.setCentralWidget(self.FResultsViewer)
            playThread = FPlayThread(self)
            playThread.start()
            self.FPlayBTN.clicked.connect(self.FPlay)
            # self.buttonCheckThread = checkPlayBTNThread(self)
            # self.buttonCheckThread.start()
        else:
            self.FPlayBTN.setIcon(QIcon(FGetIcon('play')))
            self.FLayout.addWidget(self.FPlayBTN, 2, 2)
            # time.sleep(0.2)
            
        return

    def FListDetected(self):
        count = 1
        listOfFish = list()
        self.FList = QListWidget()
        for fish in self.FDetectedDict.keys():
            listItem = FFishListItem(self, self.FDetectedDict[fish], count)
            self.FList.addItem(listItem.listItem)
            self.FList.setItemWidget(listItem.listItem, listItem.FWdiget)
            listOfFish.append(listItem)
            count += 1

        self.FLayout.addWidget(self.FList, 0,4,5,1)
        return

    def showFish(self, fishNumber, inputDict):
        print("Fish = ", fishNumber)
        return

