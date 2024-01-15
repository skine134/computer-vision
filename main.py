import cv2
import mediapipe as mp

def main():
    cap = cv2.VideoCapture(0)
    mp_draw = mp.solutions.drawing_utils
    while True:
        sucess, img = cap.read()
        cv2.imshow("image",img)
        cv2.waitKey(1)
if __name__ == "__main__":
    main()
