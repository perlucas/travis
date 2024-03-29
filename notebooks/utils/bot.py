from .long_position import LongPosition

class Bot:

    def __init__(self, money=1000, events_listener=None):
        self._money = money
        self._positions = []
        self._events_listener = events_listener

    def think(self, inputs):
        raise 'method not implemented!'

    def budget(self):
        return self._money

    def _open_position(self, date, price):
        to_invest = self._money * 0.30 # 30% of current budget
        if to_invest < price:
            # print(f"Not enough money, want to invest {to_invest} and price is {price}")
            return
        self._positions.append(LongPosition(date, price, to_invest, self._events_listener))
        self._money -= to_invest

    def _update_positions(self, date, price):
        open_positions = [p for p in self._positions if p.is_open()]
        for p in open_positions:
            p.update(price, date)
            if p.is_closed():
                self._money += p.earnings()