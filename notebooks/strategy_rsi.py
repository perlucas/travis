from utils import Bot

class RsiBot(Bot):

    def think(self, inputs):
        assert len(inputs) == 2, len(inputs)

        prev_day, today = inputs
        p_date, p_price, p_rsi = prev_day
        date, price, rsi = today

        if min(p_rsi, rsi) <= 0:
            # Make sure we have all required MA's, otherwise do nothing
            return
        
        #print(f"Date: {date}, RSI: {rsi}\n")
        threshold = 30
        if p_rsi <= threshold and rsi > threshold:
            self._open_position(date, price)
        
        
        # Revisit previous opened positions
        self._update_positions(date, price)
