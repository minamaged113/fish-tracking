"""
Python Module for functions that is used by the UI
that is available in all windows

"""
import os
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QPushButton
from UI.FViewer import FViewer
# for the about section in the help menu
import webbrowser
#for exporting results
from jinja2 import Environment, FileSystemLoader
import file_handler as FH
from math import sqrt, cos

def FOpenFile(QT_Dialog):
        ## DEBUG : remove filePathTuple and uncomment filePathTuple
        # homeDirectory = str(Path.home())
        homeDirectory = str(os.path.expanduser("~"))
        # filePathTuple = ('/home/mghobria/Documents/work/data/data.aris',) # laptop
        # filePathTuple = ('data.aris',) # Home PC & windows Laptop
        # filePathTuple = ('/home/mghobria/Documents/work/data/data 1/data.aris',) # work PC
        # filePathTuple = ("C:\\Users\\mghobria\\Downloads\\data.aris",) # Home PC windows
        # filePathTuple = (os.path.join(os.getcwd(), "samples", "sample2_reallife", "data.aris"), ) # Home PC windows
        
        filePathTuple = QFileDialog.getOpenFileName(QT_Dialog,
                                                    "Open File",
                                                    homeDirectory,
                                                    "Sonar Files (*.aris *.ddf)")
        if filePathTuple[0] != "" : 
            # if the user has actually chosen a specific file.
            QT_Dialog.FFilePath = filePathTuple[0]
            QT_Dialog.FCentralScreen = FViewer(QT_Dialog)
            QT_Dialog.setCentralWidget(QT_Dialog.FCentralScreen)
            QT_Dialog.setWindowTitle("Fisher - " + QT_Dialog.FFilePath)


def FSaveFile(dataFilePath):
    dialog = QFileDialog()
    acquiredPath = QFileDialog().getSaveFileName(dialog, "Save File", os.path.dirname(dataFilePath), "JSON File (*.json) ;; TEXT (*.txt)")

    return acquiredPath

def loadTemplate(QT_Dialog, default=False):
    """Loads an analysis template from disk from the following path 
    "/fish-tracking/file_handlers/analysis_presets".
    It calls 'loadJSON()' function from 'file_handler'
    module, which returns a dictionary that has the following keys:
    {
        "morphStruct": {string} -- indicates type of kernel,
        "morphStructDim": {list} -- [{int} -- width, {int} -- height],
        "startFrame": {int} -- frame to start analysis from,
        "blurVal": {list} -- [{int} -- width, {int} -- height],
        "bgTh": {int} -- background threshold,
        "maxApp": {int} -- appearance frames,
        "maxDis": {int} -- disappearance frames,
        "radius": {int} -- search radius,
        "showImages" : {bool} -- whether to show process or not
    }
    
    Arguments:
        QT_Dialog {PyQt5.Widget.QDialog()} -- Pop-up QtDialog to start
                        the analysis.
    
    Keyword Arguments:
        default {bool} -- determines whether to load the default template
                or another predefined template. (default: {False})
    """             
    config = None

    if default:
        # load the default template
        defaultTemplatePath = FH.pathFromList(QT_Dialog._MAIN_CONTAINER._CONFIG["analyzerTemplate"])
        config = FH.loadJSON(defaultTemplatePath)

    else:
        # load a preset from disk
        homeDirectory = str(
            os.path.expanduser(
                FH.pathFromList(
                    QT_Dialog._MAIN_CONTAINER._CONFIG["templatesFolder"]
                )
            )
        )
        filePathTuple = QFileDialog.getOpenFileName(QT_Dialog,
                                                    "Load Template",
                                                    homeDirectory,
                                                    "JSON (*.json)")
        if filePathTuple[0] != "" :
            # if the user has actually chosen a specific file.
            config = FH.loadJSON(filePathTuple[0])
    
    if config:
        # if the file was read successfully
        QT_Dialog.morphStruct.setCurrentText(config['morphStruct'])
        QT_Dialog.morphStructDimInp.setText(
            "({w},{h})".format(
                w=config['morphStructDim'][0],
                h=config['morphStructDim'][1]
            )
        )
        QT_Dialog.startFrameInp.setText(config['startFrame'])
        QT_Dialog.blurValInp.setText(
            "({w},{h})".format(
                w=config['blurVal'][0],
                h=config['blurVal'][1]
            )
        )
        QT_Dialog.bgThInp.setText(config['bgTh'])
        QT_Dialog.maxAppInp.setText(config['maxApp'])
        QT_Dialog.maxDisInp.setText(config['maxDis'])
        QT_Dialog.radiusInput.setText(config['radius'])
        QT_Dialog.showImages.setChecked(config['showImages'])
        QT_Dialog.update()
    return

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
    ## TODO _ : change the non-generic export path
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
    url = "https://minamaged113.github.io/fish-tracking/#"
    return webbrowser.open_new_tab(url)

