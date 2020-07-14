import json
import threading
from ftx import FTX
from binance import Binance
from saver import Saver
from time import sleep


def ftx():
    FTX()


def binance():
    Binance()


if __name__ == "__main__":
    saver = Saver()
    t1 = threading.Thread(target=ftx)
    t2 = threading.Thread(target=binance)
    t1.start()
    t2.start()
    try:
        while True:
            sleep(1)
    except KeyboardInterrupt:
        with open("output.txt", "w") as f:
            saved = saver.show()
            f.write(json.dumps(saved, indent=2))
