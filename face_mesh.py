import cv2
import mediapipe as mp
class face_mesh:
    def __init__(self,
                static_image_mode=False,
                max_num_faces=1,
                refine_landmarks=False,
                min_detection_confidence=0.5,
                min_tracking_confidence=0.5):
        self.static_image_mode=static_image_mode
        self.max_num_faces=max_num_faces
        self.refine_landmarks=refine_landmarks
        self.min_detection_confidence=min_detection_confidence
        self.min_tracking_confidence=min_tracking_confidence
        face_mesh_module = mp.solutions.face_mesh
        self.fm = face_mesh_module.FaceMesh(
                static_image_mode=self.static_image_mode,
                max_num_faces=self.max_num_faces,
                refine_landmarks=self.refine_landmarks,
                min_detection_confidence=self.min_detection_confidence,
                min_tracking_confidence=self.min_tracking_confidence)
        self.mp_draw = mp.solutions.drawing_utils
        self.draw_sepc = self.mp_draw.DrawingSpec(thickness=1,circle_radius=1)
    
    def init_result(self,img):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.fm.process(imgRGB)
    
    def show_face_mesh(self,img,draw=True):
        faces = []
        self.init_result(img)
        if self.results.multi_face_landmarks:
            for landmark in self.results.multi_face_landmarks:
                if draw:
                    self.mp_draw.draw_landmarks(img,landmark,mp.solutions.face_mesh.FACEMESH_CONTOURS,self.draw_sepc,self.draw_sepc)
                face=[]
                for id, lm in enumerate(landmark.landmark):
                    ih,iw,ic = img.shape
                    x, y = int(lm.x*iw), int(lm.y*ih)
                    cv2.putText(img,str(id),(x,y),
                    cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 1)
                    face.append([x, y])
                faces.append(face)
        return img, faces