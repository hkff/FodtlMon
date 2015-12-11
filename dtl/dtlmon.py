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
import json

class Dtlmon(Ltlmon):
    """
    DTL monitor using progression technique
    """

    def __init__(self, formula, trace, KV_events=None):
        super().__init__(formula, trace)
        self.KV = KVector()
        self.KV_events = [] if KV_events is None else KV_events

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
        elif isinstance(formula, Boolean3):
            return formula
        else:
            return super().prg(formula, trace)

    def update_kv(self):
        if len(self.KV_events) > 0:
            # TODO : add empty event
            self.KV.update(self.KV_events.pop(0))


#############################
# Distributed system
#############################

class Actor:
    """
    Actor class
    """
    def __init__(self, name="", formula=None, trace=None, KV_events=None):
        self.name = name
        self.formula = formula
        self.trace = trace
        self.monitor = None
        self.submons = []
        self.KV_events = [] if KV_events is None else KV_events

    def __str__(self):
        return "{%s; %s; %s; %s; %s}" % (self.name, self.formula, self.trace, self.monitor, self.submons)


class System:
    """
    Distributed system representation
    """
    def __init__(self, actors=None):
        self.actors = [] if actors is None else actors
        self.mons = []

    def __str__(self):
        return " | ".join([str(a) for a in self.actors])

    def add_actors(self, actor):
        if isinstance(actor, list):
            self.actors.extend(actor)
        elif isinstance(actor, Actor):
            self.actors.append(actor)
        return self

    def get_actor(self, name):
        return next((x for x in self.actors if x.name == name), None)

    def generate_monitors(self):
        for a in self.actors:
            remotes = a.formula.walk(filter_type=At)  # Get all remote formula
            for f in remotes:
                f.compute_hash()
            for f in remotes:
                remote_actor = self.get_actor(f.agent)
                remote_actor.submons.append(Dtlmon(formula=f.inner, trace=Trace()))
            a.monitor = Dtlmon(a.formula, a.trace, a.KV_events)
        for a in self.actors:
            a.monitor.KV = KVector([KVector.Entry("alice_b5bbaaef43512013e6319a76353c3d01", agent="alice", value=Boolean3.Unknown, timestamp=0)])

    @staticmethod
    def parseJSON(js):
        """
        {
            actors:
            [
                {
                    actorName : "",
                    formula: "",
                    KV_events: [],
                    trace: []
                }
            ]
        }
        :param json:
        :return:
        """
        decoded = json.JSONDecoder().decode(js)
        print(decoded)
        actors = decoded["actors"]
        s = System()
        for a in actors:
            # Getting actor info
            a_name = a["name"]
            a_formula = a["formula"]
            a_trace = a["trace"]
            a_KV_events = a["KV_events"]

            # Creating the actor
            a_formula = eval(a_formula)
            actor = Actor(name=a_name, formula=a_formula, trace=Trace.parse(a_trace), KV_events=a_KV_events)

            # Add actor to the system
            s.add_actors(actor)
        s.generate_monitors()
