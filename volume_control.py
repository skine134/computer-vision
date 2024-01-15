import math
import cv2
import osascript
import time
from threading import Thread
from hand_tracking import hand_tracking
MAX_VALUE = 320
MIN_VALUE = 40

class volume_control:
    def __init__(self):
        self.ht = hand_tracking()
        self.volume_thread = Thread(target=self.__volume_thread).start()
        self.queue = []
        self.volume = None
    def __enque_volume_range(self,volume):
        try:
            vol = "set volume output volume " + str(volume)
            self.queue.append(vol)
            return True
        except:
            return False
    def __volume_thread(self):
        while True:
            if len(self.queue)>0:
                script = self.queue.pop(0)
                osascript.osascript(script)
            time.sleep(10)
        
    def set_sound(self,img,min_color=(0,0,255),max_color=(255,0,0),default_color=(255,0,0)):
        start = (0,0)
        end = (0,0)
        self.ht.find_hand(img)
        landmarks = self.ht.find_position(img)
        if len(landmarks)<=0:
            return
        start = (landmarks[4][1], landmarks[4][2])
        end = (landmarks[8][1], landmarks[8][2])
        center= ((end[0]+start[0])//2,(end[1]+start[1])//2)
        circle_color = default_color
        normalize_volume = int(self.normalize(math.hypot(end[0]-start[0],end[1]-start[1]),MIN_VALUE,MAX_VALUE,is_percent=True))
        if normalize_volume<= 0:
            circle_color = min_color
        elif normalize_volume>=100:
            circle_color = max_color
        self.__enque_volume_range(normalize_volume)
        self.volume = normalize_volume

        # draw volume bar
        cv2.line(img,(50,150),(50,150-normalize_volume),(255,255,255),5)
        cv2.putText(img,str(normalize_volume),(50,150+20),cv2.FONT_HERSHEY_PLAIN,2,(255,255,255),2)

        # draw line with finger
        cv2.circle(img,start,15,circle_color,cv2.FILLED)
        cv2.circle(img,end,15,circle_color,cv2.FILLED)
        cv2.circle(img,center,15,circle_color,cv2.FILLED)
        cv2.line(img,start,end,(0,255),3)



    def normalize(self,value,min,max,is_percent=False):
        if value>max:
            value = max
        elif value<min:
            value = min
        result = (value-min)/(max-min)
        if is_percent:
            return result * 100
        return result
