import math
import numpy as np
import wmi

def BrightnessControl(lmList1, cv2, img):
    minBrightness = 0
    maxBrightness = 100
    x11, y11 = lmList1[4][1], lmList1[4][2]
    x22, y22 = lmList1[8][1], lmList1[8][2]
    cx1, cy1 = (x11 + x22) // 2, (y11 + y22) // 2
    cv2.circle(img, (x11, y11), 15, (255, 0, 255), cv2.FILLED)
    cv2.circle(img, (x22, y22), 15, (255, 0, 255), cv2.FILLED)
    cv2.line(img, (x11, y11), (x22, y22), (255, 0, 255), 3)
    cv2.circle(img, (cx1, cy1), 15, (255, 0, 255), cv2.FILLED)
    length = math.hypot(x22 - x11, y22 - y11)
    brightness = np.interp(length, [50, 300], [minBrightness, maxBrightness])
    c = wmi.WMI(namespace='wmi')
    methods = c.WmiMonitorBrightnessMethods()[0]
    methods.WmiSetBrightness(brightness, 0)
    # print(int(brightness))
    BrightnessBar = np.interp(length, [50, 300], [400, 150])
    # Brightness = "Brightness is at" + str(f'{int(brightness)} %')
    # self.talk(Brightness)
    cv2.rectangle(img, (50, 150), (85, 400), (255, 0, 0), 3)
    cv2.rectangle(img, (50, int(BrightnessBar)), (85, 400), (255, 0, 0), cv2.FILLED)
    cv2.putText(img, f'{int(brightness)} %', (40, 450), cv2.FONT_ITALIC, 1, (255, 0, 0), 3)
