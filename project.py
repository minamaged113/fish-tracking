import cv2
import os

filesPath = "/home/mghobria/Pictures/SONAR_Images"

imagesList = os.listdir(filesPath)
imagesList.sort()

font = cv2.FONT_HERSHEY_SIMPLEX
fgbg = cv2.createBackgroundSubtractorMOG2()

for count, i in enumerate(imagesList,1):
    # count = 0
    imgPath = os.path.join(filesPath, i)
    img = cv2.imread(imgPath, cv2.IMREAD_GRAYSCALE)
    img = cv2.blur(img, (5,5))
    mask = fgbg.apply(img)
    cv2.putText(mask,str(count),(10,50), font, 1,(255,255,255),2,cv2.LINE_AA)
    cv2.imshow('frame',mask)
    # count = count + 1
    print(count)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break
    


# print(type(imagesList))
# print(imagesList)