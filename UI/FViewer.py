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
from ast import literal_eval

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
        # self.FWdigetLayout.setSizeConstraint(QLayout.SetFixedSize)
        self.FWdiget.setLayout(self.FWdigetLayout)
        self.listItem.setSizeHint(self.FWdiget.sizeHint())


    
class MyFigure(QLabel):
    # isPlaying = False
    __parent = None

    def __init__(self, parent):
        self.__parent = parent
        QLabel.__init__(self, parent)

    def paintEvent(self, paintEvent):
        if isinstance(self.__parent, FViewer):
            fviewer = self.__parent
            if fviewer.play:
                fviewer.FShowNextImage()
            
        QLabel.paintEvent(self, paintEvent)
    
    def mouseMoveEvent(self, event):
        if isinstance(self.__parent, FViewer):
            fviewer = self.__parent
            #print(self.pixmap().width(), self.pixmap().height())
            if self.pixmap():
                marginx = (self.width() - self.pixmap().width()) / 2
                marginy = (self.height() - self.pixmap().height()) / 2
                xs = (event.x() - marginx) / self.pixmap().width()
                ys = (event.y() - marginy) / self.pixmap().height()
                output = fviewer.File.getBeamDistance(xs, ys)
                fviewer.FParent.FStatusBarMousePos.setText("distance={}m\t,y={}deg\t".format(output[0], output[1]))


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
        
        self.FAutoAnalizerBTN = QPushButton(self)        
        self.FAutoAnalizerBTN.setObjectName("Automatic Analyzer")
        self.FAutoAnalizerBTN.setIcon(QIcon(FGetIcon('analyze')))
        self.FAutoAnalizerBTN.clicked.connect(self.FAutoAnalizer)

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

        #self.FFigure = QLabel("Frame Viewer", self)
        #self.FFigure.setUpdatesEnabled(True)
        
        self.MyFigureWidget = MyFigure(self)
        # self.MyFigureWidget.setUpdatesEnabled(True)
        self.MyFigureWidget.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        self.MyFigureWidget.setMouseTracking(True)

        self.FToolbar = QToolBar(self)
        self.FToolbar.addWidget(self.FAutoAnalizerBTN)
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

        self.FLayout.addWidget(self.FToolbar,0,0,3,1)
        self.FLayout.addWidget(self.MyFigureWidget,0,1,1,3)
        self.FLayout.addWidget(self.FSlider,1,1,1,3)
        #self.FLayout.addLayout(self.LowerToolbar, 2,1, Qt.AlignBottom)
        self.FLayout.addWidget(FPreviousBTN, 2,1)
        self.FLayout.addWidget(self.FPlayBTN, 2,2)
        self.FLayout.addWidget(FNextBTN, 2,3)
        
        self.FLayout.setContentsMargins(0,0,0,0)
        self.FLayout.setColumnStretch(0,0)
        self.FLayout.setColumnStretch(1,1)
        self.FLayout.setColumnStretch(2,1)
        self.FLayout.setColumnStretch(3,1)
        self.FLayout.setRowStretch(0,1)
        self.FLayout.setRowStretch(1,0)
        self.FLayout.setRowStretch(2,0)
        self.FLayout.setSizeConstraint(QLayout.SetMinimumSize)

        if self.postAnalysisViewer:
            self.FListDetected()

       
        #self.FDisplayImage()

        self.setLayout(self.FLayout)

    #def UpdateFrameSlider(self):
    #    self.FSlider.setValue(self.UI_FRAME_INDEX)
        
    def FShowNextImage(self):
        """Show the next frame image.
        """
        self.UI_FRAME_INDEX +=1
        if (self.UI_FRAME_INDEX > self.File.frameCount-1):
            self.UI_FRAME_INDEX = 0
        
        self.FSlider.setValue(self.UI_FRAME_INDEX+1)
        #tick1 = time.time()
        #self.FFrames = self.File.getFrame(self.UI_FRAME_INDEX)
        #tick2 = time.time()
        #self.FDisplayImage()
        #tick3 = time.time()
        #print('time to fetch frame = ', tick2-tick1)
        #print('time to show frame = ', tick3-tick2)
        # return

    def FShowPreviousImage(self):
        """Show the previous frame image
        """

        self.UI_FRAME_INDEX -= 1
        if (self.UI_FRAME_INDEX < 0 ):
            self.UI_FRAME_INDEX = self.File.frameCount-1

        self.FSlider.setValue(self.UI_FRAME_INDEX+1)
        #tick1 = time.time()
        #self.FFrames = self.File.getFrame(self.UI_FRAME_INDEX)
        #tick2 = time.time()
        #self.FDisplayImage()
        #tick3 = time.time()
        #print('time to fetch frame = ', tick2-tick1)
        #print('time to show frame = ', tick3-tick2)

    def FDisplayImage(self, ffigure = None):
        if ffigure is None:
            ffigure = self.MyFigureWidget

        ffigure.setUpdatesEnabled(False)
        ffigure.clear()

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

        ffigure.setPixmap(QPixmap.fromImage(img).scaled(ffigure.width(), ffigure.height(), Qt.KeepAspectRatio))
        ffigure.setAlignment(Qt.AlignCenter)
        self.FParent.FStatusBarFrameNumber.setText("Frame : "+str(self.UI_FRAME_INDEX+1)+"/"+str(self.File.frameCount))
        ffigure.setUpdatesEnabled(True)


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
            #self.FDisplayImage()
        else:
            self.subtractBackground = False
            self.F_BGS_Slider.setDisabled(True)
            #self.FDisplayImage()

    def FSliderValueChanged(self, value):
        self.UI_FRAME_INDEX = value - 1
        tick1 = time.time()
        self.FFrames = self.File.getFrame(self.UI_FRAME_INDEX)
        tick2 = time.time()
        self.FDisplayImage()
        tick3 = time.time()
        print('time to fetch frame = ', tick2-tick1)
        print('time to display image = ', tick3-tick2)
        
        #self.FFrames = self.File.getFrame(self.UI_FRAME_INDEX)
        #self.FDisplayImage()

    def F_BGS_SliderValueChanged(self):
        value = self.F_BGS_Slider.value()
        self.fgbg.setVarThreshold(value)

    def FAutoAnalizer(self):
        ## TODO : Documentation
        self.popup = QDialog(self)
        self.popupLayout = QFormLayout()
        # kernel size and shape {default: ellipse, (10,2)}
        self.morphStructLabel = QLabel("Morphological Structuring Element")
        self.morphStruct = QComboBox(self)
        self.morphStruct.addItem("Rectangle")
        self.morphStruct.addItem("Ellipse")
        self.morphStruct.addItem("Cross")
        self.morphStructDim = QLabel("Structuring Element Dimension")
        self.morphStructDimInp = QLineEdit()
        self.morphStructDimInp.setPlaceholderText("(10,2)")
        self.popupLayout.addRow(self.morphStructLabel, self.morphStruct)
        self.popupLayout.addRow(self.morphStructDim, self.morphStructDimInp)
        # start frame {default: 1}
        self.startFrame = QLabel("Start Frame")
        self.startFrameInp = QLineEdit()
        self.startFrameInp.setPlaceholderText("1")
        self.popupLayout.addRow(self.startFrame, self.startFrameInp)
        # blur value {default: (5,5)}
        self.blurVal = QLabel("Blur Value")
        self.blurValInp = QLineEdit()
        self.blurValInp.setPlaceholderText("(5,5)")
        self.popupLayout.addRow(self.blurVal, self.blurValInp)
        # background threshold Value {default: 25}
        self.bgTh = QLabel("Background Threshold")
        self.bgThInp = QLineEdit()
        self.bgThInp.setPlaceholderText("25")
        self.popupLayout.addRow(self.bgTh, self.bgThInp)
        # minimum appearance {default: 30}
        self.maxApp = QLabel("Maximum Appearance")
        self.maxAppInp = QLineEdit()
        self.maxAppInp.setPlaceholderText("30 frames")
        self.popupLayout.addRow(self.maxApp, self.maxAppInp)
        # maximum disappearance {default: 5}
        self.maxDis = QLabel("Maximum Disappearance")
        self.maxDisInp = QLineEdit()
        self.maxDisInp.setPlaceholderText("5 frames")
        self.popupLayout.addRow(self.maxDis, self.maxDisInp)
        # tracker search area {default: 30px}
        self.radiusInput = QLineEdit()
        self.radiusLabel = QLabel("search radius")
        self.radiusInput.setPlaceholderText("default is 30 px")
        self.popupLayout.addRow(self.radiusLabel, self.radiusInput)
        # show images while processing? takes longer time
        self.showImages = QCheckBox("Show images while processing. (takes longer time)")
        self.showImages.setChecked(True)
        self.popupLayout.addRow(self.showImages)
        # accept or use defaults
        self.apply = QPushButton("Apply")
        self.apply.clicked.connect(self.handleAnalyzerInput)
        self.popupLayout.addRow(QLabel(), self.apply)
        self.popup.setLayout(self.popupLayout)
        self.popup.show()
        return

    def handleAnalyzerInput(self):
        ## TODO : function to take input from popup dialog box
        
        # handling kernel shape type from drop down menu 
        kernel = self.morphStruct.currentText()
        
        # handling kernel dimensions
        if self.morphStructDimInp.text() == "":
            kernelDim = None
        else:
            kernelDim = literal_eval(self.morphStructDimInp.text())

        # handling start frame index
        if self.startFrameInp.text() == "":
            startFrame = None
        else:
            startFrame = int(self.startFrameInp.text())

        # handling blur dimensions
        if self.blurValInp.text() == "":
            blurDim = None
        else:
            blurDim = literal_eval(self.blurValInp.text())

        # handling background threshold
        if self.bgThInp.text() == "":
            bgTh = None
        else:
            bgTh = int(self.bgThInp.text())

        # handling minimum appearance
        if self.maxAppInp.text() == "":
            minApp = None
        else:
            minApp = int(self.maxAppInp.text())

        # handling maximum disappearance
        if self.maxDisInp.text() == "" :
            maxDis = None
        else:
            maxDis = int(self.maxDisInp.text())

        # handling radius input
        if self.radiusInput.text() == "":
            searchRadius = None
        else:
            searchRadius = int(self.radiusInput.text())

        # handling show images checkbox
        if self.showImages.isChecked():
            imshow = True
        else:
            imshow = False

        print(kernel, type(kernel))
        print(kernelDim, type(kernelDim))
        print(startFrame, type(startFrame))
        print(blurDim, type(blurDim))
        print(bgTh, type(bgTh))
        print(minApp, type(minApp))
        print(maxDis, type(maxDis))
        print(searchRadius, type(searchRadius))
        print(imshow, type(imshow))

        self.FDetectedDict = project.FAnalyze(self, kernel = kernel, 
                                            kernelDim = kernelDim,
                                            startFrame = startFrame,
                                            blurDim = blurDim,
                                            bgTh= bgTh,
                                            minApp= minApp, 
                                            maxDis = maxDis,
                                            searchRadius= searchRadius,
                                            imshow = imshow)
        if(len(self.FDetectedDict)):
            self.FResultsViewer = FViewer(self.FParent, resultsView= True, results=self.FDetectedDict)
            self.FParent.setCentralWidget(self.FResultsViewer)
        return

    def FPlay(self):
        ## problem
        self.play = not self.play
        if self.play:
            self.FPlayBTN.setIcon(QIcon(FGetIcon('pause')))
            self.FShowNextImage()
            #self.autoPlayTimer.start()
            
            #self.FLayout.addWidget(self.FPlayBTN, 2, 2)
            # while(self.UI_FRAME_INDEX<self.File.frameCount):
            #     self.FShowNextImage()
            #     self.FFigure.repaint()
                
            
            #self.playThread = FPlayThread(self)
            #self.playThread.start()
            #while(checkPlayBTNThread(self).start()):
            #    continue
            #return

            # self.buttonCheckThread = checkPlayBTNThread(self)
            # self.buttonCheckThread.start()
        else: # pause
            self.FPlayBTN.setIcon(QIcon(FGetIcon('play')))
            #self.playThread.stop()
            #self.autoPlayTimer.stop()
            #self.FLayout.addWidget(self.FPlayBTN, 2, 2)
            # time.sleep(0.2)
            
        return

    def FListDetected(self):
        index = 1
        listOfFish = list()
        self.FList = QListWidget()
        for fish in self.FDetectedDict.keys():
            listItem = FFishListItem(self, self.FDetectedDict[fish], index)
            self.FList.addItem(listItem.listItem)
            self.FList.setItemWidget(listItem.listItem, listItem.FWdiget)
            listOfFish.append(listItem)
            index += 1

        self.FShowSelectedBTN = QPushButton("Show Selected")
        self.FShowSelectedBTN.clicked.connect(self.showSelectedFish)
        
        self.FApplyBTN = QPushButton("Apply")
        self.FApplyBTN.clicked.connect(self.FApply)

        self.FLayout.addWidget(self.FShowSelectedBTN, 2, 4)
        self.FLayout.addWidget(self.FApplyBTN, 2, 5)
        self.FLayout.addWidget(self.FList, 0,4,2,2, Qt.AlignRight)
        return

    def showFish(self, fishNumber, inputDict):
        ## TODO
        print("Fish = ", fishNumber)
        return

    def showSelectedFish(self):
        ## TODO
        pass

    def FApply(self):
        ## TODO
        pass