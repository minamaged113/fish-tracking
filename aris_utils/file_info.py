"""
Python3 module
provided by the University of Oulu in collaboration with
LUKE-OY. The software is intended to be an open-source.

author: Mina Ghobrial.
date:   April 19th, 2018.

References: 
#   https://github.com/SoundMetrics
#   https://github.com/EminentCodfish/pyARIS

"""
import struct
import aris_utils.error_description as err
import aris_utils.frame_info as frame
import os
import json
import aris_utils.utils as utils

cwd = os.getcwd()
JSON_FILE_PATH = cwd + "/aris_utils/file_headers_info.json"

class ARIS_File:
    """
    Abstraction of the ARIS file format.

    The following class contains all the tools needed
    to read, write and modify ARIS file formats. It also
    provides tools to export files and data in several
    file formats

    Example:
    >>> file = ARIS_File("sample.aris")

    Note:
        Naming Convention:
            - header values follow camel case naming convention.
            - calculated file values are in upper case
    """
    # File related calculated variables
    FILE_PATH = None
    FILE_SIZE = None
    FILE_HEADER_SIZE = None

    # Sanity check variable
    sanity = None
    
    # Frame related calculated variables
    FRAME_SIZE = None
    ALL_FRAMES_SIZE = None
    FRAME_COUNT = None

    # ARIS File class initializer
    def __init__(self,  filename):
        try:
            with open(filename, 'rb') as fhand:
                self.FILE_PATH = filename
                self.version = struct.unpack(
                    utils.cType["uint32_t"], fhand.read(utils.c("uint32_t")))[0]
                self.frameCount = struct.unpack(
                    utils.cType["uint32_t"], fhand.read(utils.c("uint32_t")))[0]
                self.frameRate = struct.unpack(
                    utils.cType["uint32_t"], fhand.read(utils.c("uint32_t")))[0]
                self.highResolution = struct.unpack(
                    utils.cType["uint32_t"], fhand.read(utils.c("uint32_t")))[0]
                self.numRawBeams = struct.unpack(
                    utils.cType["uint32_t"], fhand.read(utils.c("uint32_t")))[0]
                self.sampleRate = struct.unpack(
                    utils.cType["float"], fhand.read(utils.c("float")))[0]
                self.samplesPerChannel = struct.unpack(
                    utils.cType["uint32_t"], fhand.read(utils.c("uint32_t")))[0]
                self.receiverGain = struct.unpack(
                    utils.cType["uint32_t"], fhand.read(utils.c("uint32_t")))[0]
                self.windowStart = struct.unpack(
                    utils.cType["float"], fhand.read(utils.c("float")))[0]
                self.windowLength = struct.unpack(
                    utils.cType["float"], fhand.read(utils.c("float")))[0]
                self.reverse = struct.unpack(
                    utils.cType["uint32_t"], fhand.read(utils.c("uint32_t")))[0]
                self.serialNumber = struct.unpack(
                    utils.cType["uint32_t"], fhand.read(utils.c("uint32_t")))[0]
                self.strDate = struct.unpack(
                    utils.cType["char[32]"], fhand.read(utils.c("char[32]")))[0]
                self.strHeaderID = struct.unpack(
                    utils.cType["char[256]"], fhand.read(utils.c("char[256]")))[0]
                self.userID1 = struct.unpack(
                    utils.cType["int32_t"], fhand.read(utils.c("int32_t")))[0]
                self.userID2 = struct.unpack(
                    utils.cType["int32_t"], fhand.read(utils.c("int32_t")))[0]
                self.userID3 = struct.unpack(
                    utils.cType["int32_t"], fhand.read(utils.c("int32_t")))[0]
                self.userID4 = struct.unpack(
                    utils.cType["int32_t"], fhand.read(utils.c("int32_t")))[0]
                self.startFrame = struct.unpack(
                    utils.cType["uint32_t"], fhand.read(utils.c("uint32_t")))[0]
                self.endFrame = struct.unpack(
                    utils.cType["uint32_t"], fhand.read(utils.c("uint32_t")))[0]
                self.timelapse = struct.unpack(
                    utils.cType["uint32_t"], fhand.read(utils.c("uint32_t")))[0]
                self.recordInterval = struct.unpack(
                    utils.cType["uint32_t"], fhand.read(utils.c("uint32_t")))[0]
                self.radioSecond = struct.unpack(
                    utils.cType["uint32_t"], fhand.read(utils.c("uint32_t")))[0]
                self.frameInterval = struct.unpack(
                    utils.cType["uint32_t"], fhand.read(utils.c("uint32_t")))[0]
                self.flags = struct.unpack(
                    utils.cType["uint32_t"], fhand.read(utils.c("uint32_t")))[0]
                self.auxFlags = struct.unpack(
                    utils.cType["uint32_t"], fhand.read(utils.c("uint32_t")))[0]
                self.soundVelocity = struct.unpack(
                    utils.cType["uint32_t"], fhand.read(utils.c("uint32_t")))[0]
                self.flags3D = struct.unpack(
                    utils.cType["uint32_t"], fhand.read(utils.c("uint32_t")))[0]
                self.softwareVersion = struct.unpack(
                    utils.cType["uint32_t"], fhand.read(utils.c("uint32_t")))[0]
                self.waterTemp = struct.unpack(
                    utils.cType["uint32_t"], fhand.read(utils.c("uint32_t")))[0]
                self.salinity = struct.unpack(
                    utils.cType["uint32_t"], fhand.read(utils.c("uint32_t")))[0]
                self.pulseLength = struct.unpack(
                    utils.cType["uint32_t"], fhand.read(utils.c("uint32_t")))[0]
                self.TxMode = struct.unpack(
                    utils.cType["uint32_t"], fhand.read(utils.c("uint32_t")))[0]
                self.versionFPGA = struct.unpack(
                    utils.cType["uint32_t"], fhand.read(utils.c("uint32_t")))[0]
                self.versionPSuC = struct.unpack(
                    utils.cType["uint32_t"], fhand.read(utils.c("uint32_t")))[0]
                self.thumbnailFI = struct.unpack(
                    utils.cType["uint32_t"], fhand.read(utils.c("uint32_t")))[0]
                self.fileSize = struct.unpack(
                    utils.cType["uint64_t"], fhand.read(utils.c("uint64_t")))[0]
                self.optionalHeaderSize = struct.unpack(
                    utils.cType["uint64_t"], fhand.read(utils.c("uint64_t")))[0]
                self.optionalTailSize = struct.unpack(
                    utils.cType["uint64_t"], fhand.read(utils.c("uint64_t")))[0]
                self.versionMinor = struct.unpack(
                    utils.cType["uint32_t"], fhand.read(utils.c("uint32_t")))[0]
                self.largeLens = struct.unpack(
                    utils.cType["uint32_t"], fhand.read(utils.c("uint32_t")))[0]

        except:
            err.print_error(err.fileReadError)
            raise

        self.sanity = self.sanityChecks()
        self.FRAME_SIZE = self.getFrameSize()
        self.FILE_SIZE = self.getFileSize()
        self.FILE_HEADER_SIZE = self.getFileHeaderSize()
        self.ALL_FRAMES_SIZE = self.getAllFramesSize()

    def __len__(self):
        """
        Returns number of frames inside the file
        """
        return self.frameCount

    def sanityChecks(self):
        """
        Checking for file's sanity.
        
        returns:
            {bool} -- True if everything working, otherwise False

        """
        if ((self.version == 88491076) and (os.path.getsize(self.FILE_PATH) == self.fileSize)):
            # check number of frames == self.frameCount
            return True
        return False

    def printFileHeader(self):
        """
        Reads all file headers and displays them in non-ordered fashion.
        This function depends on "file_headers_info.json" file.
        """
        try:
            with open(JSON_FILE_PATH) as json_fhand:
                file_headers = json_fhand.read()
                data = json.loads(file_headers)
                headerFields = data.get('file').keys()

                for headerField in headerFields:
                    temp = data['file'][headerField]['title']
                    temp = str(temp) + " ="
                    exec("print(temp, self.%s)" % (headerField))
        except:
            err.print_error(err.jsonData)
            raise
        return

    def readFrame(self, frameIndex):
        frameData = frame.ARIS_Frame(self.FILE_PATH, frameIndex, self.FRAME_SIZE)
        return

    def extractData(self, frameIndex):
        pass

    def fileName(self):
        pass

    def fileVersion(self):
        return self.sanity

    def getFrameSize(self):
        return self.numRawBeams*self.samplesPerChannel

    def getFileSize(self):
        return os.path.getsize(self.FILE_PATH)

    def getFileHeaderSize(self):
        size = int()
        try:
            with open(JSON_FILE_PATH) as json_fhand:
                file_headers = json_fhand.read()
                data = json.loads(file_headers)
                size = data['headerSize']['size']
        except:
            err.print_error(err.jsonData)
            raise
        return size

    def getAllFramesSize(self):
        return self.FILE_SIZE - self.FILE_HEADER_SIZE



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
