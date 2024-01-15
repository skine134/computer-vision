import cv2
import time
import math
from body_pose import BodyPose
MIN_ANGLE=15
MAX_ANGLE=170
class PersonalTrainer:
    
    def __init__(self):
        self.bp = BodyPose()
        self.count_flag = True
        self.count = 0
    
    def __normalize(self,value,min_angle=MIN_ANGLE,max_angle=MAX_ANGLE,is_percent=False):
        result = (max_angle - value)/(max_angle-min_angle)
        if result > 1:
            result = 1
        if result < 0:
            result = 0
        if is_percent:
            result = int(result*100)
        return result

    def reset(self):
        self.count = 0
    
    def arm_training(self,img,draw=True):
        # right left
        #  12    11
        #  14    13
        #  16    15
        img = self.bp.find_pose(img)
        lm_list = self.bp.find_position(img)
        if len(lm_list)<=0:
            return img
        
        # 15<= angle <= 170
        angle = self.bp.find_angle(img,11,13,15,draw=draw)
        percent = self.__normalize(angle,is_percent=True)

        if self.count_flag and percent>=100:
            self.count = self.count+1
            self.count_flag = False

        if percent<=0:
            self.count_flag = True
            
        if draw:
            cv2.rectangle(img,(50,100),(100,300),(255,0,255),2)
            cv2.rectangle(img,(100,300),(50,300-2*percent),(255,0,255),cv2.FILLED)
            cv2.putText(img,f'{percent}%',(100,300-2*percent),cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),3)
            cv2.putText(img,f'count:{self.count}',(210,70),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),3)
        return img