import aris_utils.file_info as file

import aris_utils.error_description as err
import os
import cv2
import json
import numpy as np

cwd = os.getcwd()
testingFilePath = cwd + "/sample.aris"

file1 = file.ARIS_File(testingFilePath)
sanity = file1.fileVersion()
if(sanity):
    print("file loaded successfully")
else:
    print("some error happened")

print(json.dumps(file1.getInfo(), indent = 4))
print(file1.__repr__())

# file1.printFileHeader()
# x = file1.formImage(2)
frame = file1.readFrame(1)
print(True if(frame.largeLens) else False)

im = frame.FRAME_DATA
im = np.array(im, dtype=np.uint8) 
im = cv2.flip( im, 0)
im = cv2.flip( im, 1)
height, width = im.shape[:2]
im = cv2.resize(im,(20*width, height), interpolation = cv2.INTER_CUBIC)

cv2.namedWindow('image', cv2.WINDOW_NORMAL)
cv2.imshow('image',im)
cv2.waitKey(0)
cv2.destroyAllWindows()

