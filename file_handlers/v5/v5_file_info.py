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
import file_handlers.error_description as err
import file_handlers.v5.v5_frame_info as frame
import os
import json
import file_handlers.utils as utils
import file_handlers.beamLookUp as beamLookUp
import numpy as np
import re
from skimage.transform import warp
import cv2




cwd = os.getcwd()
JSON_FILE_PATH = cwd + "/file_handlers/v5/v5_file_headers_info.json"

class v5_File:
    """
    Abstraction of the ARIS file format.

    The following class contains all the tools needed
    to read, write and modify ARIS file formats. It also
    provides tools to export files and data in several
    file formats

    Example:
    >>> file = v5_File("sample.aris")

    Note:
        Naming Convention:
            - header values follow camel case naming convention.
            - calculated file values are in upper case
    """
    # File related calculated variables
    FILE_PATH = None
    FILE_SIZE = None
    FILE_HEADER_SIZE = None
    FILE_HEADER_NUM = 41

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

        
        self.FRAME_SIZE = self.getFrameSize()
        self.FILE_SIZE = self.getFileSize()
        self.FILE_HEADER_SIZE = self.getFileHeaderSize()
        self.ALL_FRAMES_SIZE = self.getAllFramesSize()
        self.sanity = self.sanityChecks()

        
    ##############################################################
    #       Usable user Functions
    ##############################################################

    def __len__(self):
        """
        Returns number of frames inside the file
        """
        return self.frameCount

    def __repr__(self):
        fileName = re.search("/([a-zA-Z0-9]+).aris", self.FILE_PATH)
        return fileName.group(0)
    
    def readFrame(self, frameIndex):
        """This function reads a frame given the frame index
        of that frame and returns a class handle of the read
        frame.
        
        Arguments:
            frameIndex {[integer]} -- [specifies a frame to be read from
                                    a given file]
        
        Returns:
            [class handle] -- [returns a class handle pointing
                                to the data]
        """

        return frame.ARIS_Frame(self.FILE_PATH, frameIndex, self.FRAME_SIZE)

    def getImages(self, QDrogressDialog):
        images = list()
        for frameIndex in range(self.frameCount):
            wholeFrame = frame.ARIS_Frame(self.FILE_PATH, frameIndex, self.FRAME_SIZE)
            images.append(wholeFrame.IMAGE)
            QDrogressDialog.setValue(frameIndex)
        return images

    
    def printFileHeader(self):
    
        try:
            with open(JSON_FILE_PATH) as json_fhand:
                orderedSet = dict()
                file_headers = json_fhand.read()
                data = json.loads(file_headers)
                checkList = data.get("file").keys()
                headerFields = self.__dict__
                for headerField in headerFields:
                    if(headerField in checkList):
                        headerValue = headerField + " = " + str(headerFields[headerField])
                        index = str(data["file"][headerField]["order"])
                        orderedSet[index] = headerValue
                    else:
                        continue
                for i in range(self.FILE_HEADER_NUM):
                    print(orderedSet[str(i)])

        except:
            err.print_error(err.jsonData)
            raise
        return

    def getInfo(self):
        Info = {
            "File Name": self.FILE_PATH,
            "Software Version": self.softwareVersion,
            "ARIS SN": self.serialNumber,
            "File Size": self.FILE_SIZE,
            "Number Of Frames": self.frameCount,
            "Beam Count": self.numRawBeams,
            "Samples per Beam": self.samplesPerChannel
        }
        return Info

    def fileName(self):
        return self.FILE_PATH

    def fileVersion(self):
        return self.sanity

    def exportFrameHeaders(self, format = "JSON", outputFilePath = None):
        if(format == "JSON"):
            print("Exporting JSON file...")

        elif(format == "CSV"):
            print("Exporting CSV file...")
        pass


    # def formImage(self, frameIndex):
    #     output = self.readFrame(frameIndex)
    #     createLUP(self, output)
    #     # self.warpFrame(frameIndex)
    #     remapARIS(self, output)
    #     return

    ##############################################################
    #       Functions called when initializing ARIS File Class
    ##############################################################
    
    def getFrameSize(self):
        """a functione that takes an instant of the class and returns
        an integer containing the frame size in the given file.
        
        Returns:
            [integer] -- [number of beams * number of samples per channel]
        """

        return self.numRawBeams*self.samplesPerChannel

    def getFileSize(self):
        """Returns the file size on disk
        
        Returns:
            [integer] -- [Given file size]
        """

        return os.path.getsize(self.FILE_PATH)

    def getFileHeaderSize(self):
        """Returns the default header size written in the
        `file_headers_info.json`
        
        Returns:
            [integer] -- [Number of bytes that the header occupies]
        """

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
        """Returns the size of all frames with their headers
        
        Returns:
            [integer] -- [bytes that the header file occupy]
        """

        return self.FILE_SIZE - self.FILE_HEADER_SIZE

    def sanityChecks(self):
        """
        Checking for file's sanity.
        
        returns:
            [bool] -- [True if everything working, otherwise False]

        """
        if ((self.version == 88491076)):
            # check number of frames == self.frameCount
            # for i in range(self.frameCount):
            #     x = frame.ARIS_Frame(self.FILE_PATH, i, self.FRAME_SIZE)
            #     if(x.sanityCheck() != True):
            #         return False
            return True
        return False


    def play(self):
        ## TODO
        pass
    

