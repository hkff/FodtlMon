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
import numpy as np
import matplotlib.pyplot as plt


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
        plt.plot(data["data_none"][type], label="NONE")
        plt.plot(data["data_simp"][type], label="Simplification")
        plt.plot(data["data_solver"][type], label="Solver")
        plt.plot(data["data_fxp"][type], label="Fixpoint")
        legend = plt.legend(loc='upper left', shadow=True)
        plt.savefig("%s/%s/plot_%s.png" % (bench_dir, formula_dir, type))


bench_dir = "benchmarks_2016-06-30_22:08:52"
formula_dir = "Formula0"
plot_formula_stats(formula_dir, bench_dir)
#plt.show()
