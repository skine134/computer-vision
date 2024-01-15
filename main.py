import cv2
import mediapipe as mp
from personal_trainer import PersonalTrainer
def main():
    cap = cv2.VideoCapture(0)
    mp_draw = mp.solutions.drawing_utils
    pt = PersonalTrainer()
    while True:
        sucess, img = cap.read()
        pt.arm_training(img)
        cv2.imshow("image",img)
        cv2.waitKey(1)
if __name__ == "__main__":
    main()
