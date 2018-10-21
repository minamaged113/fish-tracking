import cv2
import os
import numpy as np

filesPath = "/home/mghobria/Pictures/SONAR_Images"

imagesList = os.listdir(filesPath)
imagesList.sort()

font = cv2.FONT_HERSHEY_SIMPLEX
threshold = 25
fgbg = cv2.createBackgroundSubtractorMOG2(varThreshold= threshold)
# kernel = np.ones((5,5),np.uint8)
# kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (10,5))
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (4,2))


for count, i in enumerate(imagesList,1):
    # count = 0
    imgPath = os.path.join(filesPath, i)
    img = cv2.imread(imgPath, cv2.IMREAD_GRAYSCALE)
    # frameBlur = cv2.blur(img, (5,5))
    frameBlur = img
    mask = fgbg.apply(frameBlur)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    cv2.putText(mask,str(count),(10,50), font, 1,(255,255,255),2,cv2.LINE_AA)
    cv2.namedWindow("frames and BGS frames", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("frames and BGS frames", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.imshow("frames and BGS frames",np.hstack((mask, img)))
    # count = count + 1
    print(count)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break
    


# print(type(imagesList))
# print(imagesList)