import aris_utils.file_info as file

import aris_utils.error_description as err
import os
import cv2
import json

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
x = file1.readFrame(1)
# image = x.FRAME_DATA

# print(image.shape)
# cv2.namedWindow("Frame #1", cv2.WINDOW_NORMAL)
# cv2.imshow("Frame #1", image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
# print(file1.ALL_FRAMES_SIZE)
print(x.__repr__())
q = x.getInfo()
x.constructImage()
print(json.dumps(x.imageParamaters, indent=4))
print(json.dumps(q, indent=4))