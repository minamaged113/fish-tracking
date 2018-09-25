from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

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
        FInfo.setText("Fisher is an open-source software developed by the University of Oulu, Finland in collaboration with the Natural Resources Institute in Finland.")
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

