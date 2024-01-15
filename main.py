import cv2
import mediapipe as mp
from volume_control import volume_control

def main():
    cap = cv2.VideoCapture(0)
    mp_draw = mp.solutions.drawing_utils
    vc = volume_control()
    while True:
        sucess, img = cap.read()
        vc.set_sound(img)
        cv2.imshow("image",img)
        cv2.waitKey(1)
if __name__ == "__main__":
    main()
