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
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (10,2))

## variables for displaying frames
dummy = 0
k = 30
play = False
desc = False
# maximum number of images
number = max(enumerate(imagesList,1))[0]
imgList = list(enumerate(imagesList,1))
count =1
padding = 30


## variables for object detection
# objectDetected = False
debugMode = True
# trackingEnabled = False
# fr = list()
# differenceImage = None
# thresholdImage = None
# sensitivity = 80

while (True):
    # get image path
    imgPath = os.path.join(filesPath, imgList[count][1]) 
    
    # read the image from disk
    img = cv2.imread(imgPath, cv2.IMREAD_GRAYSCALE)
    
    # Blur the image to help in object detection
    frameBlur = cv2.blur(img, (5,5))

    # apply background subtraction to get moving objects
    # the image produced has the objects and shadows
    # background value #0
    # shadow value #127
    # objects value #255
    mask = fgbg.apply(frameBlur)
    
    # perform morphological operations to visualize objects better
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    # remove shadows
    # function returns tuple, with the image mask as second arg
    mask = cv2.threshold(mask, 128, 255, cv2.THRESH_BINARY)[1]

    # if (debugMode):
        # prev = os.path.join(filesPath, imgList[count-1][1])
        # prevImg = cv2.imread(prev, cv2.IMREAD_GRAYSCALE)
        # differenceImage, thresholdImage = method1(prev, img, 80)
        # cv2.namedWindow("Thresh", cv2.WND_PROP_FULLSCREEN)
        # cv2.imshow("Thresh",thresholdImage)
        # cv2.namedWindow("diff", cv2.WND_PROP_FULLSCREEN)
        # cv2.imshow("diff",differenceImage)
    

    # detecting connected components and labeling
    # ret, labels = cv2.connectedComponents(mask)
    candidatesInfo = cv2.connectedComponentsWithStats(mask)
    
    ret         = candidatesInfo[0] # number of objects
    labels      = candidatesInfo[1] # labeled image
    stats       = candidatesInfo[2] # statistics matrix of each label
    centroids   = candidatesInfo[3] # floating point centroid (x,y) output for each label, including the background label

    if ret == 1:
        count = count + 1
        continue

    label_hue = np.uint8(179*labels/np.max(labels))
    blank_ch = 255*np.ones_like(label_hue)
    labeled_img = cv2.merge([label_hue, blank_ch, blank_ch])
    labeled_img = cv2.cvtColor(labeled_img, cv2.COLOR_HSV2BGR)
    labeled_img[label_hue==0] = 0

    colored_img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR )
    # colored_img = []
    # colored_img.append(img)
    # colored_img.append(img)
    # showing the results stacked next to the original image
    # cv2.putText(mask,str(count),(10,50), font, 1,(255,255,255),2,cv2.LINE_AA)
    # if debugMode:
    for i in range(ret-1):
        # print("Object ",i+1, ": { Center: (",centroids[i+1,0], ",", centroids[i+1,1], ") }." )
        
        x1 = stats[i+1,0]-padding       # left
        y1 = stats[i+1,1]-padding       # top
        x2 = stats[i+1,0] + stats[i+1, 2]+ padding #  left + width
        y2 = stats[i+1,1] + stats[i+1, 3]+ padding
        if x1 < 0:
            x1 = 0
        if y1 < 0:
            y1 = 0
        if x2 > mask.shape[1]:
            x2 = mask.shape[1]
        if y2 > mask.shape[0]:
            y2 = mask.shape[0]

        topLeft = (x1, y1)
        bottomRight = ( x2, y2)

        cv2.rectangle(labeled_img, topLeft, bottomRight, (0,255,0),1)

    cv2.putText(labeled_img,"Objects: "+str(ret-1),(10,100), font, 1,(255,255,255),2,cv2.LINE_AA)
    cv2.putText(labeled_img,str(count),(10,50), font, 1,(255,255,255),2,cv2.LINE_AA)
    cv2.namedWindow("frames and BGS frames", cv2.WND_PROP_FULLSCREEN)
    # cv2.setWindowProperty("frames and BGS frames", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    # cv2.imshow("frames and BGS frames",np.hstack((mask, img)))
    cv2.imshow("frames and BGS frames",np.hstack((labeled_img, colored_img)))

    

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

def method1(prev, current, sensitivity):

    prevBlur = cv2.blur(prev, (5,5))
    frameBlur = cv2.blur(current, (5,5))

    prevMask = fgbg.apply(prevBlur)    
    prevMask = cv2.morphologyEx(prevMask, cv2.MORPH_CLOSE, kernel)
    prevMask = cv2.morphologyEx(prevMask, cv2.MORPH_OPEN, kernel)
    mask = fgbg.apply(frameBlur)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    differenceImage = cv2.absdiff(mask, prevMask)
    _, thresholdImage = cv2.threshold(differenceImage, sensitivity, 255, cv2.THRESH_BINARY)
    thresholdImage = cv2.blur(thresholdImage, (10,10))
    _, thresholdImage = cv2.threshold(thresholdImage, sensitivity, 255, cv2.THRESH_BINARY)

    return differenceImage, thresholdImage