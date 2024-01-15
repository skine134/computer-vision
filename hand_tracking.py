import cv2
import mediapipe as mp


class HandTracking:
    
    def __init__(self, mode=False, max_hands=2, mudel_complex=1, min_detection_conf=0.5, min_tracikng_conf=0.5):
        self.mode = mode
        self.max_hands = max_hands
        self.mudel_complex = mudel_complex
        self.min_detection_conf = min_detection_conf
        self.min_tracikng_conf = min_tracikng_conf
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(static_image_mode=False)
        self.mpDraw = mp.solutions.drawing_utils
        self.results = None
    def init_results(self,img):
        imageRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imageRGB)
    def find_hand(self,img,draw=True):
        self.init_results(img)
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img
    def find_position(self,img,hand_no=0,circle_size=5,draw=True):
        lmList = []
        if self.results.multi_hand_landmarks:
            my_hand = self.results.multi_hand_landmarks[hand_no]
            for id, lm in enumerate(my_hand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                lmList.append([id, cx, cy])
                if draw:# and id % 4 == 0:
                    cv2.circle(img, (cx, cy), circle_size,
                                (255, 0, 255), cv2.FILLED)
        return lmList