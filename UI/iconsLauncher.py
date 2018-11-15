import json
import os

iconsDir = os.path.join("UI","icons")
iconsDirList = os.listdir(iconsDir)
icons = dict()
for i,iconType in enumerate(iconsDirList):
    temp = os.listdir(os.path.join(iconsDir, iconType))
    temp.sort()
    icons[iconType] = temp
def getIcon(name,iconsDir = iconsDir, icons = icons, theme = "black", resolution = 32):
    """function used to get path of icons based on each OS.
    and the give the path of the icon to the caller function.
    
    Arguments:
        name {[string]} -- [name of the icon category, it can take values:
                        `analyze`,
                        `background_subtraction`,
                        `file`,
                        `file_header`,
                        `flip_horizontally`,
                        `flip_vertically`,
                        `frame_header`,
                        `info`,
                        `next`,
                        `play`,
                        `salmon`,
                        `settings_gear`,
                        `show_markers`,
                        `statistics`,
                        `welcome_logos`]
    
    Keyword Arguments:
        iconsDir {string} -- [directory containing the icons] (default: {iconsDir})
        icons {dict} -- [dictionary of all icons directories] (default: {icons})
        theme {str} -- [string that holds the theme of the program, it
                        can take the values:
                        `black`,
                        `white`] (default: {"black"})
        resolution {int} -- [resolution of the icons, it has values:
                        `256`,
                        `128`] (default: {32})
    
    Returns:
        [type] -- [description]
    """

    
    iconName = str(theme) + "_" + str(resolution) + ".png"
    iconPath = os.path.join(iconsDir, icons['name'], icons['name'][4] )
    return iconPath
print(iconsDirList)