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


class ARIS_Frame:

    def __init__(self, filename, frameIndex, frameSize):
        try:
            with open(filename, "rb") as fhand:
                frameoffset = (1024+(frameNumber*(1024+(frameSize))))
                print('inside the frame')
        except:
            err.print_error(err.frameReadError)
            raise
        pass

    def __len__(self):
        pass
