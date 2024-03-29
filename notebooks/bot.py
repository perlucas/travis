from datetime import datetime

class LongPosition:

    def __init__(self, date, price, money, listener=None):
        self._date_opened = date
        self._s_price = price
        self._take_profit = price * 1.15
        self._stop_loss = price * 0.95
        self._is_open = True
        self._invested = money
        self._e_price = None
        self._events_listener = listener
        self._notify_listener({"event": "OPEN", "date":date, "price":price})

    def is_open(self):
        return self._is_open

    def is_closed(self):
        return not self.is_open()

    def update(self, price, date):
        today = datetime.strptime(date, '%m/%d/%Y').date()
        opened_at = datetime.strptime(self._date_opened, '%m/%d/%Y').date()
        diff = today - opened_at
        if diff.days < 7:
            return
        
        if price >= self._take_profit:
            # Raise TP and SL
            self._take_profit = price * 1.10
            self._stop_loss = price * 0.95
            return
        if price <= self._stop_loss:
            self._is_open = False
            self._e_price = price
            self._notify_listener({"event": "CLOSED", "date":date, "price":price})
            print(f'Closed position, earned: {round(self.earnings(percentage_only=True)*100)}%')
        
    def earnings(self, percentage_only=False):
        if self._is_open:
            raise 'position still open!'
        percentage = (self._e_price - self._s_price) / self._s_price
        if percentage_only:
            return percentage
        return self._invested * (1+percentage)

    def _notify_listener(self, event):
        if self._events_listener:
            self._events_listener.notify(event)
            

        
class Bot:

    def __init__(self, money=1000, events_listener=None):
        self._money = money
        self._positions = []
        self._events_listener = events_listener

    def think(self, inputs):
        assert len(inputs) == 2, len(inputs)

        prev_day, today = inputs
        p_date, p_price, p_ma20, p_ma50, p_ma100 = prev_day
        date, price, ma20, ma50, ma100 = today

        if min(p_ma20, p_ma50, p_ma100, ma20, ma50, ma100) <= 0:
            # Make sure we have all required MA's, otherwise do nothing
            return

        # Look for MAs crosses today
        if p_ma50 > p_ma100 and ma50 > ma100: # MA50 already crossed up MA100
        # if p_ma20 < p_ma50 or p_ma50 < p_ma100:
        #    if ma20 > ma50 and ma50 > ma100:
            if p_ma20 < p_ma50 and ma20 >= ma50:
                self.__open_position(date, price)

        # Revisit previous opened positions
        self.__update_positions(date, price)

    def budget(self):
        return self._money

    def __open_position(self, date, price):
        to_invest = self._money * 0.30 # 30% of current budget
        if to_invest < price:
            # print(f"Not enough money, want to invest {to_invest} and price is {price}")
            return
        self._positions.append(LongPosition(date, price, to_invest, self._events_listener))
        self._money -= to_invest

    def __update_positions(self, date, price):
        open_positions = [p for p in self._positions if p.is_open()]
        for p in open_positions:
            p.update(price, date)
            if p.is_closed():
                self._money += p.earnings()


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
