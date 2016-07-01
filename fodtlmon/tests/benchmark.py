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
from fodtlmon.ltl.test import Fuzzer


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

            f.write("#\n{:<10}{:<15}{:<20}{:<10}{:<10}\n".
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


def run_formula(base_dir, f_dir):
    """
    Run benchmark on a formula
    :param base_dir: base directory
    :param f_dir: form FormulaX
    :return:
    """
    print(f_dir)
    formula_file = "%s/%s/%s.formula" % (base_dir, f_dir, f_dir.replace("Formula", ""))
    trace_file = "%s/%s/%s.trace" % (base_dir, f_dir, f_dir.replace("Formula", ""))
    with open(formula_file, "r") as f:
        formula = f.read()
    with open(trace_file, "r") as f:
        trace = f.read()

    tr = Trace().parse(trace)
    fl = FodtlParser.parse(formula)

    # 1. No optimization
    output_file = "%s/%s/gen.dat" % (base_dir, f_dir)
    InstrumentedMon(fl, tr).monitor(optimization=Optimzation.NONE, output=output_file)

    # 2. Simplification
    output_file = "%s/%s/gen_simplification.dat" % (base_dir, f_dir)
    InstrumentedMon(fl, tr).monitor(optimization=Optimzation.SIMPLIFICATION, output=output_file)

    # 3. Solver
    output_file = "%s/%s/gen_solver.dat" % (base_dir, f_dir)
    InstrumentedMon(fl, tr).monitor(optimization=Optimzation.SOLVER, output=output_file)

    # 4. Fixpoint
    output_file = "%s/%s/gen_fixpoint.dat" % (base_dir, f_dir)
    InstrumentedMon(fl, tr).monitor(optimization=Optimzation.FIXPOINT, output=output_file)


def run_benchmarks(bench_dir="fodtlmon/tests/benchmarks/", jobs=1):
    """
    Run benchmarks
    """
    # Get formulas folders
    formulas_dir = []
    dirs = os.listdir(bench_dir)
    for file in dirs:
        formulas_dir.append(file)

    # Check for joblib
    import importlib
    parallel = importlib.find_loader("joblib") is not None

    if parallel and jobs > 1:
        # Parallel version
        from joblib import Parallel, delayed
        Parallel(n_jobs=jobs)(delayed(run_formula)(bench_dir, x) for x in formulas_dir)
    else:
        # Sequential version
        for x in formulas_dir:
            run_formula(bench_dir, x)


def gen_formula_trace(x, fuzzer, formula_nbr, formula_depth, trace_length, trace_depth, write_dir="fodtlmon/tests/benchmarks/"):
    """
    Generate a formula and a trace
    """
    f_dir = "%sFormula%s" % (write_dir, x)
    os.mkdir(f_dir)
    formula = fuzzer.gen(formula_depth)
    trace = fuzzer.gen_trace(trace_length, depth=trace_depth, preds=formula.walk(filter_type=P))
    with open("%s/%s.formula" % (f_dir, x), "w+") as f: f.write(str(formula))
    with open("%s/%s.trace" % (f_dir, x), "w+") as f: f.write(str(trace))


def generate_benchmarks(formula_nbr=1, formula_depth=2, trace_length=5, trace_depth=1, jobs=1, alphabet=None, constants=None):
    """
    Generate formulas and traces for benchmarks
    :param formula_nbr:
    :param formula_depth:
    :param trace_length:
    :param trace_depth:
    :param jobs:
    :param alphabet:
    :param constants:
    :return:
    """
    alphabet = ["P"] if alphabet is None else alphabet
    constants = ["a", "b", "c"] if constants is None else constants
    fuzzer = Fuzzer("fotl", alphabet=alphabet, constants=constants)
    fuzzer.init_fuzzer()

    import datetime
    output_dir = "fodtlmon/tests/benchmarks_%s/" % (datetime.datetime.today().strftime("%Y-%m-%d_%H:%M:%S"))

    os.mkdir(output_dir)

    # Check for joblib
    import importlib
    parallel = importlib.find_loader("joblib") is not None

    if parallel and jobs > 1:
        # Parallel version
        from joblib import Parallel, delayed
        Parallel(n_jobs=jobs)(delayed(gen_formula_trace)(x, fuzzer, formula_nbr, formula_depth, trace_length,
                                                         trace_depth, write_dir=output_dir)
                              for x in range(formula_nbr))
    else:
        # Sequential version
        for x in range(formula_nbr):
            gen_formula_trace(x, fuzzer, formula_nbr, formula_depth, trace_length, trace_depth, write_dir=output_dir)

    return output_dir


def load_bench_from_file(bench_file):
    """
    Read the benchmark from config file and run it
    :param bench_file: format
        {
            "formula_nbr": int,        DEFAULT 1
            "formula_depth": int,      DEFAULT 2
            "trace_length": int,       DEFAULT 5
            "trace_depth": int,        DEFAULT 1
            "alphabet": list of str,   DEFAULT ["p"]
            "constants": list of str,  DEFAULT ["a", "b", "c"]
            "jobs": int                DEFAULT 1
       }
    :return:
    """
    import ast

    with open(bench_file, 'r') as f:
        config = ast.literal_eval(f.read())

    keys = config.keys()
    formula_nbr = int(config["formula_nbr"]) if "formula_nbr" in keys else 1
    formula_depth = int(config["formula_depth"]) if "formula_depth" in keys else 2
    trace_length = int(config["trace_length"]) if "trace_length" in keys else 5
    trace_depth = int(config["trace_depth"]) if "trace_depth" in keys else 1
    alphabet = list(config["alphabet"]) if "alphabet" in keys else ["P"]
    constants = list(config["constants"]) if "constants" in keys else ["a", "b", "c"]
    jobs = int(config["jobs"]) if "jobs" in keys else 1

    output_dir = generate_benchmarks(formula_nbr=formula_nbr, formula_depth=formula_depth, trace_length=trace_length,
                                     trace_depth=trace_depth, jobs=jobs, alphabet=alphabet, constants=constants)
    run_benchmarks(bench_dir=output_dir, jobs=jobs)
