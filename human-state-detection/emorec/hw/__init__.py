import serial
from time import sleep

from service import ServiceThread

class Serial:
    def __init__(self, port: str, baudrate: int, timeout: float):
        self._port = port
        self._baud = baudrate
        self._tout = timeout
        self._comm = None
        self._prev = 0
    
    def connect(self):
        if not self._comm:
            self._comm = serial.Serial(port=self._port, baudrate=self._baud, timeout=self._tout)
            if not self._comm.is_open:
                self._comm.open()
        return self._comm
    
    def poll(self):
        val = self.connect().readline().decode('utf-8')
        if val is not None:
            self._prev = val
        return self._prev

class HWPoll(ServiceThread):
    def __init__(self, serial_obj: Serial, poll_interval: float, callback, debug_data: str = None):
        super().__init__()
        self._serial = serial_obj
        self._poll_interval = poll_interval
        self._callback = callback
        self._debug_data = debug_data
        self._debug = debug_data is not None and len(str(debug_data)) > 0

    def run(self):
        while self._running:
            # Read from Serial
            if self._debug:
                data = self._debug_data
            else:
                data = self._serial.poll()
            # Pass to callback
            self._callback(data)
            # Wait
            sleep(self._poll_interval)