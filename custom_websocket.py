from typing import Optional

import websocket
import json
from saver import Saver
from abc import ABC, abstractmethod


class CustomWebSocket(ABC):
    def __init__(self):
        websocket.enableTrace(True)
        self.ws = None
        self.url = None
        self.subscribe_message = None
        self.saver = Saver()

    def connect(self):
        while not self.ws:
            self.ws = websocket.create_connection(self.url)
        self.send(self.subscribe_message)

    def send(self, message: dict):
        self.ws.send(json.dumps(message))

    def receive(self):
        i = False
        while True:
            response = json.loads(self.ws.recv())
            if i:
                yield response
            i = True

    @abstractmethod
    def format_data(self, data: Optional[dict]) -> Optional[dict]:
        pass
