import cv2
import numpy as np
import time
import math
import osascript
import HandTrackingModule as hm

pTime = 0

cap = cv2.VideoCapture(0)

detector = hm.handDetector(detectionConfi=0.7)

#####################
## for windows pycaw - https://github.com/AndreMiras/pycaw
## for macOs - osascript
#####################

result = osascript.osascript('get volume settings')
#print(result)
#print(type(result))
volInfo = result[1].split(',')
outputVol = volInfo[0].replace('output volume:', '')
print(outputVol)

minVol = 0
maxVol = 100



while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    if len(lmList) != 0:
        #print(lmList[4], lmList[8])

        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cx, cy = (x1+x2)//2, (y1+y2)//2

        cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
        cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

        length = math.hypot(x2-x1, y2-y1)
        #print(length)

        # hand range 50 - 300
        # volume range 0 - 100
        vol = np.interp(length, [50, 300], [minVol, maxVol])
        print(int(length), int(vol))

        target_volume = int(vol)
        vol = "set volume output volume " + str(target_volume)
        osascript.osascript(vol)

        if length < 50:
            cv2.circle(img, (cx, cy), 15, (0, 255, 0), cv2.FILLED)

        cv2.rectangle(img, (50, 150), (85, 400), (0, 255,0), 3)
        cv2.rectangle(img, (50, (int(target_volume))), (85, 400), (0, 255,0), cv2.FILLED)

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (40, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255,0,0), 3)
    cv2.imshow("image", img)
    cv2.waitKey(2)
