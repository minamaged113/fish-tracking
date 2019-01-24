"""
This module is used to initialize `Help` drop down menu
that is placed in the main menu bar.

Functions used are available in the `UI_utils` module.

Takes an instance of class `QMainWindow` which in this case
is called `FMainContainer`

"""
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from UI.UI_utils import *

def FHelpMenu_init(FMainContainer):
    ## TODO : add signal handler to open webpage
    FMainContainer.aboutAction = QAction("About", FMainContainer)
    FMainContainer.aboutAction.setStatusTip("Opens a webpage contains all info about the project.")
    FMainContainer.aboutAction.triggered.connect(lambda: FMainContainer.print_stat_msg("About pressed"))
    FMainContainer.aboutAction.setEnabled(False)

    ## TODO : add signal handler to check for updates
    FMainContainer.checkForUpdatesAction = QAction("Check for updates", FMainContainer)
    FMainContainer.checkForUpdatesAction.setStatusTip("Check for updates online")
    FMainContainer.checkForUpdatesAction.triggered.connect(lambda: FMainContainer.print_stat_msg("Check for updates pressed."))
    FMainContainer.checkForUpdatesAction.setEnabled(False)

    ## TODO : add signal handler to show license file.
    FMainContainer.viewLicenseAction = QAction("View License", FMainContainer)
    FMainContainer.viewLicenseAction.setStatusTip("Shows the licenses for the whole software.")
    FMainContainer.viewLicenseAction.triggered.connect(lambda: FMainContainer.print_stat_msg("view license pressed."))
    FMainContainer.viewLicenseAction.setEnabled(False)

    ## TODO : add signal handler to report an issue with the software
    FMainContainer.reportAction = QAction("Report Issue", FMainContainer)
    FMainContainer.reportAction.setStatusTip("Report an issue to the developers.")
    FMainContainer.reportAction.triggered.connect(lambda : FMainContainer.print_stat_msg("reprot issure pressed."))
    FMainContainer.reportAction.setEnabled(False)
    
    ## TODO : add signal handler to show statistics
    FMainContainer.showStatisticsAction = QAction("Statistics", FMainContainer)
    FMainContainer.showStatisticsAction.setStatusTip("Shows statistics about old processed files.")
    FMainContainer.showStatisticsAction.triggered.connect(lambda : FMainContainer.print_stat_msg("Statistics pressed."))
    FMainContainer.showStatisticsAction.setEnabled(False)

    FMainContainer.helpMenu = FMainContainer.mainMenu.addMenu("&Help")
    FMainContainer.helpMenu.addAction(FMainContainer.showStatisticsAction)
    FMainContainer.helpMenu.addSeparator()
    FMainContainer.helpMenu.addAction(FMainContainer.reportAction)
    FMainContainer.helpMenu.addAction(FMainContainer.viewLicenseAction)
    FMainContainer.helpMenu.addAction(FMainContainer.checkForUpdatesAction)
    FMainContainer.helpMenu.addSeparator()
    FMainContainer.helpMenu.addAction(FMainContainer.aboutAction)
