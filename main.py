import cv2
import mediapipe as mp
import time
from body_pose import body_pose
from hand_tracking import hand_tracking

def main():
    cap = cv2.VideoCapture(0)
    mp_pose = mp.solutions.pose
    mp_draw = mp.solutions.drawing_utils
    pose = mp_pose.Pose()
    c_time = 0
    p_time = 0
    pose = body_pose()
    tracking = hand_tracking()
    dot_color = (0,255,0)
    dot_size = 5
    while True:
        success, img = cap.read()
        img = pose.find_pose(img)
        img = tracking.find_hand(img)
        pose.find_position(img,dot_color,dot_size,exclude_ids=[16,17,18,19,20,21])
        tracking.find_position(img)
        c_time = time.time()
        fps = 1/(c_time-p_time)
        p_time = c_time
        cv2.putText(img, str(int(fps)), (70, 50),
                    cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
        cv2.imshow("Image", img)
        cv2.waitKey(1)
# hand_tracking
# from hand_tracking import hand_tracking
#
# def main():
#     cap = cv2.VideoCapture(0)
#     pTime = 0
#     cTime = 0
#     tracking = hand_tracking()
#     while True:
#         success, img = cap.read()
#         img = tracking.find_hand(img,draw=False)
#         lm = tracking.find_position(img,circle_size=9,draw=True)
#         if len(lm) !=0:
#             print(lm[4])
#         cTime = time.time()
#         fps = 1/(cTime-pTime)
#         pTime = cTime
#         cv2.putText(img, str(int(fps)), (10, 70),
#                     cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
#         cv2.imshow("Image", img)
#         cv2.waitKey(1)


if __name__ == "__main__":
    main()
