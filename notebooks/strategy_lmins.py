from utils import Bot
from datetime import datetime
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
        self._range = [self._avg * 0.98, self._avg * 1.02]

    def avg(self):
        return self._avg

class LMinsBot(Bot):

    def __init__(self, money=1000, events_listener=None):
        Bot.__init__(self,money,events_listener)
        self._groups = []

    def think(self, inputs, lmins):
        assert len(inputs) == 2, len(inputs)

        _, today = inputs
        date, price = today

        # Can open position only if last one was at least 5 days ago
        today = datetime.strptime(date, '%m/%d/%Y').date()
        can_operate = True
        last_position = None if len(self._positions) == 0 else self._positions[len(self._positions)-1]
        if last_position != None:
            diff = today - last_position.opened_at()
            can_operate = diff.days >= 5
        
        #print(lmins)
        if can_operate:
            g_mins = self._process_lmins(lmins)
            
            # Open long position if price is a min
            accepted_by = [g for g in g_mins if g.accepts(price) and g.weight() >= 3]
            if len(accepted_by) > 0:
                self._open_position(date, price)

        # Revisit previous opened positions
        self._update_positions(date, price)

    def _process_lmins(self, lmins):
        for m in lmins:
            # Try to locate the point in a group
            added = self._point_is_accepted(m)
            # Create a new group if point cannot be placed into any group
            if not added:
                self._groups.append(MinsGroup(m))
        return self._groups

    def _point_is_accepted(self, point):
        for g in self._groups:
            if g.accepts(point):
                g.add(point)
                return True
        return False

    def get_groups(self):
        return [(g.avg(), g.weight()) for g in self._groups]