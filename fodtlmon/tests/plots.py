"""
Fodtlmon benchmarks analysis
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
import pandas as pd
#import numpy as np
import matplotlib.pyplot as plt
import sys


def get_dat_info(file):
    """
    Get exec_time and result from a formula bench log file
    :param file:
    :return: {"exec_time": 0, "result": "", "at": 0}
    """
    res = {"exec_time": 0, "result": "", "at": 0}
    with open(file, 'r') as f:
        lines = f.readlines()
        if "# Execution time:" in lines[-1]:
            res["exec_time"] = lines[-1].replace("# Execution time:", "").replace("ms", "").strip()

        if "# Result:" in lines[-2]:
            res["result"] = lines[-2].replace("# Result: ", "")[0]
            res["at"] = lines[-2].replace("# Result: ", "").replace(" events.", "").replace(" after ", "")[1:-1]
            try:
                res["at"] = int(res["at"])
                res["exec_time"] = float(res["exec_time"])
            except:
                raise Exception("Data conversion error !")
    return res


def load_formula_data(formula_dir, bench_dir):
    """
    Load data from a formula bench dir
    :param formula_dir:
    :param bench_dir:
    :return:
    """
    file = "%s/%s/gen.dat" % (bench_dir, formula_dir)
    data_none = pd.read_table(file, sep=' \s+', header=0,  encoding='utf-8', comment='#', skip_blank_lines=True, engine="python")
    none_info = get_dat_info(file)

    file = "%s/%s/gen_simplification.dat" % (bench_dir, formula_dir)
    data_simp = pd.read_table(file, sep=' \s+', header=0,  encoding='utf-8', comment='#', skip_blank_lines=True, engine="python")
    simp_info = get_dat_info(file)

    file = "%s/%s/gen_solver.dat" % (bench_dir, formula_dir)
    data_solver = pd.read_table(file, sep=' \s+', header=0,  encoding='utf-8', comment='#', skip_blank_lines=True, engine="python")
    solver_info = get_dat_info(file)

    file = "%s/%s/gen_fixpoint.dat" % (bench_dir, formula_dir)
    data_fxp = pd.read_table(file, sep=' \s+', header=0,  encoding='utf-8', comment='#', skip_blank_lines=True, engine="python")
    fxp_info = get_dat_info(file)

    return {"none": {"data": data_none, "info": none_info},
            "simp": {"data": data_simp, "info": simp_info},
            "solver": {"data": data_solver, "info": solver_info},
            "fxp": {"data": data_fxp, "info": fxp_info}}


def plot_formula_stats(formula_dir, bench_dir):
    """
    Plot formula stats
    :param formula_dir:
    :param bench_dir:
    :return:
    """
    data = load_formula_data(formula_dir, bench_dir)
    types = ["Formula-length", "Exec-time(ms)"]
    for tp in types:
        plt.clf()
        plt.plot(data["none"]["data"][tp], label="None")
        plt.plot(data["simp"]["data"][tp], label="Simplification")
        plt.plot(data["solver"]["data"][tp], label="Solver")
        plt.plot(data["fxp"]["data"][tp], label="Fixpoint")
        legend = plt.legend(loc='upper left', shadow=True)
        plt.ylabel(tp)
        plt.xlabel("Step")
        plt.savefig("%s/%s/plot_%s.png" % (bench_dir, formula_dir, tp))

        plt.clf()
        df = pd.Series({'None':           data["none"]["data"][tp].sum(0),
                        'Simplification': data["simp"]["data"][tp].sum(0),
                        'Solver':         data["solver"]["data"][tp].sum(0),
                        'Fixpoint':       data["fxp"]["data"][tp].sum(0)})
        plt.ylabel(tp)
        df.plot(kind='bar', rot=0)
        plt.savefig("%s/%s/plot_total_%s.png" % (bench_dir, formula_dir, tp))


#########################
#       Main
#########################
if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Missing argument ! Usage: plots.py <bench_dir> <formula_nbr> <jobs number>")
        exit(-1)

    bench_dir = sys.argv[1]
    formula_dirs = ["Formula%s" % x for x in range(int(sys.argv[2]))]
    jobs = int(sys.argv[3])

    ######################################
    # 1. Generate stats for each formula
    ######################################
    import importlib
    parallel = importlib.find_loader("joblib") is not None

    if parallel and jobs > 1:
        # Parallel version
        from joblib import Parallel, delayed
        Parallel(n_jobs=jobs)(delayed(plot_formula_stats)(formula_dir, bench_dir) for formula_dir in formula_dirs)
    else:
        # Sequential version
        for formula_dir in formula_dirs:
            plot_formula_stats(formula_dir, bench_dir)

    ######################################
    # 2. Global stats
    ######################################
    formulas_data = []
    for formula_dir in formula_dirs:
        formulas_data.append(load_formula_data(formula_dir, bench_dir))
    #print(formulas_data)

    # 2.1 Plot global merged exec-time
    plt.clf()
    data = {}
    tp = "Exec-time(ms)"
    df = pd.Series({'None':           sum([f["none"]["data"][tp].sum(0) for f in formulas_data]),
                    'Simplification': sum([f["simp"]["data"][tp].sum(0) for f in formulas_data]),
                    'Solver':         sum([f["solver"]["data"][tp].sum(0) for f in formulas_data]),
                    'Fixpoint':       sum([f["fxp"]["data"][tp].sum(0) for f in formulas_data])})
    plt.ylabel(tp)
    df.plot(kind='bar', rot=0)
    plt.savefig("%s/plot_global_%s.png" % (bench_dir, tp))

    # 2.2 Plot global merged formula length
    plt.clf()
    data = {}
    tp = "Formula-length"
    df = pd.Series({'None':           sum([f["none"]["data"][tp].sum(0) for f in formulas_data]),
                    'Simplification': sum([f["simp"]["data"][tp].sum(0) for f in formulas_data]),
                    'Solver':         sum([f["solver"]["data"][tp].sum(0) for f in formulas_data]),
                    'Fixpoint':       sum([f["fxp"]["data"][tp].sum(0) for f in formulas_data])})
    plt.ylabel(tp)
    df.plot(kind='bar', rot=0)
    plt.savefig("%s/plot_global_%s.png" % (bench_dir, tp))
