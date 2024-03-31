from utils import Bot

class MacdBot(Bot):

    def think(self, inputs):
        assert len(inputs) == 2, len(inputs)

        prev_day, today = inputs
        p_date, p_price, p_macd, p_h, p_s = prev_day
        date, price, macd, h, s = today

        if min(p_macd, p_h, p_s, macd, h, s) <= 0:
            # Make sure we have all required MA's, otherwise do nothing
            return
        
        #print(f"Date: {date}, MACD: {macd}, H: {h}, S: {s}\n")

        # Set strategy
        __strategy = 2

        # Strategy 1: buy if MACD crosses above Signal
        if __strategy == 1 and p_macd < p_s and macd >= s:
            #print("Opening position")
            self._open_position(date, price)

        # Strategy 2: MACD crosses zero line above
        zero = 10
        if __strategy == 2 and p_macd < zero and macd >= zero:
            self._open_position(date, price)
        
        
        # Revisit previous opened positions
        self._update_positions(date, price)
