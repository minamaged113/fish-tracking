
from aris_utils import file_info as file
# import aris_utils.file_info as file

import aris_utils.error_description as err
import os
import cv2
import json
import numpy as np

cwd = os.getcwd()
# testingFilePath = cwd + "/sample.aris"
testingFilePath = "/home/mghobria/Documents/work/data/data 1/data.aris"
file1 = file.ARIS_File(testingFilePath)
sanity = file1.fileVersion()
if(sanity):
    print("file loaded successfully")
else:
    print("some error happened")

print(json.dumps(file1.getInfo(), indent = 4))
print(file1.__repr__())

frame = file1.readFrame(46)
frame.showImage()
# for i in range(file1.frameCount):
#     frame = file1.readFrame(i)
#     # frame.showImage()
#     ## uncomment the next part to save images on disk
#     image = frame.FRAME_DATA
#     image = np.array(image, dtype= np.uint8)
#     cv2.imwrite("frame_"+ str(i)+ "_data.jpg", image)

