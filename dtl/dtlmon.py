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
        self.KV = {}

    def prg(self, formula, trace):
        if isinstance(formula, At):
            # Check in KV
            res = self.KV.get(formula.agent)
            return Boolean3.Unknown if res is None else res
        else:
            return super().prg(formula, trace)

    def update_kv(self, agent, value):
        self.KV[agent] = value
