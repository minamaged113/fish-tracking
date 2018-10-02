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
        self.FRAMES = None
        self.version = None
        self.FILE_HANDLE = None
        self.FRAME_HEADER_SIZE = None
        self.FILE_HEADER_SIZE = None

    def getFrame(self, FI):
        
        frameSize = self.DATA_SHAPE[0] * self.DATA_SHAPE[1]
        frameoffset = (self.FILE_HEADER_SIZE + self.FRAME_HEADER_SIZE +(FI*(self.FRAME_HEADER_SIZE+(frameSize))))
        self.FILE_HANDLE.seek(frameoffset, 0)
        strCat = frameSize*"B"
        self.FRAMES = np.array(struct.unpack(strCat, self.FILE_HANDLE.read(frameSize)), dtype=np.uint8)
        self.FRAMES = cv2.flip(self.FRAMES.reshape((self.DATA_SHAPE[0], self.DATA_SHAPE[1])), 0)
        self.FRAMES = self.constructImages()
        return self.FRAMES

    def constructImages(self):
        
        allAngles = beamLookUp.BeamLookUp(self.BEAM_COUNT, self.largeLens)
        
        d0 = self.sampleStartDelay * 0.000001 * self.soundSpeed/2
        dm = d0 + self.samplePeriod * self.samplesPerBeam * 0.000001 * self.soundSpeed/2
        am = allAngles[-1]
        K = self.samplesPerBeam
        N, M = self.DATA_SHAPE

        xm = dm*np.tan(am/180*np.pi)
        L = int(K/(dm-d0) * 2*xm)

        sx = L/(2*xm)
        sa = M/(2*am)
        sd = N/(dm-d0)
        O = sx*d0
        Q = sd*d0

        def invmap(inp):
            xi = inp[:,0]
            yi = inp[:,1]
            xc = (xi - L/2)/sx
            yc = (K + O - yi)/sx
            dc = np.sqrt(xc**2 + yc**2)
            ac = np.arctan(xc / yc)/np.pi*180
            ap = ac*sa
            dp = dc*sd
            a = ap + M/2
            d = N + Q - dp
            outp = np.array((a,d)).T
            return outp
        


        out = warp( self.FRAMES, invmap, output_shape=(K, L))
        out = (out/np.amax(out)*255).astype(np.uint8)
        return out


def FOpenSonarFile(filename):
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
    print("inside DIDSON v4")
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
    v5_getAllFramesData(fhand, version, cls)
    cls.FILE_PATH = fhand.name
    cls.FILE_HANDLE = fhand
    cls.FRAME_HEADER_SIZE = 1024
    cls.FILE_HEADER_SIZE = 1024
    return

