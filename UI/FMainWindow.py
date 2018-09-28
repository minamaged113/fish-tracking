from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import cv2

## library for reading SONAR files
# SF: SONAR File
import file_handler as SF
from skimage.transform import rescale
import numpy as np


class FMainWindow(QDialog):
    """This class holds the main window which will be used to 
    show the SONAR images, analyze them and edit images.
    
    Arguments:
        QDialog {Class} -- inheriting from QDialog class.
    """
    fgbg = cv2.createBackgroundSubtractorMOG2()
    UI_FRAME_INDEX = 0
    FRAMES_LIST = list()
    SCALE = 3.0/3.0
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
        self.origImage = self.FFrames[int(self.UI_FRAME_INDEX)]
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


    def FLoadSONARFile(self, filePath):
        self.FFilePath = filePath
        # SF: Sonar File Library
        self.File = SF.FOpenSonarFile(filePath)

        self.FFrames = self.File.FRAMES
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
