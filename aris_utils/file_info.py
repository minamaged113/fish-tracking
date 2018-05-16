"""
Python3 module
provided by the University of Oulu in collaboration with
LUKE-OY. The software is intended to be an open-source 
version of sound

"""
import struct
import aris_utils.error_description as err
import aris_utils.frame_info as frame 

class ARIS_File:
    const_ARIS_FILE_SIGNATURE = 0x05464444
    version = None              # File format version DDF_05 = 0x05464444
    frameCount = None           # Total frames in a file
    frameRate = None            # Initial recorded framerate
    highResolution = None       # 0: LF, 1: HF

    def __init__(self,  filename):
        try:
            with open(filename, 'rb') as fhand:
                self.version        = struct.unpack(cType["uint32_t"], fhand.read(c("uint32_t")))[0]
                self.frameCount     = struct.unpack(cType["uint32_t"], fhand.read(c("uint32_t")))[0]
                self.frameRate      = struct.unpack(cType["uint32_t"], fhand.read(c("uint32_t")))[0]


                self.sanityChecks()

        except:
            err.print_error(err.fileReadError)
            raise

    def sanityChecks(self):
        if (self.version == 88491076):
            return True
        return False

    def readFileHeader(self, filename):
        pass

    def readFrameHeader(self, filename):
        pass

    def extractData(self, filname):
        pass

    def fileName(self):
        pass

    def fileVersion(self):
        return self.version

def get_beams_from_pingmode(pingmode):
    pingmode = int(pingmode)
    if (pingmode is 1 or pingmode is 2):
        return 48

    elif (pingmode is 3 or pingmode is 4 or pingmode is 5):
        return 96

    elif (pingmode is 6 or pingmode is 7 or pingmode is 8):
        return 64

    elif (pingmode is 9 or pingmode is 10 or pingmode is 11 or pingmode is 12):
        return 128

    else:
        return False

def c(inpStr):
    return struct.calcsize(cType[inpStr])
    
cType = {
    "uint32_t"  :   "I" ,
    "float"     :   "f" ,
    "int32_t"   :   "i" ,
    "uint64_t"  :   "Q" ,
    "char[32]"  :   "32s",
    "char[256]" :   "256s",
}