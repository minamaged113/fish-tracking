import cv2
import os
import numpy as np
import copy
import json

def main():
    # filesPath = "/home/mghobria/Pictures/SONAR_Images" ## laptop
    filesPath = "C:\\Users\\mghobria\\Downloads\\aris\\F" ## windows home PC

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


    # variables for trakcers:
    tracker = centroidTracker()

    while (True):
    # while (count<100):
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

        candidatesInfo = cv2.connectedComponentsWithStats(mask)
        
        ret         = candidatesInfo[0] - 1 # number of objects
        labels      = candidatesInfo[1] # labeled image
        stats       = np.delete(candidatesInfo[2],0, axis = 0) # statistics matrix of each label (deleting the first row --> backgorund)
        centroids   = np.delete(candidatesInfo[3], 0, axis = 0) # floating point centroid (x,y) output for each label, including the background label

        # if the program can not detect any objects, continue; 
        if ret == 0:
            if (desc):
                count = count - 1
            else:
                count = count + 1
            continue

        fishes = tracker.update(stats, centroids, count)

        label_hue = np.uint8(179*labels/np.max(labels))
        blank_ch = 255*np.ones_like(label_hue)
        labeled_img = cv2.merge([label_hue, blank_ch, blank_ch])
        labeled_img = cv2.cvtColor(labeled_img, cv2.COLOR_HSV2BGR)
        labeled_img[label_hue==0] = 0

        colored_img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR )
        if (bool(fishes['objects'])):
            for fish in fishes['objects'].keys():
                x = int(fishes['objects'][fish].locations[-1][0])
                y = int(fishes['objects'][fish].locations[-1][1])
                center = (x,y)
                # x1 = stats[i,0]-padding       # left
                # y1 = stats[i,1]-padding       # top
                # x2 = stats[i,0] + stats[i, 2]+ padding #  left + width
                # y2 = stats[i,1] + stats[i, 3]+ padding
                # if x1 < 0:
                #     x1 = 0
                # if y1 < 0:
                #     y1 = 0
                # if x2 > mask.shape[1]:
                #     x2 = mask.shape[1]
                # if y2 > mask.shape[0]:
                #     y2 = mask.shape[0]

                # topLeft = (x1, y1)
                # bottomRight = ( x2, y2)

                # cv2.rectangle(labeled_img, topLeft, bottomRight, (0,255,0),1)
                cv2.circle(labeled_img, center, tracker.searchArea, (0,255,0), 1)
        cv2.putText(labeled_img,"Objects: "+str(fishes["objects"].__len__()),(10,100), font, 1,(255,255,255),2,cv2.LINE_AA)
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
    print(tracker.archive)
    print(tracker.objects)
