import cv2
import os
import numpy as np

filesPath = "/home/mghobria/Pictures/SONAR_Images"

imagesList = os.listdir(filesPath)
imagesList.sort()

font = cv2.FONT_HERSHEY_SIMPLEX
threshold = 25
fgbg = cv2.createBackgroundSubtractorMOG2()
# kernel = np.ones((5,5),np.uint8)
# kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (10,5))
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (4,2))

## variables for displaying frames
dummy = 0
k = 30
play = False
desc = False
# maximum number of images
number = max(enumerate(imagesList,1))[0]
imgList = list(enumerate(imagesList,1))
count =1


## variables for object detection
objectDetected = False
debugMode = True
trackingEnabled = False
fr = list()
differenceImage = None
thresholdImage = None
sensitivity = 80

while (True):
    prev = os.path.join(filesPath, imgList[count-1][1])
    imgPath = os.path.join(filesPath, imgList[count][1])
    
    prevImg = cv2.imread(prev, cv2.IMREAD_GRAYSCALE)
    img = cv2.imread(imgPath, cv2.IMREAD_GRAYSCALE)
    
    prevBlur = cv2.blur(prevImg, (5,5))
    frameBlur = cv2.blur(img, (5,5))

    prevMask = fgbg.apply(prevBlur)    
    prevMask = cv2.morphologyEx(prevMask, cv2.MORPH_CLOSE, kernel)
    prevMask = cv2.morphologyEx(prevMask, cv2.MORPH_OPEN, kernel)
    mask = fgbg.apply(frameBlur)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    if (debugMode):
        differenceImage = cv2.absdiff(mask, prevMask)
        _, thresholdImage = cv2.threshold(differenceImage, sensitivity, 255, cv2.THRESH_BINARY)
        thresholdImage = cv2.blur(thresholdImage, (10,10))
        _, thresholdImage = cv2.threshold(thresholdImage, sensitivity, 255, cv2.THRESH_BINARY)
        cv2.namedWindow("Thresh", cv2.WND_PROP_FULLSCREEN)
        cv2.imshow("Thresh",thresholdImage)
        cv2.namedWindow("diff", cv2.WND_PROP_FULLSCREEN)
        cv2.imshow("diff",differenceImage)
    


    cv2.putText(mask,str(count),(10,50), font, 1,(255,255,255),2,cv2.LINE_AA)
    cv2.namedWindow("frames and BGS frames", cv2.WND_PROP_FULLSCREEN)
    # cv2.setWindowProperty("frames and BGS frames", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.imshow("frames and BGS frames",np.hstack((mask, img)))

    

    k = cv2.waitKey(30 * play) & 0xff

    if k == 27:
        break
    elif k == 0x53:
        print("right")
        desc = False
        count = count + 1
        continue
    elif k == 0x51:
        print("left")
        desc = True
        count = count - 1
        continue
    # elif k == 0x52:
    #     print("up")
    # elif k == 0x54:
    #     print("down")
    elif k == 0x20:
        print("Pause/Play")
        play = not play
    # elif k!= dummy:
    #     dummy = k
    #     print(hex(k))
    count = count + 1
    # if count > number-1:
    #     count = 

# print(type(imagesList))
# print(imagesList)