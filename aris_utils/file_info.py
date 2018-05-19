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

    def __init__(self,  filename):
        try:
            with open(filename, 'rb') as fhand:
                self.version = struct.unpack(
                    cType["uint32_t"], fhand.read(c("uint32_t")))[0]
                self.frameCount = struct.unpack(
                    cType["uint32_t"], fhand.read(c("uint32_t")))[0]
                self.frameRate = struct.unpack(
                    cType["uint32_t"], fhand.read(c("uint32_t")))[0]
                self.highResolution = struct.unpack(
                    cType["uint32_t"], fhand.read(c("uint32_t")))[0]
                self.numRawBeams = struct.unpack(
                    cType["uint32_t"], fhand.read(c("uint32_t")))[0]
                self.sampleRate = struct.unpack(
                    cType["float"], fhand.read(c("float")))[0]
                self.samplesPerChannel = struct.unpack(
                    cType["uint32_t"], fhand.read(c("uint32_t")))[0]
                self.receiverGain = struct.unpack(
                    cType["uint32_t"], fhand.read(c("uint32_t")))[0]
                self.windowStart = struct.unpack(
                    cType["float"], fhand.read(c("float")))[0]
                self.windowLength = struct.unpack(
                    cType["float"], fhand.read(c("float")))[0]
                self.reverse = struct.unpack(
                    cType["uint32_t"], fhand.read(c("uint32_t")))[0]
                self.serialNumber = struct.unpack(
                    cType["uint32_t"], fhand.read(c("uint32_t")))[0]
                self.strDate = struct.unpack(
                    cType["char[32]"], fhand.read(c("char[32]")))[0]
                self.strHeaderID = struct.unpack(
                    cType["char[256]"], fhand.read(c("char[256]")))[0]
                self.userID1 = struct.unpack(
                    cType["int32_t"], fhand.read(c("int32_t")))[0]
                self.userID2 = struct.unpack(
                    cType["int32_t"], fhand.read(c("int32_t")))[0]
                self.userID3 = struct.unpack(
                    cType["int32_t"], fhand.read(c("int32_t")))[0]
                self.userID4 = struct.unpack(
                    cType["int32_t"], fhand.read(c("int32_t")))[0]
                self.startFrame = struct.unpack(
                    cType["uint32_t"], fhand.read(c("uint32_t")))[0]
                self.endFrame = struct.unpack(
                    cType["uint32_t"], fhand.read(c("uint32_t")))[0]
                self.timelapse = struct.unpack(
                    cType["uint32_t"], fhand.read(c("uint32_t")))[0]
                self.recordInterval = struct.unpack(
                    cType["uint32_t"], fhand.read(c("uint32_t")))[0]
                self.radioSecond = struct.unpack(
                    cType["uint32_t"], fhand.read(c("uint32_t")))[0]
                self.frameInterval = struct.unpack(
                    cType["uint32_t"], fhand.read(c("uint32_t")))[0]
                self.flags = struct.unpack(
                    cType["uint32_t"], fhand.read(c("uint32_t")))[0]
                self.auxFlags = struct.unpack(
                    cType["uint32_t"], fhand.read(c("uint32_t")))[0]
                self.soundVelocity = struct.unpack(
                    cType["uint32_t"], fhand.read(c("uint32_t")))[0]
                self.flags3D = struct.unpack(
                    cType["uint32_t"], fhand.read(c("uint32_t")))[0]
                self.softwareVersion = struct.unpack(
                    cType["uint32_t"], fhand.read(c("uint32_t")))[0]
                self.waterTemp = struct.unpack(
                    cType["uint32_t"], fhand.read(c("uint32_t")))[0]
                self.salinity = struct.unpack(
                    cType["uint32_t"], fhand.read(c("uint32_t")))[0]
                self.pulseLength = struct.unpack(
                    cType["uint32_t"], fhand.read(c("uint32_t")))[0]
                self.TxMode = struct.unpack(
                    cType["uint32_t"], fhand.read(c("uint32_t")))[0]
                self.versionFPGA = struct.unpack(
                    cType["uint32_t"], fhand.read(c("uint32_t")))[0]
                self.versionPSuC = struct.unpack(
                    cType["uint32_t"], fhand.read(c("uint32_t")))[0]
                self.thumbnailFI = struct.unpack(
                    cType["uint32_t"], fhand.read(c("uint32_t")))[0]
                self.fileSize = struct.unpack(
                    cType["uint64_t"], fhand.read(c("uint64_t")))[0]
                self.optionalHeaderSize = struct.unpack(
                    cType["uint64_t"], fhand.read(c("uint64_t")))[0]
                self.optionalTailSize = struct.unpack(
                    cType["uint64_t"], fhand.read(c("uint64_t")))[0]
                self.versionMinor = struct.unpack(
                    cType["uint32_t"], fhand.read(c("uint32_t")))[0]
                self.largeLens = struct.unpack(
                    cType["uint32_t"], fhand.read(c("uint32_t")))[0]

                self.sanityChecks()

        except:
            err.print_error(err.fileReadError)
            raise

    def sanityChecks(self):
        if (self.version == 88491076):
            # check number of frames == self.frameCount
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
    "uint32_t":   "I",
    "float":   "f",
    "int32_t":   "i",
    "uint64_t":   "Q",
    "char[32]":   "32s",
    "char[256]":   "256s",
    "char[568]":   "568s"
}
