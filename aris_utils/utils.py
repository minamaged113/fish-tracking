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
    "uint16_t": "H"
}
