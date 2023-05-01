import math
import os
import time
import webbrowser
from pycaw import pycaw
import VolumeControls
import BrightnessControls
# import virtualmouse
import wmi
import ctypes
import cv2
import comtypes
import HandTrackingModule
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import subprocess
import getpass

# volume metrics
devices = pycaw.AudioUtilities.GetSpeakers()
interface = devices.Activate(pycaw.IAudioEndpointVolume._iid_, comtypes.CLSCTX_ALL, None)
volume = ctypes.cast(interface, ctypes.POINTER(pycaw.IAudioEndpointVolume))
volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]
vol = 0
volBar = 400
volPer = 0
chromeFlag = 0
flag = 0

# brightness metrics
minBrightness = 0
maxBrightness = 100

USER_NAME = getpass.getuser()


class HandDetectorClass():
    chromeFlag = 0
    flag = 0
    f = wmi.WMI()

    def __init__(self):
        super(HandDetectorClass, self).__init__()
        self.cap = cv2.VideoCapture(0)
        self.detector = HandTrackingModule.HandDetector(detectionCon=0.8, maxHands=2)
        self.x = 0

    def readVideoFromCamera(self):
        while True:
            self.success, self.img = self.cap.read()
            self.hands, self.img = self.detector.findHands(self.img)
            if self.hands:
                self.InitializeHand()
                try:
                    self.DoActivity(self.x)
                except Exception as e:
                    print(e)
            cv2.imshow("Image", self.img)
            cv2.waitKey(1)

    def InitializeHand(self):
        self.hand1 = self.hands[0]
        self.lmList1 = self.hand1["lmList"]
        self.bbox1 = self.hand1["bbox"]
        self.centerPoint1 = self.hand1["center"]
        self.handType1 = self.hand1["type"]
        self.fingers1 = self.detector.fingersUp(self.hand1)

        if len(self.hands) == 2:
            self.hand2 = self.hands[1]
            self.lmList2 = self.hand2["lmList"]
            self.bbox2 = self.hand2["bbox"]
            self.centerPoint2 = self.hand2["center"]
            self.handType2 = self.hand2["type"]
            self.fingers2 = self.detector.fingersUp(self.hand2)
            try:
                self.length, self.info, self.img = self.detector.findDistance(self.centerPoint1, self.centerPoint2,
                                                                              self.img)
                self.x = int(self.length)
            except Exception as e:
                print("-----------")

        elif len(self.hands) == 1 and self.handType1 == "Left" and self.fingers1 == [1, 1, 0, 0, 0]:
            volobj = VolumeControls
            volobj.VolumeControl(self.lmList1,cv2,self.img,volume)

        elif len(self.hands) == 1 and self.handType1 == "Right" and self.fingers1 == [1,1,0,0,0]:
            brightness = BrightnessControls
            brightness.BrightnessControl(self.lmList1,cv2,self.img)

        elif len(self.hands) == 1 and self.handType1 == "Left" and self.fingers1 == [0,1,1,0,0]:
            flag=0
            print(self.fingers1)
            x1, y1 = self.lmList1[8][1], self.lmList1[8][2]
            x2, y2 = self.lmList1[12][1], self.lmList1[12][2]
            length = math.hypot(x2 - x1, y2 - y1)
            print(length)
            if length>20 and length<90:
                if self.process_exists("Telegram.exe") == False:
                    # self.talk("opening telegram")
                    os.startfile("C:\Telegram Desktop\Telegram.exe")

        elif len(self.hands) == 1 and self.handType1 == "Right" and self.fingers1==[0,1,1,0,0]:
            print(self.fingers1)
            x1, y1 = self.lmList1[8][1], self.lmList1[8][2]
            x2, y2 = self.lmList1[12][1], self.lmList1[8][2]
            length = math.hypot(x2-x1, y2-y1)
            # print(length)
            print(self.process_exists("chrome.exe"))
            if length>20 and length<90 :
                os.system("shutdown /s /t 1")
                # os.system("shutdown /r /t 1")

        elif len(self.hands) == 1 and self.handType1 == "Right" and self.fingers1==[1,1,1,1,1]:
            print(self.fingers1)
            cv2.putText(self.img, str(5), (45, 375), cv2.FONT_HERSHEY_TRIPLEX, 10, (255, 0, 0), 25)
            x1, y1, z1 = self.lmList1[4][1], self.lmList1[8][1], self.lmList1[20][1]
            x2, y2, z2 = self.lmList1[4][2], self.lmList1[8][2], self.lmList1[20][2]
            length = math.hypot(x2-x1, y2-y2, z2-z1)
            print(length)

    def process_exists(self,process_name):
        call = 'TASKLIST', '/FI', 'imagename eq %s' % process_name
        # use buildin check_output right away
        output = subprocess.check_output(call).decode()
        # check in last line for process name
        last_line = output.strip().split('\r\n')[-1]
        # because Fail message could be translated
        return last_line.lower().startswith(process_name.lower())


    def DoActivity(self, x):
        if self.x in range(400, 500, 2):
            self.openWhatsApp()

    def openWhatsApp(self):
        if self.process_exists("Chrome.exe") == False:
            self.talk("Opening Whatsapp")
            webbrowser.open("https://web.whatsapp.com")


obj = HandDetectorClass()
obj.readVideoFromCamera()
