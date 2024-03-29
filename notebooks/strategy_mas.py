from utils import Bot

class MasBot(Bot):

    def think(self, inputs):
        assert len(inputs) == 2, len(inputs)

        prev_day, today = inputs
        p_date, p_price, p_ma20, p_ma50, p_ma100 = prev_day
        date, price, ma20, ma50, ma100 = today

        if min(p_ma20, p_ma50, p_ma100, ma20, ma50, ma100) <= 0:
            # Make sure we have all required MA's, otherwise do nothing
            return

        # Look for MAs crosses today
        #if (p_ma50 > p_ma100 and ma50 > ma100) and p_ma20 < p_ma50 and ma20 >= ma50:
        #if (p_ma20 < p_ma50 or p_ma50 < p_ma100) and ma20 > ma50 and ma50 > ma100:
        if p_ma50 < p_ma100 and ma50 >= ma100:
                self._open_position(date, price)

        # Revisit previous opened positions
        self._update_positions(date, price)
