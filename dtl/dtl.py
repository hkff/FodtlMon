"""
dtl
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
__author__ = 'hkff'
from ltl.ltl import *
from hashlib import md5

#############################
# Localisation Operators
#############################

class At(UExp):
    """
    Localisation operator
    """
    symbol = "@"

    def __init__(self, agent="", inner=None, fid=-1):
        super().__init__(inner)
        self.agent = agent
        self.fid = fid

    def toTSPASS(self):
        raise Exception("Not compatible with TSPASS !")

    def toLTLFO(self):
        raise Exception("Not compatible with TSPASS !")

    def prefix_print(self):
        return str(self)

    def toCODE(self):
        return "%s(%s,%s)" % (self.__class__.__name__, self.agent, self.inner.toCODE())

    def eval(self):
        return self

    def __str__(self):
        return "@_{%s}(%s)" % (self.agent, self.inner)

    def compute_hash(self):
        self.fid = "%s_%s" % (self.agent, md5(str(self.inner).encode()).hexdigest())


#############################
# Knowledge vectors
#############################

class KVector:
    """
    Knowledge vector
    """
    class Entry:
        def __init__(self, fid, agent="", value=Boolean3.Unknown, timestamp=0):
            self.fid = fid
            self.agent = agent
            self.value = value
            self.timestamp = timestamp

        def __str__(self):
            # return "{fid:%s; agent:%s; value:%s; timestamp:%s}" % (self.fid, self.agent, self.value, self.timestamp)
            return "{%s; %s; %s; %s}" % (self.fid, self.agent, self.value, self.timestamp)

        def time_compare(self, other):
            if self.fid == other.fid and self.agent == other.agent:
                if self.timestamp == other.timestamp: return 0
                elif self.timestamp > other.timestamp: return 1
                else: return -1
            else:
                return None

    def __init__(self, entries=None):
        self.entries = [] if entries is None else entries

    def __str__(self):
        return ",".join([str(e) for e in self.entries])

    def has(self, entry):
        if isinstance(entry, KVector.Entry):
            return next((self.entries.index(x) for x in self.entries if x.fid == entry.fid), -1)
        else:
            return next((self.entries.index(x) for x in self.entries if x.fid == entry), -1)

    def update(self, entry):
        i = self.has(entry)
        if i != -1:
            if entry.time_compare(self.entries[i]) == 1:
                self.entries[i] = entry

