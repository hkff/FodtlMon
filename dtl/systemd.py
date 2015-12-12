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
import copy


#############################
# System Actor
#############################
class Actor:
    """
    Actor class
    """

    class Event:
        """
        Internal actor event
          in  : actor-> event coming from actor
          out : ->actor sending event to actor
        """
        class EventType(Enum):
            IN = "in",
            OUT = "out"
            EMPTY = "EMPTY"

        def __init__(self, target="", e_type=EventType.EMPTY):
            self.target = target
            self.e_type = e_type

        def __str__(self):
            if self.e_type is Actor.Event.EventType.IN:
                return "->%s" % self.target
            elif self.e_type is Actor.Event.EventType.OUT:
                return "%s->" % self.target
            else:
                return "->"

        @staticmethod
        def parse(ste):
            ste = ste.strip()
            if ste == "" or ste == "->":
                return Actor.Event(e_type=Actor.Event.EventType.EMPTY)
            else:
                res = ste.split("->")
                if len(res) < 2:
                    raise Exception("Malformed Actor internal event !")
                if res[0] == "":
                    return Actor.Event(target=res[1], e_type=Actor.Event.EventType.OUT)
                else:
                    return Actor.Event(target=res[0], e_type=Actor.Event.EventType.IN)

    def __init__(self, name="", formula=None, trace=None, events=None):
        self.name = name
        self.formula = formula
        self.trace = trace
        self.monitor = None
        self.submons = []
        self.events = [] if events is None else events

    def __str__(self):
        evs = "[%s]" % ",".join(str(e) for e in self.events)
        return "{%s; %s; %s; %s; %s; %s}" % (self.name, self.formula, self.trace, self.monitor, self.submons, evs)

    def update_kv(self, kv):
        """
        Update the KV of the main monitor
        :param kv:
        :return:
        """
        self.monitor.update_kv(kv)

    def run(self):
        """
        Run main monitor and all sub monitors
        :return:
        """
        print("- Actor %s " % self.name)
        for m in self.submons:
            res = m.monitor()
            print("   | Submonitor %s : %s" % (self.name, res))
        res = self.monitor.monitor()
        print("  Main monitor %s : %s" % (self.name, res))


#############################
# Distributed system
#############################
class System:
    """
    Distributed system representation
    """
    def __init__(self, actors=None, kv_implementation=KVector):
        """
        Init the system
        coms is a dictionary that contains
        :param actors: actors list
        :param kv_implementation: the Knowledge vector implementation (IKVector)
        :return:
        """
        self.actors = [] if actors is None else actors
        self.mons = []
        self.turn = 0
        self.kv_implementation = kv_implementation
        self.coms = {}

    def __str__(self):
        return " | ".join([str(a) for a in self.actors])

    def add_actors(self, actor):
        """
        Add an actor / actor list to the system's actors
        :param actor: Actor | list<Actor>
        :return: self
        """
        if isinstance(actor, list):
            self.actors.extend(actor)
        elif isinstance(actor, Actor):
            self.actors.append(actor)
        return self

    def get_actor(self, name):
        """
        Get an actor by name
        :param name: str
        :return:
        """
        return next((x for x in self.actors if x.name == name), None)

    def generate_monitors(self):
        """
        Generate monitors for each actor in the system
        :return:
        """
        submons = []
        for a in self.actors:
            # Get all remote formula
            remotes = a.formula.walk(filter_type=At)
            # Compute formula hash
            for f in remotes:
                f.compute_hash()

            # Create the global monitor for the actor
            a.monitor = Dtlmon(a.formula, a.trace)

            # Create the remote sub monitors for each @Formula
            for f in remotes:
                remote_actor = self.get_actor(f.agent)
                remote_actor.submons.append(Dtlmon(formula=f.inner, trace=remote_actor.trace, parent=remote_actor.monitor))
                submons.append({"fid": f.fid, "actor": remote_actor.name})

            # Create the com entry in the system
            for a2 in self.actors:
                self.coms["%s->%s" % (a.name, a2.name)] = []
                self.coms["%s->%s" % (a2.name, a.name)] = []

        # Create the general KV structure
        kv = self.kv_implementation()
        for m in submons:
            kv.add_entry(self.kv_implementation.Entry(m["fid"], agent=m["actor"], value=Boolean3.Unknown, timestamp=0))

        # Add a copy of KV structure for each actor
        for a in self.actors:
            a.monitor.KV = copy.deepcopy(kv)

    def run(self):
        """
        Run the system
        :return:
        """
        print("\n====== System round %s" % self.turn)
        print("== Updating actors events...")
        for a in self.actors:
            if self.turn < len(a.events):
                e = a.events[self.turn]
                if e.e_type == Actor.Event.EventType.OUT:
                    # register
                    pass
                elif e.e_type == Actor.Event.EventType.IN:
                    # Update KV and check pop the send
                    pass

        print("\n== Running monitors on each actor...")
        for a in self.actors:
            a.run()
        self.turn += 1

    def update_events(self, e):
        """
        Update KV of each actor
        :param e:
        :return:
        """
        for a in self.actors:
            a.update_kv(e)

    @staticmethod
    def parseJSON(js):
        """
        {
            kv_type : "",
            type    : "",
            actors  : <Actors list>
                [
                    {
                     actorName : <String>,
                     formula: <String>,
                     events: ["->b", "b->"],
                     trace: []
                    }
                ]
        }
        :param json:
        :return:
        """
        decoded = json.JSONDecoder().decode(js)
        actors = decoded["actors"]
        s = System()
        for a in actors:
            # Getting actor info
            a_name = a["name"]
            a_formula = a["formula"]
            a_trace = a["trace"]
            sa_events = a["events"]
            a_events = []

            # Parsing actor info
            for e in sa_events:
                a_events.append(Actor.Event.parse(e))
            a_formula = eval(a_formula)
            a_trace = Trace.parse(a_trace)

            # Creating the actor
            actor = Actor(name=a_name, formula=a_formula, trace=a_trace, events=a_events)

            # Add actor to the system
            s.add_actors(actor)
        s.generate_monitors()
        return s
