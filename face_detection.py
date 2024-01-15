import cv2
import mediapipe as mp


class FaceDetection:

    def __init__(self, min_detection_confidence=0.75, model_selection=0):
        self.mp_face_detection = mp.solutions.face_detection
        self.mp_draw = mp.solutions.drawing_utils
        self.min_detection_confidence = min_detection_confidence
        self.model_selection = model_selection
        self.face_detection = self.mp_face_detection.FaceDetection(
            self.min_detection_confidence, self.model_selection)

    def init_detection(self, img, type: cv2.typing.MatLike = cv2.COLOR_BGR2RGB):
        self.imgRGB = cv2.cvtColor(img, type)
        self.results = self.face_detection.process(self.imgRGB)

    def detection(self, img, draw=True):
        self.init_detection(img)
        h, w, c = img.shape
        bbox_list = []
        if draw and self.results.detections:
            for id, detection in enumerate(self.results.detections):
                # self.mp_draw.draw_detection(img,detection)
                bboxC = detection.location_data.relative_bounding_box
                bbox = int(bboxC.xmin * w), int(bboxC.ymin * h), \
                    int(bboxC.width * w), int(bboxC.height * h)
                bbox_list.append([id, bbox, detection.score])
                img = self.fancy_draw(img,bbox)
                cv2.putText(img, f'{int(detection.score[0]*100)}%', (bbox[0], bbox[1]-20),
                            cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 2)
        return img, bbox_list

    def fancy_draw(self, img, bbox,line_width=30,line_weight=10, rectangle_weight=1):
        x, y, w, h = bbox
        x1, y1 = x+w, y+h
        cv2.rectangle(img, bbox, (255, 0, 255), rectangle_weight)
        #top left
        cv2.line(img, (x,y),(x+line_width,y),(255,0,255),line_weight)
        cv2.line(img, (x,y),(x,y+line_width),(255,0,255),line_weight)
        #top right
        cv2.line(img, (x1,y),(x1-line_width,y),(255,0,255),line_weight)
        cv2.line(img, (x1,y),(x1,y+line_width),(255,0,255),line_weight)

        # bottom left
        cv2.line(img, (x,y1),(x+line_width,y1),(255,0,255),line_weight)
        cv2.line(img, (x,y1),(x,y1-line_width),(255,0,255),line_weight)

        # bottom right
        cv2.line(img, (x1,y1),(x1-line_width,y1),(255,0,255),line_weight)
        cv2.line(img, (x1,y1),(x1,y1-line_width),(255,0,255),line_weight)
        return img
