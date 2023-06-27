from . import app, db

from .models import Hardware, Emotion

import time

@app.route('/')
def index():
    pass

@app.route('/state')
def state():
    return {
        'cv' : state_cv(),
        'hardware' : state_hw(),
        'emotion' : state_emo()
    }

@app.route('/state/cv')
def state_cv():
    return {}

@app.route('/state/hardware')
def state_hw():
    #hw = Hardware.query.first()
    hw = Hardware.query.order_by(Hardware.timestamp.desc()).first()
    return { sensor : values | { 'value' : getattr(hw,sensor) } for sensor, values in app.config['HARDWARE'].items() }

@app.route('/state/emotion')
def state_emo():
    emo = Emotion.query.order_by(Emotion.timestamp.desc()).first()
    return { emotion : value | { 'value' : getattr(emo,emotion) } for emotion, value in app.config['EMOTIONS'].items() }

@app.route('/history')
def hist():
    return {
        'cv' : hist_cv(),
        'hardware' : hist_hw(),
        'emotion' : hist_emo()
    }

@app.route('/history/cv')
def hist_cv():
    emo = Emotion.query.all()
    return { time.mktime(i.timestamp.timetuple()) : {emotion : value | { 'value' : getattr(i,emotion) } for emotion, value in app.config['EMOTIONS'].items()} for i in emo } 

@app.route('/history/hardware')
def hist_hw():
    hw = Hardware.query.all()
    return { time.mktime(i.timestamp.timetuple()) : {sensor : values | { 'value' : getattr(i,sensor) } for sensor, values in app.config['HARDWARE'].items()} for i in hw } 

@app.route('/history/emotion')
def hist_emo():
    return {}