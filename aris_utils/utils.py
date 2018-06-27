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

def c(inpStr):
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
    "uint8_t": "B"
}
