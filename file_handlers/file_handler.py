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

def FOpenSonarFile(filename):
    ## TODO : function that opens sonar file
    """
    Opens a sonar file and decides which DIDSON version it is.
    DIDSON version 3: 
    DIDSON version 4: 
    DIDSON version 5 [ARIS]: 
    Then calls the extract images function from each file-type file.
    """

    pass


def c(inpStr):
    """
    Takes a variable type from the cType dictionary and returns
    the number of bytes which that exact variable occupies.
    
    Arguments:
        inpStr {string} -- [string that indicates the type of
                            variable that we need to calculate
                            the size of]
    
    Returns:
        [string] -- [indicates the letter that]

    Reference: https://docs.python.org/3/library/struct.html
    """

    return struct.calcsize(cType[inpStr])


cType = {
    "uint32_t":   "I",
    "float":   "f",
    "int32_t":   "i",
    "uint64_t":   "Q",
    "char[32]":   "32s",
    "char[256]":   "256s",
    "char[568]":   "568s",
    "char[288]": "288s",
    "uint16_t": "H",
    "uint8_t": "B",
    "double": "d"
}