def exportResult(type, detectedFish, path, cls_FViewer):    
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
    if type == "txt":
        templatesPath = os.path.join( os.getcwd(), "file_handlers","output_templates")
        file_loader = FileSystemLoader(templatesPath)
        env = Environment(loader = file_loader)
        items = []
        textTemp = env.get_template("textTemplate.txt")
        for n in detectedFish.keys():
            an_item = dict(
                # frame is the middle frame from the set frames that the fish was detected
                frame=str(detectedFish[n]["frames"][int(len(detectedFish[n]["frames"])/2)]).rjust(5)+"\t\t",
                dir=str(detectedFish[n]["ID"]).rjust(4)+"\t\t",
                R=str(
                    round(
                        calcDistanceAngle(
                            cls_FViewer,
                            detectedFish[n]["locations"]
                            )[0],
                            2
                        ),
                    ).rjust(4)+"\t\t",
                theta=str(
                    round(
                        calcDistanceAngle(
                            cls_FViewer,
                            detectedFish[n]["locations"]
                            )[1],
                            2
                        ),
                    ).rjust(4)+"\t\t",
                L="{0:.2f}".format(
                    round(
                        getAvgLength(cls_FViewer,
                            detectedFish[n]["left"],
                            detectedFish[n]["width"],
                            detectedFish[n]["top"],
                            detectedFish[n]["height"]
                            ),
                        2
                        )
                    ).rjust(4)+"\t\t",

                dR=str(detectedFish[n]["ID"]).rjust(4)+"\t\t",
                aspect=str(detectedFish[n]["ID"]).rjust(4)+"\t\t",
                time=str(n).rjust(4)+"\t\t",
                date=str(detectedFish[n]["ID"]).rjust(4)+"\t\t",
                speed=str(calcSpeed()).rjust(4)+"\t\t",
                comments=""
                )
            items.append(an_item)

        output = textTemp.render(fishes=items,
            fileName=path,
            totalFish=len(detectedFish),
            editorID="TODO",
            fileDate="TODO",
            startTimeStamp="TODO",
            endTimeStamp="TODO"
            )

        with open(path, 'w') as outFile:
            outFile.write(output)

    elif type == "json":

        for n in detectedFish.keys():
            data[str(n)] = {
                "ID" : detectedFish[n]["ID"],
                "locations" : tuple(map(tuple, detectedFish[n]["locations"])),
                "frames" : detectedFish[n]["frames"],
                "left": list(map(int, detectedFish[n]["left"])),
                "top": list(map(int, detectedFish[n]["top"])),
                "width": list(map(int, detectedFish[n]["width"])),
                "height" : list(map(int, detectedFish[n]["height"])),
                "area": list(map(int, detectedFish[n]["area"]))
            }
                  
        with open(path, 'w') as outFile:
            json.dump(data, outFile)

    else:
        return False

    return True

def loadFrameList():
    """Function that loads frames before and after the current
    Frame into the memory for faster processing.
    Every time the user presses `Next` or `Previous` it modifies
    the list to maintain the number of loaded frames.

        range: {integer} -- defines number of frames loaded into
                the memory.

    """
    ## TODO _
    framesIndices = list()
    range = 10
    if range > (self.File.FRAME_COUNT+1):
        range = self.File.FRAME_COUNT
    for i in range(range):
        framesIndices.append()
        
    pass

def getAvgLength(cls_FViewer, listOfLefts, listOfWidths, listOfTops, listOfHeights):
    ## TODO : this now returns average width in pixels, it should be in 
    ## metric system units
    
    # https://www.easycalculation.com/physics/classical-physics/resultant-vector.php
    # the hypotenus being the length of the fish
    # p1  p2
    # ____
    # |  /
    # | /
    # |/
    # p3
    
    
    lengths = list()
    for i in range(len(listOfLefts)):
        p2 = (listOfLefts[i]+listOfWidths[i], listOfTops[i])        # fish head
        p3 = (listOfLefts[i], listOfTops[i]-listOfHeights[i])       # fish tail

        [L1, a1] = cls_FViewer.File.getBeamDistanceNonScaled(p2[0], p2[1])
        [L2, a2] = cls_FViewer.File.getBeamDistanceNonScaled(p3[0], p3[1])

        R = sqrt(
            (L1**2)
            + (L2**2)
            + (2*L1*L2) * cos(abs(a2-a1))
            )

        lengths.append(R)


    return sum(lengths)/len(lengths)

def calcDistanceAngle(cls_FViewer, listOfCenters):
    medianFrame = int(len(listOfCenters)/2)
    [L, a] = cls_FViewer.File.getBeamDistanceNonScaled(listOfCenters[medianFrame][0], listOfCenters[medianFrame][1])
    return [L, a]

def calcDir():
    ## TODO
    return "TODO"

def calcSpeed():
    ## TODO
    return "TODO"

def errorMessage(error=None, msg=None, details=None):
    msgBox = QMessageBox()
    msgBox.setIcon(QMessageBox.Warning)
    if error:
        msgBox.setWindowTitle(error)
    if msg:
        msgBox.setText(msg)
    if details:
        msgBox.setDetailedText(details)
    msgBox.setStandardButtons(QMessageBox.Ok)
    msgBox.exec()
    return

def FGetSavePath():
    fileDialog = QFileDialog.getSaveFileName()
    return fileSavePath

def print_stat_msg(text):
    ## TODO _ : delete this function
    print(text)