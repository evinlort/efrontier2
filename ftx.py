from typing import Optional

from custom_websocket import CustomWebSocket


class FTX(CustomWebSocket):
    def __init__(self):
        url = "wss://ftx.com/ws/"
        subscribe_message = {"channel": "orderbook", "market": "BTC-PERP", "op": "subscribe"}
        super(FTX, self).__init__(url, subscribe_message)

    def receiver(self):
        gen = super(FTX, self).receive()
        while resp := next(gen):
            resp = self.get_relevant_data(resp)
            self.saver.save(self.format_data(resp))

    @staticmethod
    def get_relevant_data(message: dict) -> Optional[dict]:
        if message["type"] == "partial":
            return None
        message = message["data"]
        if len(message["bids"]) == 0 and len(message["asks"]) == 0:
            return None
        if len(message["bids"]) > 0:
            message["bids"] = message["bids"][0]
        else:
            message["bids"] = [0, 0]
        if len(message["asks"]) > 0:
            message["asks"] = message["asks"][0]
        else:
            message["asks"] = [0, 0]
        del message["checksum"]
        del message["action"]
        message["time"] = int(message["time"])
        return message

    def format_data(self, data: Optional[dict]) -> Optional[dict]:
        if not data:
            return data
        formatted = dict()
        formatted["timestamp"] = data["time"]
        formatted["exchange"] = "FTX"
        formatted["market"] = "BTC-PERP"
        formatted["bid_price"] = data["bids"][0]
        formatted["bid_size"] = data["bids"][1]
        formatted["ask_price"] = data["asks"][0]
        formatted["ask_size"] = data["asks"][1]
        return formatted
