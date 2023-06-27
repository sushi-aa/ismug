import requests
from fer import FER
import cv2
from pprint import pprint
import time

from service import ServiceThread

GRAPH_PATH = 'graph.png'

def calculate_state(data) -> int:
    # Quadrants as follows:
    # 1: Calm / Energy
    # 2: Tense / Energy
    # 3: Tense / Tired
    # 4: Calm / Tired

    # happy=1, angy=-1, sad=-1, neutral=0 

    # TODO: Help. Pls.

    # Really naïve approach to state inference.
    # okay
    # happy AND tense (increase in heart rate) -> Q1
    # unhappy AND tense (increase in heart rate) -> Q2
    # unhappy AND calm (normal heart rate) -> Q3
    # happy AND calm (normal heart rate) -> Q4

    # {'cv': {}, 'emotion': {'angry': {'value': 0.16}, 'disgust': {'value': 0.0}, 'fear': {'value': 0.11}, 'happy': {'value': 0.08}, 'neutral': {'value': 0.58}, 'sad': {'value': 0.07}, 'surprise': {'value': 0.01}}, 'hardware': {'pulse': {'type': 'float', 'unit': 'bpm', 'value': 88.0}}}

    # this is bad code
    # i do not endorse writing bad code
    # uwu

    bpm = data['hardware']['pulse']['value']
    RESTING_BPM = 80
    TENSE_BPM = 90

    #print(data['emotion'])
    best_emo = max(data['emotion'], key=lambda emo: data['emotion'][emo]['value'])
    #print(f'DEBUG: {best_emo}')
    
    if bpm:
        if best_emo in ['happy', 'neutral']:
            return 1 if bpm > TENSE_BPM else 4
        if best_emo in ['sad', 'angry']:
            return 2 if bpm > TENSE_BPM else 3
        
    return 4

class CVCapture(ServiceThread):    
    def run(self):
        fps = 0
        detector = FER()

        while self._running:        
            start_time = time.time()
            ret,frame=self._cap.read()
            
            if not ret:
                continue

            result = detector.detect_emotions(frame)
            #print(result)
            top_result = detector.top_emotion(frame)
            pred_label = "None" if top_result[0] == None else top_result[0]
            confidence = 0 if top_result[1] == None else top_result[1]

            self._callback(result)

            data = requests.get('http://localhost:8080/state').json()
            bpm = data['hardware']['pulse']['value']
            quadrant = calculate_state(data)
            
            #cv2.putText(frame, 'FPS: {:.2f}'.format(fps), (10, 20), cv2.FONT_HERSHEY_SIMPLEX,0.8, (255, 20, 55), 1)
            cv2.putText(frame, 'Label: {}'.format(pred_label), (10,20), cv2.FONT_HERSHEY_SIMPLEX,0.8, (255, 20, 55), 1)
            cv2.putText(frame, 'Confidence: {:.2f}'.format(confidence), (10, 50), cv2.FONT_HERSHEY_SIMPLEX,0.8, (255, 20, 55), 1)
            cv2.putText(frame, 'Heart Rate: {} bpm'.format(bpm), (10, 80), cv2.FONT_HERSHEY_SIMPLEX,0.8, (255, 20, 55), 1)
            cv2.putText(frame, 'Quadrant: {}'.format(quadrant), (10, 110), cv2.FONT_HERSHEY_SIMPLEX,0.8, (255, 20, 55), 1)           

            graph = cv2.imread(GRAPH_PATH)
            desired_dims = (int(graph.shape[1] * 0.2), int(graph.shape[0] * 0.2))
            graph = cv2.resize(graph, desired_dims, interpolation = cv2.INTER_AREA)

            rows,cols,_ = graph.shape

            rect_width = int(cols/2)
            rect_height = int(rows/2)
            start_point = (0,0)
            end_point = (rect_width,rect_height)
            
            color = (3, 186, 252)
            thickness = 5

            INSET = 2

            x,y,_ = frame.shape
            x-=cols
            y-=rows

            if quadrant == 1:
                start_point = (rect_width + INSET,INSET)
                end_point = (cols-INSET, rect_height-INSET)
            elif quadrant == 2:
                start_point = (INSET,INSET)
                end_point = (rect_width-INSET,rect_height-INSET)
            elif quadrant == 3:
                start_point = (INSET,rect_height+INSET)
                end_point = (rect_width-INSET,rows-INSET)
            elif quadrant == 4:
                start_point = (rect_width+INSET,rect_height+INSET)
                end_point = (cols-INSET,rows-INSET)
            
            #start_point = (start_point[0] + x, start_point[1] + y)
            #end_point = (end_point[0] + x, end_point[1] + y)

            cv2.rectangle(graph, start_point, end_point, color, thickness)

            frame[-rows:,-cols:] = graph

            cv2.imshow("iSMuG",frame)
            cv2.waitKey(100)

            fps = (1.0 / (time.time() - start_time))
            
    def __init__(self, callback):
        super().__init__()
        self._callback = callback
        self._cap = cv2.VideoCapture(0)

    def _cleanup(self):
        print("Cleaning up...")
        self._cap.release() 
        cv2.destroyAllWindows() 