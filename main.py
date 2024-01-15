import cv2
import mediapipe as mp
from finger_count import FingerCount
def main():
    cap = cv2.VideoCapture(0)
    mp_draw = mp.solutions.drawing_utils
    fc = FingerCount()
    while True:
        sucess, img = cap.read()
        fc.counting_finger(img)
        cv2.imshow("image",img)
        cv2.waitKey(1)
if __name__ == "__main__":
    main()
