from utils import Bot

class AdxBot(Bot):

    def think(self, inputs):
        assert len(inputs) == 2, len(inputs)

        prev_day, today = inputs
        p_date, p_price, p_adx, p_pdi, p_ndi = prev_day
        date, price, adx, pdi, ndi = today

        if min(p_adx, p_pdi, p_ndi, adx, pdi, ndi) <= 0:
            # Make sure we have all required MA's, otherwise do nothing
            return
        
        #print(f"Date: {date}, ADX: {adx}, +DI: {pdi}, -DI: {ndi}\n")

        # Look for +DI crossing upwards -DI
        if p_pdi <= p_ndi and pdi > ndi and adx > ndi and adx < pdi:
            self._open_position(date, price)

        # Revisit previous opened positions
        self._update_positions(date, price)
