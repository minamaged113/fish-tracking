"""
Python Module for functions that is used by the UI
that is available in all windows

"""
import os
from PyQt5.QtWidgets import QFileDialog
from UI.FViewer import FViewer

def FOpenFile(QT_Dialog):
        ## DEBUG : remove filePathTuple and uncomment filePathTuple
        # home = str(Path.home())
        home = str(os.path.expanduser("~"))
        # filePathTuple = ('/home/mghobria/Documents/work/data/data.aris',) # laptop
        # filePathTuple = ('data.aris',) # Home PC & windows Laptop
        # filePathTuple = ('/home/mghobria/Documents/work/data/data 1/data.aris',) # work PC
        # filePathTuple = ("C:\\Users\\mghobria\\Downloads\\data.aris",) # Home PC windows
        filePathTuple = QFileDialog.getOpenFileName(QT_Dialog, "Open File", home, "Sonar Files (*.aris *.ddf)")
        if filePathTuple[0] != "" : 
            QT_Dialog.FFilePath = filePathTuple[0]
            QT_Dialog.FCentralScreen = FViewer(QT_Dialog)
            QT_Dialog.setCentralWidget(QT_Dialog.FCentralScreen)
            QT_Dialog.setWindowTitle("Fisher - " + QT_Dialog.FFilePath)



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


def print_stat_msg(self, text):
    ## TODO : delete this function
    print(text)