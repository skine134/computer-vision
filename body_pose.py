import mediapipe as mp
import cv2
import math
class BodyPose:
    def __init__(self,
               mode=False,
               complex=1,
               smooth=True,
               enable_seg=False,
               smooth_seg=True,
               min_detection_conf=0.5,
               min_tracking_conf=0.5):
        self.mode = mode
        self.complex = complex
        self.smooth = smooth
        self.enable_seg = enable_seg
        self.smooth_seg = smooth_seg
        self.min_detection_conf = min_detection_conf
        self.min_tracking_conf = min_tracking_conf
        self.mp_pose = mp.solutions.pose
        self.mp_draw = mp.solutions.drawing_utils
        self.pose = self.mp_pose.Pose()
        self.lm_list = []

    def init_pose(self,img):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)
    
    def find_pose(self,img,color=(255,255,255)):
        self.init_pose(img)
        if self.results.pose_landmarks:
            self.mp_draw.draw_landmarks(
                img, self.results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS,self.mp_draw.DrawingSpec(color))
        return img
    def find_position(self,img,color=(255,0,0),circle_size=5,exclude_ids=[]):
        self.lm_list=[]
        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w),  int(lm.y * h)
                cv2.circle(img,(cx,cy),circle_size,color,cv2.FILLED)
                self.lm_list.append([id,cx,cy])
                cv2.putText(img,str(id),(cx,cy-10),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),3)
        return self.lm_list
    def find_angle(self,img,p1,p2,p3,draw=True):
        x1,y1 = self.lm_list[p1][1:]
        x2,y2 = self.lm_list[p2][1:]
        x3,y3 = self.lm_list[p3][1:]
        angle_rad = math.atan2(y3-y2,x3-x2) - math.atan2(y1-y2,x1-x2)
        angle_deg = math.degrees(angle_rad)
        if draw:
            cv2.circle(img,(x1,y1),10,(0,0,255),cv2.FILLED)
            cv2.circle(img,(x1,y1),15,(0,0,255),2)
            cv2.circle(img,(x2,y2),10,(0,0,255),cv2.FILLED)
            cv2.circle(img,(x2,y2),15,(0,0,255),2)
            cv2.circle(img,(x3,y3),10,(0,0,255),cv2.FILLED)
            cv2.circle(img,(x3,y3),15,(0,0,255),2)
            cv2.line(img,(x1,y1),(x2,y2),(255,255,255),5)
            cv2.line(img,(x3,y3),(x2,y2),(255,255,255),5)
            cv2.putText(img,f'angle:{angle_deg}',(x2,y2),cv2.FONT_HERSHEY_PLAIN,3,(255,255,255),3)
        return angle_deg