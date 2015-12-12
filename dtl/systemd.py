"""
systemd
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
from dtl.dtlmon import *
import json


#############################
# Distributed system
#############################

class Actor:
    """
    Actor class
    """
    def __init__(self, name="", formula=None, trace=None, events=None):
        self.name = name
        self.formula = formula
        self.trace = trace
        self.monitor = None
        self.submons = []
        self.events = [] if events is None else events

    def __str__(self):
        return "{%s; %s; %s; %s; %s}" % (self.name, self.formula, self.trace, self.monitor, self.submons)

    def update_kv(self, kv):
        self.monitor.update_kv(kv)

    def run(self):
        print("- Actor %s " % self.name)
        for m in self.submons:
            res = m.monitor()
            print("   | Submonitor %s : %s" % (self.name, res))
        res = self.monitor.monitor()
        print("  Main monitor %s : %s" % (self.name, res))


class System:
    """
    Distributed system representation
    """
    def __init__(self, actors=None):
        self.actors = [] if actors is None else actors
        self.mons = []
        self.turn = 0

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

            a.monitor = Dtlmon(a.formula, a.trace)

            for f in remotes:
                remote_actor = self.get_actor(f.agent)
                remote_actor.submons.append(Dtlmon(formula=f.inner, trace=remote_actor.trace, parent=remote_actor.monitor))

        for a in self.actors:
            # TODO create entry
            #a.monitor.KV = KVector([KVector.Entry("alice_b5bbaaef43512013e6319a76353c3d01", agent="alice", value=Boolean3.Unknown, timestamp=0)])
            pass

    def run(self):
        print("Updating actors events...")
        for a in self.actors:
            a.events

        print("Running monitors on each actor...")
        for a in self.actors:
            a.run()

    def update_events(self, e):
        for a in self.actors:
            a.update_kv(e)

    @staticmethod
    def parseJSON(js):
        """
        {
            actors:
            [
                {
                    actorName : "",
                    formula: "",
                    events: [->b, b->],
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
            a_events = a["events"]

            # Creating the actor
            a_formula = eval(a_formula)
            actor = Actor(name=a_name, formula=a_formula, trace=Trace.parse(a_trace), events=a_events)

            # Add actor to the system
            s.add_actors(actor)
        s.generate_monitors()
