"""
Python Module for functions that is used by the UI
that is available in all windows

"""
import os
from PyQt5.QtWidgets import QFileDialog
from FViewer import FViewer                                      # UI/FViewer
# for the about section in the help menu
import webbrowser
#for exporting results
from jinja2 import Environment, FileSystemLoader

def FOpenFile(QT_Dialog):
        ## DEBUG : remove filePathTuple and uncomment filePathTuple
        # home = str(Path.home())
        home = str(os.path.expanduser("~"))
        filePathTuple = ('/home/mghobria/Documents/work/data/data.aris',) # laptop
        # filePathTuple = ('data.aris',) # Home PC & windows Laptop
        # filePathTuple = ('/home/mghobria/Documents/work/data/data 1/data.aris',) # work PC
        # filePathTuple = ("C:\\Users\\mghobria\\Downloads\\data.aris",) # Home PC windows
        #filePathTuple = QFileDialog.getOpenFileName(QT_Dialog, "Open File", home, "Sonar Files (*.aris *.ddf)")
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
    ## TODO : change the non-generic export path
    ## allow the user to enter their specific paths.
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

def lukeInfo():
    """Opens a new tab in the default webbrowser to show LUKE homepage.
    """
    url = "https://www.luke.fi/en/"
    return webbrowser.open_new_tab(url)

def uniOuluInfo():
    """Opens a new tab in the default webbrowser to show University
    of Oulu homepage.
    """
    url = "https://www.oulu.fi/university/"
    return webbrowser.open_new_tab(url)

def fisherInfo():
    """Opens a new tab in the default webbrowser to show project's
    homepage.
    """
    url = "https://github.com/minamaged113"
    return webbrowser.open_new_tab(url)

def exportResult(type, detectedFish):    
    """Function used to export results of the program to well-known
    file formats {CSV, JSON, TXT}, according to the choice of the user.
    
    Keyword Arguments:
        type {string} -- The specified output format chosen by the user.
                         it has 3 values {CSV, JSON, TXT}.
                         CSV: Comma-Separated Value,
                         JSON: JavaScript Object Notation,
                         TXT: text.
        detectedFish {list} -- Ouput of the analysis process.
    """
    templatesPath = os.path.join( os.getcwd(), "file_handlers","output_templates")
    file_loader = FileSystemLoader(templatesPath)
    env = Environment(loader = file_loader)
    items = []
    textTemp = env.get_template("textTemplate.txt")
    for i in range(10):
        an_item = dict(frame=i, dir=i, R=i, theta=i, L=i, dR=i, aspect=i, time=i, date=i, speed=i, comments="")
        items.append(an_item)

    output = textTemp.render(fishes=items)
    
    return


def print_stat_msg(text):
    ## TODO : delete this function
    print(text)