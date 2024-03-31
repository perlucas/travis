from utils import Bot
import numpy as np

class MinsGroup:

    def __init__(self, point):
        self._points = []
        self._avg = -1
        self._range = [-1,-1]
        self._add_and_update(point)

    def accepts(self, point):
        min, max = self._range
        return min <= point and point <= max

    def add(self, point):
        self._add_and_update(point)

    def weight(self):
        return len(self._points)

    def _add_and_update(self, point):
        self._points.append(point)
        self._avg = np.average(self._points)
        self._range = [self._avg * 0.95, self._avg * 1.10]


class LMinsBot(Bot):

    def think(self, inputs, lmins):
        assert len(inputs) == 2, len(inputs)

        _, today = inputs
        date, price = today

        mins = self._process_lmins(lmins)

        
        # Look for +DI crossing upwards -DI
        if False:
            self._open_position(date, price)

        # Revisit previous opened positions
        self._update_positions(date, price)

    def _process_lmins(self, lmins):
        groups = []
        for m in lmins:
            added = False
            # Try to locate the point in a group
            for g in groups:
                if g.accepts(m):
                    g.add(m)
                    added = True
                    break
            # Create a new group if point cannot be placed into any group
            if not added:
                groups.append(MinsGroup(m))
        return groups
                