"""
Fodtlmon benchmarks
Copyright (C) 2016 Walid Benghabrit

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
__author__ = 'walid'

from fodtlmon.fodtl.fodtlmon import *
from datetime import datetime


class InstrumentedMon(Fotlmon):
    """
    FOTL instrumented monitor.
    """
    def monitor(self, once=False, debug=False, struct_res=False, optimization=Optimzation.NONE, output=None):
        self.optimization = optimization

        # Create the output file
        with open(output, "w+") as f:

            f.write("# Created on %s\n" % datetime.now())
            f.write("# Optimization: %s\n" % self.optimization.name)
            f.write("# Formula: %s\n" % self.formula)
            f.write("# Trace: %s\n" % self.trace)
            f.write("# Trace length: %s\n" % len(self.trace.events))

            f.write("#\n#{:<10}{:<15}{:<20}{:<10}{:<10}\n".
                    format("Step", "Event-size", "Formula-length", "Result", "Exec-time(ms)"))

            total_start_time = time.time()

            for e in self.trace.events[self.counter:]:
                step_start_time = time.time()
                if self.last == Boolean3.Top or self.last == Boolean3.Bottom:
                    break
                else:
                    self.counter += 1
                    self.counter2 += 1
                    self.rewrite = self.prg(self.rewrite, e)
                    self.last = B3(self.rewrite.eval()) if isinstance(self.rewrite, Formula) else self.rewrite

                step_time = ((time.time() - step_start_time)*1000)
                f.write("{:<10} {:<15}{:<20}{:<10}{:5.4f}\n".
                        format(self.counter, len(e.predicates), self.rewrite.size(), self.last, step_time))

            # Result
            ret = "Result: %s after %s events." % (self.last, self.counter)
            f.write("#\n# %s\n" % ret)

            # Total exec time
            f.write("# Execution time: %5.4f ms\n" % ((time.time() - total_start_time)*1000))

        return ret
