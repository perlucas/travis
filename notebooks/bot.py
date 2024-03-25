class Bot:

    def think(self, inputs):
        assert len(inputs) == 10, len(inputs)

        for in_day in inputs:
            date, price, ma20, ma50, ma100 = in_day
            print(f"Date: {date}, Price: {price}, MA20: {ma20}, MA50: {ma50}, MA100: {ma100}\n")
        
        # TODO: decide whether or not to buy applying strategy
        # TODO: Revisit previous open positions and decide whether or not to close them