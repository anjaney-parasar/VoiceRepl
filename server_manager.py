import requests
import time

class ServerManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ServerManager, cls).__new__(cls)
            cls._instance.port = 8000
        return cls._instance

    def start_server(self):
        self._wait_for_server()

    def _wait_for_server(self):
        max_retries = 30
        for _ in range(max_retries):
            try:
                requests.get(f"http://127.0.0.1:{self.port}")
                return
            except requests.ConnectionError:
                time.sleep(1)
        raise Exception("FastAPI server failed to start")

    def stop_server(self):
        pass  # No need to stop the server in this setup