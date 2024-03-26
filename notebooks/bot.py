class LongPosition:

    def __init__(self, date, price):
        self.__date = date
        self.__entry_price = price
        self.__target = price * 1.10
        self.__stop_loss = price * 0.95
        self.__is_open = True

    def update(self, price):
        if price >= self.__target or price <= self.__stop_loss:
            self.__is_open = False
            #self.__earnings = self.__entry_price/price
            return
            

        
class Bot:

    def think(self, inputs):
        assert len(inputs) == 2, len(inputs)

        prev_day, today = inputs
        p_date, p_price, p_ma20, p_ma50, p_ma100 = prev_day
        date, price, ma20, ma50, ma100 = today

        if min(p_ma20, p_ma50, p_ma100, ma20, ma50, ma100) <= 0:
            # Make sure we have all required MA's, otherwise do nothing
            return

        # Look for MAs crosses today
        if p_ma20 < p_ma50 or p_ma50 < p_ma100:
            if ma20 > ma50 and ma50 > ma100:
                self.__open_position(date, price)

        # Revisit previous opened positions
        self.__update_positions(date, price)

    def __open_position(self, date, price):
        print(f"Opening long position on {date}")

    def __update_positions(self, date, price):
        pass