def v5_getAllFramesData(fhand, version, cls):
    """Opens a .aris file and extracts all bytes for all frames and returns a
    list containing all frames data, to be used in drawing the images.
    For images to be drawn from frames, the following attributes are needed
    from this function:
        - SONAR Sample Data     --> `allFrames`
        - Number of Beams [fl]  --> `numRawBeams`
        - Samples Per Beam [fl] --> `samplesPerChannel`
        - Type of Lens  [fr]    --> `largeLens`
        - Sample Start Delay[fr]--> `sampleStartDelay`
        - Sound Velocity[fr]    --> `soundSpeed`
        - Sample Period[fr]     --> `samplePeriod`

    """
    
    ## TODO
    
    cls.version = "ARIS"
    fileAttributesList = ["numRawBeams", "samplesPerChannel", "frameCount"]
    frameAttributesList = ["largeLens", "sampleStartDelay", "soundSpeed", "samplePeriod"]

    fileHeader = utils.getFileHeaderValue(version, fileAttributesList)
    frameHeader = utils.getFrameHeaderValue(version, frameAttributesList)
    print("inside v5_getAllFramesData(fhand)")
    #   Reading Number of frames in the file [from file header]
    fhand.seek(fileHeader["frameCount"]["location"], 0)
    cls.frameCount = struct.unpack(
            utils.cType[fileHeader["frameCount"]["size"]],
            fhand.read(utils.c(fileHeader["frameCount"]["size"])))[0]

    #   Reading number of beams in each frame [from file header]
    fhand.seek(fileHeader["numRawBeams"]["location"], 0)
    cls.BEAM_COUNT = struct.unpack(
            utils.cType[fileHeader["numRawBeams"]["size"]],
            fhand.read(utils.c(fileHeader["numRawBeams"]["size"])))[0]

    #   Reading number of samples in each beam [from file header]
    fhand.seek(fileHeader["samplesPerChannel"]["location"], 0)
    cls.samplesPerBeam = struct.unpack(
            utils.cType[fileHeader["samplesPerChannel"]["size"]],
            fhand.read(utils.c(fileHeader["samplesPerChannel"]["size"])))[0]

    #   Reading Sample Period [from frame header]
    fhand.seek(cls.FILE_HEADER_SIZE + fhand.seek(frameHeader["samplePeriod"]["location"], 0))
    cls.samplePeriod = struct.unpack(
            utils.cType[frameHeader["samplePeriod"]["size"]],
            fhand.read(utils.c(frameHeader["samplePeriod"]["size"])))[0]

    #   Reading Sound Velocity in Water [from frame header]
    fhand.seek(cls.FILE_HEADER_SIZE + fhand.seek(frameHeader["soundSpeed"]["location"], 0))
    cls.soundSpeed = struct.unpack(
            utils.cType[frameHeader["soundSpeed"]["size"]],
            fhand.read(utils.c(frameHeader["soundSpeed"]["size"])))[0]
    
    #   Reading Sample Start Delay [from frame header]
    fhand.seek(cls.FILE_HEADER_SIZE + fhand.seek(frameHeader["sampleStartDelay"]["location"], 0))
    cls.sampleStartDelay = struct.unpack(
            utils.cType[frameHeader["sampleStartDelay"]["size"]],
            fhand.read(utils.c(frameHeader["sampleStartDelay"]["size"])))[0]

    #   Reading availability of large lens [from frame header]
    fhand.seek(cls.FILE_HEADER_SIZE + fhand.seek(frameHeader["largeLens"]["location"], 0))
    cls.largeLens = struct.unpack(
            utils.cType[frameHeader["largeLens"]["size"]],
            fhand.read(utils.c(frameHeader["largeLens"]["size"])))[0]

    frameSize = cls.BEAM_COUNT * cls.samplesPerBeam
    # the first frame data offset from file start is 2048
    frameoffset = 2048
    fhand.seek(frameoffset, 0)
    strCat = frameSize*"B"
    cls.FRAMES = np.array(struct.unpack(strCat, fhand.read(frameSize)), dtype=np.uint8)
    cls.FRAMES = cv2.flip(cls.FRAMES.reshape((cls.samplesPerBeam, cls.BEAM_COUNT)), 0)
    cls.DATA_SHAPE = cls.FRAMES.shape
    cls.windowStart = cls.sampleStartDelay * 0.000001 * cls.soundSpeed/2
    cls.windowLength = cls.samplePeriod * cls.samplesPerBeam * 0.000001 * cls.soundSpeed/2
    cls.firstBeamAngle = beamLookUp.BeamLookUp(cls.BEAM_COUNT, cls.largeLens)[-1]
    cls.FRAMES = cls.constructImages()
    
    return


