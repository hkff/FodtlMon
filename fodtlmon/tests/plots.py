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


def load_formula_data(formula_dir, bench_dir):
    file = "%s/%s/gen.dat" % (bench_dir, formula_dir)
    data_none = pd.read_table(file, sep=' \s+', header=0,  encoding='utf-8', comment='#', skip_blank_lines=True, engine="python")

    file = "%s/%s/gen_simplification.dat" % (bench_dir, formula_dir)
    data_simp = pd.read_table(file, sep=' \s+', header=0,  encoding='utf-8', comment='#', skip_blank_lines=True, engine="python")

    file = "%s/%s/gen_solver.dat" % (bench_dir, formula_dir)
    data_solver = pd.read_table(file, sep=' \s+', header=0,  encoding='utf-8', comment='#', skip_blank_lines=True, engine="python")

    file = "%s/%s/gen_fixpoint.dat" % (bench_dir, formula_dir)
    data_fxp = pd.read_table(file, sep=' \s+', header=0,  encoding='utf-8', comment='#', skip_blank_lines=True, engine="python")

    return {"none": data_none, "simp": data_simp, "solver": data_solver, "fxp": data_fxp}


def plot_formula_stats(formula_dir, bench_dir):
    data = load_formula_data(formula_dir, bench_dir)

    types = ["Formula-length", "Exec-time(ms)"]
    for tp in types:
        plt.clf()
        plt.plot(data["none"][tp], label="None")
        plt.plot(data["simp"][tp], label="Simplification")
        plt.plot(data["solver"][tp], label="Solver")
        plt.plot(data["fxp"][tp], label="Fixpoint")
        legend = plt.legend(loc='upper left', shadow=True)
        plt.savefig("%s/%s/plot_%s.png" % (bench_dir, formula_dir, tp))
        #plt.show()


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Missing argument ! Usage: plots.py <bench_dir> <formula_nbr>")
        exit(-1)

    bench_dir = sys.argv[1]
    formula_dirs = ["Formula%s" % x for x in range(int(sys.argv[2]))]

    # 1. Generate graph for each formula
    #for formula_dir in formula_dirs:
    #    plot_formula_stats(formula_dir, bench_dir)

    # 2. Load all formulas data
    formulas_data = []
    for formula_dir in formula_dirs:
        formulas_data.append(load_formula_data(formula_dir, bench_dir))
    #print(formulas_data)

    plt.clf()
    df = pd.Series({'None':           formulas_data[0]["none"]["Exec-time(ms)"].sum(0),
                    'Simplification': formulas_data[0]["simp"]["Exec-time(ms)"].sum(0),
                    'Solver':         formulas_data[0]["solver"]["Exec-time(ms)"].sum(0),
                    'Fixpoint':       formulas_data[0]["fxp"]["Exec-time(ms)"].sum(0)})
    df.plot(kind='bar')
    #plt.show()

    plt.clf()
    df = pd.Series({'None':           formulas_data[0]["none"]["Formula-length"].sum(0),
                    'Simplification': formulas_data[0]["simp"]["Formula-length"].sum(0),
                    'Solver':         formulas_data[0]["solver"]["Formula-length"].sum(0),
                    'Fixpoint':       formulas_data[0]["fxp"]["Formula-length"].sum(0)})
    df.plot(kind='bar')
    plt.show()
