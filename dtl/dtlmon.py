"""
dtlmon DTL monitor
Copyright (C) 2015 Walid Benghabrit

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
from dtl.dtl import *
from ltl.ltlmon import *


class Dtlmon(Ltlmon):
    """
    DTL monitor using progression technique
    """

    def __init__(self, formula, trace):
        super().__init__(formula, trace)
        self.KV = KVector()
        self.events = []

    def monitor(self):
        # counter = 0
        b3 = Boolean3.Unknown
        res = self.formula
        for e in self.trace.events[self.counter:]:
            self.update_kv()
            self.counter += 1
            res = self.prg(res, e)
            Debug(res)
            b3 = B3(res.eval()) if isinstance(res, Formula) else res
            if b3 == Boolean3.Top or b3 == Boolean3.Bottom: break
        ret = "Result Progression: %s after %s events." % (b3, self.counter)
        # print(ret)
        return ret

    def prg(self, formula, trace):
        if isinstance(formula, At):
            # Check in KV
            res = self.KV.has(formula.fid)
            return Boolean3.Unknown if res == -1 else self.KV.entries[res].value
        else:
            return super().prg(formula, trace)

    def update_kv(self):
        if len(self.events) > 0:
            self.KV.update(self.events.pop())
