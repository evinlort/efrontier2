import json
import threading


class Saver:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Saver, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.saved = []
        self.is_printable = True

    def save(self, message):
        lock = threading.Lock()
        with lock:
            if message is not None:
                self.saved.append(message)
                if self.is_printable:
                    print(json.dumps(message))

    def show(self):
        return self.saved