class centroidTracker():
    # number of pixels around centroid to look at
    searchArea = 30
    def __init__(self):
        self.objects = {
            'objects' :{}
        }
        self.psuedoObjects = {
            'objects': {}
        }
        self.archive = {
            'objects': {}
        }

    def update(self, npArrayOfObjects, npArrayOfCentroids, frameIndex):
        #** npArrayOfCentroids [centroids] > array of arrays with float entries 
        # example:
        #   [0:3] :[array([202.42857143,...57142857]), array([268.84, 885.72]), array([262.20689655,...65517241])]
        #   0:array([202.42857143, 462.57142857])
        #   1:array([268.84, 885.72])
        #   2:array([262.20689655, 956.65517241])

        #** npArrayOfObjects [stats]  > array of arrays with float entries 
        # array entries description:
        #   0: The leftmost (x) coordinate which is the inclusive start of the bounding box in the horizontal direction.
        #   1: The topmost (y) coordinate which is the inclusive start of the bounding box in the vertical direction.
        #   2: The horizontal size of the bounding box.
        #   3: The vertical size of the bounding box.
        #   4: The total area (in pixels) of the connected component.
        # example:
        #   [0:3] :[array([197, 462,  12...ype=int32), array([263, 885,  12...ype=int32), array([254, 956,  17...ype=int32)]
        #   0:array([197, 462,  12,   3,  21], dtype=int32)
        #   1:array([263, 885,  12,   3,  25], dtype=int32)
        #   2:array([254, 956,  17,   3,  29], dtype=int32)

        everything = {}
        # looping on all objects to register them as new objects
        for i in range(npArrayOfObjects.shape[0]):
            NNLocation = self.NAN(npArrayOfCentroids[i])
            if not NNLocation:
                newFish = Fish(npArrayOfCentroids[i], frameIndex)
                self.psuedoObjects['objects'][newFish.id] = newFish
            else:
                self.psuedoObjects['objects'][NNLocation].updateInfo(npArrayOfCentroids[i], frameIndex)
        

        self.delete(frameIndex)
        self.archiveObject(frameIndex)

        return self.objects


    def NAN(self, centroid):
        # (N)earest (A)ctive (N)eighbour
        allObjectsLocations = np.array([0,0])
        location = list()
        if (bool(self.psuedoObjects['objects'])):
            for key in self.psuedoObjects['objects'].keys():
                location.append(key)
                objectHandler = self.psuedoObjects['objects'][key]
                allObjectsLocations = np.vstack((allObjectsLocations, objectHandler.getLastLocation()) )
            allObjectsLocations = np.delete(allObjectsLocations, 0, axis=0)
            distances = np.linalg.norm((allObjectsLocations - centroid), axis=1)
            distanceToNN = np.min(distances)
            if (distanceToNN<self.searchArea):
                index = np.argmin(distances)
                # it returns the key of the nearest neighbor in the `self.psuedoObjects['objects']`
                return location[index]
            else:
                return False
        else:
            return False

    def register(self):
        return

    def delete(self, currentFrame):
        copyOfPsuedo = copy.deepcopy(self.psuedoObjects['objects'])
        for fish in copyOfPsuedo.keys():
            fishHandle = self.psuedoObjects['objects'][fish]
            if (len(fishHandle.frames) < fishHandle.minAppear):
                if (np.abs(fishHandle.frames[-1] - currentFrame) > 2*fishHandle.minAppear):
                    del self.psuedoObjects['objects'][fish]
            if (len(fishHandle.frames) > 2*fishHandle.minAppear):
                self.objects['objects'][fish] = self.psuedoObjects['objects'][fish]
        return
    
    def archiveObject(self, currentFrame):
        copyOfObjects = copy.deepcopy(self.objects['objects'])
        for fish in copyOfObjects.keys():
            fishHandle = self.objects['objects'][fish]
            if (np.abs(fishHandle.frames[-1] - currentFrame) > 2*fishHandle.maxDisappear):
                self.archive['objects'][fish] = self.objects['objects'][fish]
                del self.objects['objects'][fish]
        return
    
class Fish():
    ID = 0
    maxDisappear = 5
    minAppear = 30
    
    def __init__(self, centroid, firstFrame):
        # ID given to the fish during first detection
        self.id = Fish.ID
        # Maximum number of frames the fish has to disappear to be deleted from the list
        self.maxDisappear = Fish.maxDisappear
        # Minimum number of frames the fish has to disappear to be added to the list
        self.minAppear = Fish.minAppear

        self.activeToggler = False
        self.locations = list()
        self.locations.append(centroid)
        self.frames = list()
        self.frames.append(firstFrame)
        Fish.ID += 1
        self.attributes = {
            "ID" : self.id,
            "locations": self.locations,
            "framesVisible": self.frames
        }
        return 

    def getLastLocation(self):
        return self.locations[-1]

    def updateInfo(self, centroid = None, currentFrame= None):
        if ( (centroid is not None) and (currentFrame is not None)):
            self.locations.append(centroid)
            self.frames.append(currentFrame)
            self.minAppear -= 1
            return
    



main()