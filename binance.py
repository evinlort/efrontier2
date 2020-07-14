from custom_websocket import CustomWebSocket


class Binance(CustomWebSocket):
    def __init__(self):
        super(Binance, self).__init__()
        self.url = "wss://fstream.binance.com/ws/btcusdt"
        self.subscribe_message = {"method": "SUBSCRIBE", "params": ["btcusdt@bookTicker"], "id": 1}
        self.connect()
        self.receiver()

    def receiver(self):
        for resp in self.receive():
            self.saver.save(self.format_data(resp))

    def format_data(self, data):
        if not data:
            return data
        formatted = dict()
        formatted["timestamp"] = int(data["T"] / 1000)
        formatted["exchange"] = "Binance"
        formatted["market"] = "btcusdt"
        formatted["bid_price"] = data["b"]
        formatted["bid_size"] = data["B"]
        formatted["ask_price"] = data["a"]
        formatted["ask_size"] = data["A"]
        return formatted
