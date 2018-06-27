import aris_utils.file_info as file

import aris_utils.error_description as err
import os

cwd = os.getcwd()
testingFilePath = cwd + "/sample.aris"

file1 = file.ARIS_File(testingFilePath)
sanity = file1.fileVersion()
if(sanity):
    print("file loaded successfully")
else:
    print("some error happened")

# file1.printFileHeader()
x = file1.readFrame(2)
print(x.pingMode)
print(file1.ALL_FRAMES_SIZE)