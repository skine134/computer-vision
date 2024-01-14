import cv2
import mediapipe as mp
import math
import osascript
from threading import Thread
MAX_VALUE = 320
MIN_VALUE = 40


def normalize(value,min,max,is_percent=False):
    if value>max:
        value = max
    elif value<min:
        value = min
    result = (value-min)/(max-min)
    if is_percent:
        return result * 100
    return result
queue = []
def set_vol(volume):
    try:
        vol = "set volume output volume " + str(volume)
        queue.append(vol)
        return True
    except:
        return False
def os_script_process():
    while True:
        if len(queue)>0:
            script = queue.pop(0)
            osascript.osascript(script)
def main():
    cap = cv2.VideoCapture(0)
    Thread(target=os_script_process).start()
    mp_draw = mp.solutions.drawing_utils
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands()
    # volume.GetMute()
    # volume.GetMasterVolumeLevel()
    # volume.GetVolumeRange()
    # volume.SetMasterVolumeLevel(-20.0,None)
    while True:
        sucess, img = cap.read()
        imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        results = hands.process(imgRGB)
        if results.multi_hand_landmarks:
            for landmarks in results.multi_hand_landmarks:
                h, w, c = img.shape
                mp_draw.draw_landmarks(img,landmarks,mp_hands.HAND_CONNECTIONS)
                start = (0,0)
                end = (0,0)
                start = (int(landmarks.landmark[4].x*w), int(landmarks.landmark[4].y*h))
                end = (int(landmarks.landmark[8].x*w), int(landmarks.landmark[8].y*h))
                center= ((end[0]+start[0])//2,(end[1]+start[1])//2)
                circle_color = (255,0,255)
                normalize_volume = int(normalize(math.hypot(end[0]-start[0],end[1]-start[1]),MIN_VALUE,MAX_VALUE,True))
                if normalize_volume<= 0:
                    circle_color = (0,0,255)
                elif normalize_volume>=100:
                    circle_color = (255,0,0)
                
                set_vol(normalize_volume)
                cv2.line(img,(50,150),(50,150-normalize_volume),(255,255,255),5)
                cv2.putText(img,str(normalize_volume),(50,150+20),cv2.FONT_HERSHEY_PLAIN,2,(255,255,255),2)
                cv2.circle(img,start,15,circle_color,cv2.FILLED)
                cv2.circle(img,end,15,circle_color,cv2.FILLED)
                cv2.circle(img,center,15,circle_color,cv2.FILLED)
                cv2.line(img,start,end,(0,255),3)
        cv2.imshow("image",img)
        cv2.waitKey(1)
if __name__ == "__main__":
    main()
