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

##########################################################
#       UI elements
##########################################################


class FMainWindow(QDialog):
    FRAME_INDEX = 0
    def __init__(self):
        ##  Reading the file
        self.FLoadARISFile()

        QDialog.__init__(self)
        self.FLayout = QGridLayout()

        FNextBTN = QPushButton("Next",self)
        FNextBTN.clicked.connect(self.FShowNextImage)
        FPreviousBTN = QPushButton("Previous",self)
        FPreviousBTN.clicked.connect(self.FShowPreviousImage)

        self.FLayout.addWidget(FNextBTN,1,1)
        self.FLayout.addWidget(FPreviousBTN,1,0)

        self.Frame = self.File.readFrame(self.FRAME_INDEX)
        plt.imsave("temp.jpg",self.Frame.IMAGE, cmap = 'gray')
        self.im = QImage("temp.jpg")
        self.imageLabel = QLabel()
        self.imageLabel.setPixmap(QPixmap.fromImage(self.im))
        self.FLayout.addWidget(self.imageLabel,0,0,1,2, Qt.AlignCenter)

        self.setLayout(self.FLayout)

    def FShowNextImage(self):
        self.imagePath = "/home/mghobria/Pictures/Screenshot from 2018-05-17 00-34-44.png"
        self.im = QImage(self.imagePath)
        self.imageLabel = QLabel()
        self.pixmap = QPixmap.fromImage(self.im)
        self.pixmap = self.pixmap.scaledToWidth(64)
        self.imageLabel.setPixmap(self.pixmap)
        self.FLayout.addWidget(self.imageLabel,0,0,1,2, Qt.AlignCenter)


    def FShowPreviousImage(self):
        self.imagePath = "/home/mghobria/Pictures/Figure_1.png"
        self.im = QImage(self.imagePath)
        self.imageLabel = QLabel()
        self.imageLabel.setPixmap(QPixmap.fromImage(self.im))
        self.FLayout.addWidget(self.imageLabel,0,0,1,2, Qt.AlignCenter)

    def FLoadARISFile(self):
        self.FFilePath = "/home/mghobria/Documents/work/data/data 1/data.aris"
        self.File = ARIS_File.ARIS_File(self.FFilePath)
        sanity = self.File.fileVersion()
        if(sanity):
            print("file loaded successfully")
        else:
            print("some error happened")

        print(json.dumps(self.File.getInfo(), indent = 4))
        print(self.File.__repr__())

        # frame = file1.readFrame(46)
        # frame.showImage()
        # for i in range(file1.frameCount):
        #     frame = file1.readFrame(i)
        #     # frame.showImage()
        #     ## uncomment the next part to save images on disk
        #     image = frame.FRAME_DATA
        #     image = np.array(image, dtype= np.uint8)
        #     cv2.imwrite("frame_"+ str(i)+ "_data.jpg", image)



cwd = os.getcwd()
app = QApplication(sys.argv)
MainWindow = FMainWindow()
MainWindow.show()
app.exec_()

# # FFilePath = cwd + "/sample.aris"
# self.FFilePath = "/home/mghobria/Documents/work/data/data 1/data.aris"
# file1 = file.ARIS_File(FFilePath)
# sanity = file1.fileVersion()
# if(sanity):
#     print("file loaded successfully")
# else:
#     print("some error happened")

# print(json.dumps(file1.getInfo(), indent = 4))
# print(file1.__repr__())

# frame = file1.readFrame(46)
# frame.showImage()
# # for i in range(file1.frameCount):
# #     frame = file1.readFrame(i)
# #     # frame.showImage()
# #     ## uncomment the next part to save images on disk
# #     image = frame.FRAME_DATA
# #     image = np.array(image, dtype= np.uint8)
# #     cv2.imwrite("frame_"+ str(i)+ "_data.jpg", image)

