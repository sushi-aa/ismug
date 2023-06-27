# Debug
DEBUG = False # Set to true to enable debugging of web server and debug logging
SAMPLE_COM_DATA = None # Set to None to disable. Otherwise overrides serial connection.

# Sensor Data Acquisition
SENSOR_TIMEOUT   = 0.1
SENSOR_COM_PORT  = "COM3"
SENSOR_BAUD_RATE = 115200

HW_POLL_INTERVAL = 1.0

# Emotion DB
SQLALCHEMY_DATABASE_URI = "sqlite:///project.db"

# Server Setup
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 8080
