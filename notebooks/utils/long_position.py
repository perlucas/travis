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

    def opened_at(self):
        return datetime.strptime(self._date_opened, '%m/%d/%Y').date()
    
    def is_open(self):
        return self._is_open

    def is_closed(self):
        return not self.is_open()

    def update(self, price, date):
        #today = datetime.strptime(date, '%m/%d/%Y').date()
        #opened_at = datetime.strptime(self._date_opened, '%m/%d/%Y').date()
        #diff = today - opened_at
        #if diff.days < 7:
        #    return
        
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

    def force_close(self, price, date):
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