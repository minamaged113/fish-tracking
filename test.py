import aris_utils.file_info as file

import aris_utils.error_description as err
import os
import cv2

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
print(x.BEAM_COUNT)
image = x.FRAME_DATA

print(image.shape)
cv2.namedWindow("Frame #1", cv2.WINDOW_NORMAL)
cv2.imshow("Frame #1", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
print(file1.ALL_FRAMES_SIZE)