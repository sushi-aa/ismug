from sqlalchemy.sql import func

from . import app
from . import db

col_map = {
    'txt'    : db.Text,
    'str'    : db.String,
    'int'    : db.Integer,
    'float'  : db.Float,
    'bool'   : db.Boolean,
}

def __map_col_type__(col_type: str):
    col_type = col_type.strip().lower()
    return col_map[col_type] if col_type in col_map else db.String

class Hardware(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    timestamp = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())

for sensor, values in app.config['HARDWARE'].items():
    setattr(Hardware,sensor,db.Column(__map_col_type__(values['type'])))

class Emotion(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    timestamp = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())

for emotion, values in app.config['EMOTIONS'].items():
    #print(emotion)
    setattr(Emotion,emotion,db.Column(__map_col_type__(app.config['EMOTION_TYPE'])))