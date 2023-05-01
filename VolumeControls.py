import math
import numpy as np


def VolumeControl(lmList1, cv2, img, volume):
    volRange = volume.GetVolumeRange()
    minVol = volRange[0]
    maxVol = volRange[1]
    vol = 0
    volBar = 400
    volPer = 0
    print("check")
    x1, y1 = lmList1[4][1], lmList1[4][2]
    print(x1, y1)
    x2, y2 = lmList1[8][1], lmList1[8][2]
    cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
    cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
    cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
    cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
    cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

    length = math.hypot(x2 - x1, y2 - y1)
    # print(length)
    # Hand range 50 - 300
    # Volume Range -65 - 0
    vol = np.interp(length, [50, 300], [minVol, maxVol])
    # print(vol)
    volBar = np.interp(length, [50, 300], [400, 150])
    volPer = np.interp(length, [50, 300], [0, 100])
    VOL = "volume is at"+str(f'{int(volPer)} %')
    # self.talk(VOL)
    # print(int(length), vol)
    volume.SetMasterVolumeLevel(vol, None)
    if length < 50:
        cv2.circle(img, (cx, cy), 15, (0, 255, 0), cv2.FILLED)

    cv2.rectangle(img, (50, 150), (85, 400), (255, 0, 0), 3)
    cv2.rectangle(img, (50, int(volBar)), (85, 400), (255, 0, 0), cv2.FILLED)
    cv2.putText(img, f'{int(volPer)} %', (40, 450), cv2.FONT_ITALIC, 1, (255, 0, 0), 3)

