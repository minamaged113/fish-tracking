"""
Python3 module
provided by the University of Oulu in collaboration with
LUKE-OY. The software is intended to be an open-source 
version of sound

"""


class ARIS_File:
    const_ARIS_FILE_SIGNATURE = 0x05464444

    def __init__(self,  filename):
        pass

    def readFileHeader(self, filename):
        pass

    def readFrameHeader(self, filename):
        pass

    def extractData(self, filname):
        pass

    def fileName(self):
        pass


class ARIS_Frame:
    const_ARIS_FRAME_SIGNATURE = 0x05464444
    filename = None
    def __init__(self, filename, frameNumber):
        pass


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

print(help(ARIS_File))
print(help(ARIS_Frame))