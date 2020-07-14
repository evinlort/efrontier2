from typing import Optional

import websocket
import json
from saver import Saver
from abc import ABC, abstractmethod


class CustomWebSocket(ABC):
    def __init__(self, url, subscribe_message):
        websocket.enableTrace(True)
        self.ws = None
        while not self.ws:
            self.ws = websocket.create_connection(url)
        self.send(subscribe_message)
        self.saver = Saver()

    def send(self, message: dict):
        self.ws.send(json.dumps(message))

    def receive(self):
        i = 0
        while True:
            response = json.loads(self.ws.recv())
            if i > 0:
                yield response
            i += 1

    @abstractmethod
    def format_data(self, data: Optional[dict]) -> Optional[dict]:
        pass
