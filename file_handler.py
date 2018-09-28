"""
Python3 module
provided by the University of Oulu in collaboration with
LUKE-OY. The software is intended to be an open-source.

author: Mina Ghobrial.
date:   May 28th, 2018.

References: 
#   https://github.com/SoundMetrics
#   https://github.com/EminentCodfish/pyARIS
"""

import struct
from file_handlers.utils import *

from file_handlers.v0.v0_file_info import *
from file_handlers.v1.v1_file_info import *
from file_handlers.v2.v2_file_info import *
from file_handlers.v3.v3_file_info import *
from file_handlers.v4.v4_file_info import *
from file_handlers.v5.v5_file_info import *

class FSONAR_File():
    def __init__(self, filename):
        self.FILE_PATH = filename
        self.frameCount = None
        self.BEAM_COUNT = None
        self.largeLens = None
        self.sampleStartDelay = None
        self.soundSpeed = None
        self.samplesPerBeam = None
        self.samplePeriod = None
        self.DATA_SHAPE = None
        self.FRAMES = dict()
        self.version = None



def FOpenSonarFile(filename):
    ## TODO : function that opens sonar file
    """
    Opens a sonar file and decides which DIDSON version it is.
    DIDSON version 0: 0x0464444
    DIDSON version 1: 0x1464444
    DIDSON version 2: 0x2464444
    DIDSON version 3: 0x3464444
    DIDSON version 4: 0x4464444
    DIDSON version 5 [ARIS]: 0x05464444
    Then calls the extract images function from each file-type file.
    """
    # Initializing Class
    SONAR_File = FSONAR_File(filename)
    # versions [Key] = [Value]()
    # all version numbers as Keys
    # all functions to read files as Values
    versions = {
        4604996: lambda: DIDSON_v0(fhand, version, SONAR_File),
        21382212: lambda: DIDSON_v1(fhand, version, SONAR_File),
        38159428: lambda: DIDSON_v2(fhand, version, SONAR_File),
        54936644: lambda: DIDSON_v3(fhand, version, SONAR_File),
        71713860: lambda: DIDSON_v4(fhand, version, SONAR_File),
        88491076: lambda: DIDSON_v5(fhand, version, SONAR_File)
    }
    try:
        fhand = open(filename, 'rb')
        
    except:
        err.print_error(err.fileReadError)
        raise
    # read the first 4 bytes in the file to decide the version
    version = struct.unpack(cType["uint32_t"], fhand.read(c("uint32_t")))[0]
    versions[version]()
    return SONAR_File

def DIDSON_v0(fhand, version, cls):
    """
    This function will handle version 0 DIDSON Files
    """
    ## TODO
    return cls


def DIDSON_v1(fhand, version, cls):
    """
    This function will handle version 1 DIDSON Files
    """
    ## TODO
    pass

def DIDSON_v2(fhand, version, cls):
    """
    This function will handle version 2 DIDSON Files
    """
    ## TODO
    pass

def DIDSON_v3(fhand, version, cls):
    """
    This function will handle version 3 DIDSON Files
    """
    ## TODO
    pass


def DIDSON_v4(fhand, version, cls):
    """
    This function will handle version 4 DIDSON Files
    """
    ## TODO
    pass


def DIDSON_v5(fhand, version, cls):
    """
    This function will handle version 5 DIDSON Files
    version 5 of DIDSON format is also known as ARIS
        dataAndParams = {
            "data": allFrames,
            "parameters":{
                "frameCount": frameCount,
                "numRawBeams" : numRawBeams,
                "samplesPerChannel" : samplesPerChannel,
                "samplePeriod" : samplePeriod,
                "soundSpeed" : soundSpeed,
                "sampleStartDelay" : sampleStartDelay,
                "largeLens" : largeLens,
                "DATA_SHAPE" : data.shape
            }
        }
    """
    print("inside DIDSON v5")
    dataAndParams = v5_getAllFramesData(fhand, version)
    cls.FILE_PATH = fhand.name
    cls.BEAM_COUNT = dataAndParams["parameters"]["numRawBeams"]
    cls.largeLens = dataAndParams["parameters"]["largeLens"]
    cls.sampleStartDelay = dataAndParams["parameters"]["sampleStartDelay"]
    cls.soundSpeed = dataAndParams["parameters"]["soundSpeed"]
    cls.samplesPerBeam = dataAndParams["parameters"]["samplesPerChannel"]
    cls.samplePeriod = dataAndParams["parameters"]["samplePeriod"]
    cls.DATA_SHAPE = dataAndParams["parameters"]["DATA_SHAPE"]
    cls.FRAMES = dataAndParams["data"]
    cls.version = "ARIS"
    cls.frameCount = dataAndParams["parameters"]["frameCount"]
    cls.FRAMES = v5_constructImages(cls)
    return

