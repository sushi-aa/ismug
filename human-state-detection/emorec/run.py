from api import app, db, WebAPI
from api.models import Hardware, Emotion
from hw import Serial, HWPoll
from cv import CVCapture
from gui import UserFeedback

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

import sys
from time import sleep

import requests

def handle_start(services):
    for service in services:
        service.start()

def handle_exit(services):
    for service in services:
        service.stop()


def poll_callback(data):
    with app.app_context():
        if len(data) > 0:
            tokens = {a[0]: a[1] for tok in data.rstrip(';').split(';') if len(a:=tok.split(':'))>1}
            #print(tokens)
            entry = Hardware(**tokens)
            db.session.add(entry)
            db.session.commit()

def cv_callback(data):
    with app.app_context():
        if len(data) > 0:
            #tokens = {a[0]: a[1] for tok in data.rstrip(';').split(';') if len(a:=tok.split(':'))>1}
            #print(data[0]['emotions'])
            entry = Emotion(**data[0]['emotions'])
            db.session.add(entry)
            db.session.commit()

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

if __name__ == '__main__':
    # CHANGETHIS
    # Fetch the service account key JSON file contents
    fb_cred = credentials.Certificate('ismug-1-403a7a07002e.json')
    # Initialize the app with a service account, granting admin privileges
    fb_app = firebase_admin.initialize_app(fb_cred)
    fb_db = firestore.client()
    # Start DB
    with app.app_context():
        db.create_all()

    print("Initializing services...")

    serial = Serial(app.config['SENSOR_COM_PORT'], app.config['SENSOR_BAUD_RATE'], app.config['SENSOR_TIMEOUT'])

    # Define Services
    # Hardware Polling Service
    poll = HWPoll(serial, app.config['HW_POLL_INTERVAL'], poll_callback, app.config['SAMPLE_COM_DATA'])
    # CV Service
    cap = CVCapture(cv_callback)
    # User Feedback
    user_feedback = UserFeedback()
    # CHANGETHIS
    # Web Service
    web = WebAPI(app.config['SERVER_HOST'], app.config['SERVER_PORT'], app)
    
    services = (poll, cap, user_feedback, web)

    print("Services initialized.")
   
    print("Starting services...")

    with app.app_context():
        handle_start(services)

    print("Services started.")
    
    try:
        # CHANGETHIS
        sleep(15) # Waiting for database to get populated
        QUAD_SAMPLES = 1
        quads = [4] * QUAD_SAMPLES
        while True:
            for i in range(QUAD_SAMPLES):
                # CHANGETHIS
                # Get current values
                data = requests.get('http://localhost:8080/state').json()

                # Calculate the state
                quads[i] = calculate_state(data)
                # print(quads[i])

                sleep(5)

            quadrant = max(set(quads), key=quads.count)
            match quads[i]:
                case 1:
                    print("Current state: Exuberance")
                case 2:
                    print("Current state: Anxiety")
                case 3:
                    print("Current state: Depression")
                case 4:
                    print("Current state: Zen")
                case _:
                    print("Unknown state")

            # CHANGETHIS
            # Make a request that tells the remote web server what the current quadrant is
            #requests.get(f'https://emotion.jadewhiting.com/update/{quadrant}')
            fb_db.collection(u'Sensor Data').document(u'Vitals').set({u'quadrant': quadrant})
            print(f"Updated database: {quadrant}")
    except KeyboardInterrupt:
        handle_exit(services)
        sys.exit(0)
    
    
