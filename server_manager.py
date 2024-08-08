import multiprocessing
import time
import requests
from main import run_fastapi

class ServerManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ServerManager, cls).__new__(cls)
            cls._instance.process = None
            cls._instance.port = 8000
        return cls._instance

    def start_server(self):
        if self.process is None or not self.process.is_alive():
            self.process = multiprocessing.Process(target=run_fastapi, args=(self.port,))
            self.process.start()
            self._wait_for_server()

    def _wait_for_server(self):
        max_retries = 30
        for _ in range(max_retries):
            try:
                requests.get(f"http://127.0.0.1:{self.port}")
                return
            except requests.ConnectionError:
                time.sleep(0.1)
        raise Exception("FastAPI server failed to start")

    def stop_server(self):
        if self.process:
            self.process.terminate()
            self.process.join()
            self.process = None