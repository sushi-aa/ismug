from threading import Thread

class ServiceThread(Thread):
    def __init__(self):
        super().__init__()
        self._running = False
    
    def start(self):
        print(f"Starting service: {str(self)}")
        self._running = True
        super().start()
    
    def run(self):
        pass

    def stop(self):
        print(f"Stopping service: {str(self)}")
        self._running = False
        self.join()
        if "_cleanup" in self.__dict__:
            self._cleanup()
        print(f"Service {str(self)} stopped.")
