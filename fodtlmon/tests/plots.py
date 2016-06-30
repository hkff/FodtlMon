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

    return {"data_none": data_none, "data_simp": data_simp, "data_solver": data_solver, "data_fxp": data_fxp}


def plot_formula_stats(formula_dir, bench_dir):
    data = load_formula_data(formula_dir, bench_dir)

    types = ["Formula-length", "Exec-time(ms)"]
    for type in types:
        plt.clf()
        plt.plot(data["data_none"][type], label="None")
        plt.plot(data["data_simp"][type], label="Simplification")
        plt.plot(data["data_solver"][type], label="Solver")
        plt.plot(data["data_fxp"][type], label="Fixpoint")
        legend = plt.legend(loc='upper left', shadow=True)
        plt.savefig("%s/%s/plot_%s.png" % (bench_dir, formula_dir, type))
        #plt.show()


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Missing argument ! Usage: plots.py <bench_dir> <formula_nbr>")
        exit(-1)
    bench_dir = sys.argv[1]
    formula_dirs = ["Formula%s" % x for x in range(int(sys.argv[2]))]
    for formula_dir in formula_dirs:
        plot_formula_stats(formula_dir, bench_dir)
