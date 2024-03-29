
class BotTracker:
    
    def __init__(self, current_index = 0):
        self._index = current_index
        self._positions = []

    def notify(self, event):
        if event["event"] != "OPEN":
            return
        self._positions.append({"index": self._index, "price": event["price"]})

    def incr(self, jump=1):
        self._index += jump

    def get_for_rendering(self):
        return self._positions