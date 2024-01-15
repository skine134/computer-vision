import cv2
import os
import time
import mediapipe as mp
from hand_tracking import HandTracking
W_CAM, H_CAM = 640, 480

# 주석은 숫자 이미지를 화면에 띄우는 코드 관련

class FingerCount:
    
    def __init__(self,folder_path=''):
        self.ht = HandTracking()
        self.finger_indexs = [4,8,12,16,20]
        # self.folder_path = folder_path
        # dirs = os.listdir(folder_path)
        # self.file_images = []
        # for filename in dirs:
        #     filepath = f'{folder_path}/{filename}'
        #     img = cv2.imread(filepath)
        #     self.file_images.append(img)

    def counting_finger(self, img):
        img = self.ht.find_hand(img)
        lm_list = self.ht.find_position(img,draw=False)
        if len(lm_list) > 0:
            result = [0,0,0,0,0]
            for i in range(0,5):
                if i==0:
                    if lm_list[self.finger_indexs[i]][1]>lm_list[self.finger_indexs[i]-1][1]:
                        result[i]=1
                elif lm_list[self.finger_indexs[i]][2]<lm_list[self.finger_indexs[i]-1][2] and lm_list[self.finger_indexs[i]-1][2]<lm_list[self.finger_indexs[i]-2][2]:
                    result[i]=1
            # img[10:210,10:210] = self.file_images[result.count(1)-1]