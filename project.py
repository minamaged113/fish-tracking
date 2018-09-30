import numpy as np
import cv2
import os
import matplotlib.pyplot as plt
from skimage.transform import warp


def v5_constructImages(imagesArray):
    d0 = 2.0
    dm = 10.0
    am = 13.762
    K = 1000
    N, M ,frames = imagesArray.shape

    xm = dm*np.tan(am/180*np.pi)
    L = int(K/(dm-d0) * 2*xm)

    sx = L/(2*xm)
    sa = M/(2*am)
    sd = N/(dm-d0)
    O = sx*d0
    Q = sd*d0

    def invmap(inp):
        xi = inp[:,0]
        yi = inp[:,1]
        xc = (xi - L/2)/sx
        yc = (K + O - yi)/sx
        dc = np.sqrt(xc**2 + yc**2)
        ac = np.arctan(xc / yc)/np.pi*180
        ap = ac*sa
        dp = dc*sd
        a = ap + M/2
        d = N + Q - dp
        outp = np.array((a,d)).T
        return outp

    out = warp(imagesArray, invmap, output_shape=(K, L))
    return  out


imagesPath = "/home/mghobria/Pictures/images_same_size/"

imagesList = os.listdir(imagesPath)
numImages = len(imagesList)
# TODO : check for the next line,  NOT FINISHED YET
imagesArray = cv2.imread(os.path.join(imagesPath, imagesList[0]), cv2.IMREAD_GRAYSCALE)
imagesList.pop(0)
for i in imagesList:
    imgPath = os.path.join(imagesPath, i)

    img = cv2.imread(imgPath, cv2.IMREAD_GRAYSCALE)

    imagesArray = np.dstack((imagesArray,img))

    # cv2.imshow('frame', img)
    # k = cv2.waitKey(0) & 0xff
    # if k == 27:
    #     cv2.destroyAllWindows()

output = v5_constructImages(imagesArray)
print("end")

# framesArray = np.dsplit(output, output.shape[2])
# plt.imshow(np.squeeze(framesArray[frameIndex]))


# cap = cv2.VideoCapture("/home/mghobria/Videos/Pexels Videos 1397052.mp4")

# fgbg = cv2.createBackgroundSubtractorMOG2()

# while(1):
#     ret, frame = cap.read()
    
#     fgmask = fgbg.apply(frame)
    
#     cv2.imshow('frame', fgmask)
#     k = cv2.waitKey(30) & 0xff
#     if k == 27:
#         break
        
# cap.release()
# cv2.destroyAllWindows()
