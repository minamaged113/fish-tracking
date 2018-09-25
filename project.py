import struct
from file_handlers.file_handler import *
import os

filename = "/home/mghobria/Documents/work/Tornionjoki/2018-06-24_000000.ddf"
fileSize = os.path.getsize(filename)
fhand = open(filename, 'rb')
version = struct.unpack(
                    cType["uint32_t"], fhand.read(c("uint32_t")))[0]

print('File version: ', hex(version))
print('File size: ', fileSize, ' Bytes')

FILE_HEADER_SIZE = 512
FRAME_HEADER_SIZE = 256

fhand.seek(16, 0)

numRawBeams = struct.unpack(
                    cType["uint32_t"], fhand.read(c("uint32_t")))[0]

fhand.seek(24, 0)

samplePerBeam = struct.unpack(
                    cType["uint32_t"], fhand.read(c("uint32_t")))[0]

print("Frame Dimensions: ", numRawBeams ," x ", samplePerBeam)

frameSize = numRawBeams*samplePerBeam

frameCount = (fileSize - FILE_HEADER_SIZE) / (FRAME_HEADER_SIZE + frameSize)

print("Number of frames in file = ", frameCount)

for i in range(512):
    if i<4:
        continue

    fhand.seek(i,0)
    data = struct.unpack(
                    cType["uint32_t"], fhand.read(c("uint32_t")))[0]

    if data == 11663:
        print(i)
