import cv2
import mediapipe as mp
import time
from face_detection import face_detection
from face_mesh import face_mesh
def main():
    cap = cv2.VideoCapture(0)
    c_time = 0
    p_time = 0
    dot_color = (0,255,0)
    dot_size = 5
    # pose = body_pose()
    # tracking = hand_tracking()
    # fd = face_detection()
    fm = face_mesh()
    while True:
        # read img
        success, img = cap.read()
        img, faces = fm.show_face_mesh(img,draw=False)
        if len(faces)>0:
            print(faces[0])
        c_time = time.time()
        fps = 1/(c_time-p_time)
        p_time = c_time
        cv2.putText(img, str(int(fps)), (70, 50),
                    cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
        cv2.imshow("Image", img)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()
