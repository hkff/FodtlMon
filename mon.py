#!/usr/bin/python3.4
"""
fodtlmon version 0.1
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
__author__ = 'walid'
import sys
import getopt
from ltl.test import *
from dtl.test import *
from fotl.test import *
from fodtl.test import *


###################
# Main
###################
def main(argv):
    """
    Main mon
    :param argv: console arguments
    :return:
    """
    input_file = ""
    output_file = ""
    monitor = None
    formula = None
    trace = None
    online = False
    fuzzer = False
    iformula = None
    itrace = None
    isys = None
    rounds = 1
    l2m = False
    help_str_extended = "fodtlmon V 0.1 .\n" + \
                        "For more information see fodtlmon home page\n Usage : mon.py [OPTIONS] formula trace" + \
                        "\n  -h \t--help          " + "\t display this help and exit" + \
                        "\n  -i \t--input= [file] " + "\t the input file" + \
                        "\n  -o \t--output= [path]" + "\t the output file" + \
                        "\n  -f \t--formula       " + "\t the formula" + \
                        "\n     \t--iformula      " + "\t path to file that contains the formula" + \
                        "\n  -t \t--trace         " + "\t the trace" + \
                        "\n     \t--itrace        " + "\t path to file that contains the trace" + \
                        "\n  -1 \t--ltl           " + "\t use LTL monitor" + \
                        "\n     \t--l2m           " + "\t call ltl2mon also" + \
                        "\n  -2 \t--fotl          " + "\t use FOTL monitor" + \
                        "\n  -3 \t--dtl           " + "\t use DTL monitor" + \
                        "\n  -4 \t--fodtl         " + "\t use FODTL monitor" + \
                        "\n     \t--sys= [file]   " + "\t Run a system from json file" + \
                        "\n     \t--rounds= int   " + "\t Number of rounds to run in the system" + \
                        "\n  -z \t--fuzzer        " + "\t run fuzzing tester" + \
                        "\n\nReport fodtlmon bugs to walid.benghabrit@mines-nantes.fr" + \
                        "\nfodtlmon home page: <https://github.com/hkff/fodtlmon>" + \
                        "\nfodtlmon is a free software released under GPL 3"

    # Checking options
    try:
        opts, args = getopt.getopt(argv[1:], "hi:o:f:t:1234z",
                                   ["help", "input=", "output=", "trace=", "formula=" "ltl", "fotl", "dtl",
                                    "fodtl", "sys=", "fuzzer", "itrace=", "iformula=", "rounds=", "l2m"])
    except getopt.GetoptError:
        print(help_str_extended)
        sys.exit(2)

    if len(opts) == 0:
        print(help_str_extended)

    # Handling options
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(help_str_extended)
            sys.exit()
        elif opt in ("-i", "--input"):
            input_file = arg
        elif opt in ("-o", "--output"):
            output_file = arg
        elif opt in ("-1", "--ltl"):
            monitor = Ltlmon
        elif opt in ("-2", "--fotl"):
            monitor = Fotlmon
        elif opt in ("-3", "--dtl"):
            monitor = Dtlmon
        elif opt in ("-4", "--fodtl"):
            monitor = Fodtlmon
        elif opt in ("-f", "--formula"):
            formula = arg
        elif opt in ("-t", "--trace"):
            trace = arg
        elif opt in "--sys":
            isys = arg
        elif opt in "--rounds":
            rounds = int(arg)
        elif opt in ("-z", "--fuzzer"):
            fuzzer = True
        elif opt in "--iformula":
            iformula = arg
        elif opt in "--itrace":
            itrace = arg
        elif opt in "--l2m":
            l2m = True

    if fuzzer:
        if monitor is Ltlmon:
            run_ltl_tests(monitor="ltl", alphabet=["P"], constants=["a", "b", "c"], trace_lenght=10, formula_depth=5, formula_nbr=10000)
        elif monitor is Dtlmon:
            run_dtl_tests()
        return

    if itrace is not None:
        with open(itrace, "r") as f:
            trace = f.read()

    if iformula is not None:
        with open(iformula, "r") as f:
            formula = f.read()

    if isys is not None:
        with open(isys, "r") as f:
            js = f.read()
            s = System.parseJSON(js)
            for x in range(rounds):
                s.run()
        return

    # print(argv)
    if None not in (monitor, trace, formula):
        tr = Trace().parse(trace)
        fl = eval(formula)
        mon = monitor(fl, tr)
        res = mon.monitor()
        print("")
        print("Trace        : %s" % tr)
        print("Formula      : %s" % fl)
        print("Code         : %s" % fl.toCODE())
        print("PPrint       : %s" % fl.prefix_print())
        print("TSPASS       : %s" % fl.toTSPASS())
        print("LTLFO        : %s" % fl.toLTLFO())
        print("Result       : %s" % res)
        if l2m:
            print(fl.toLTLFO())
            res = ltlfo2mon(fl.toLTLFO(), tr.toLTLFO())
            print("ltl2mon : %s" % res)

# Call the main
if __name__ == '__main__':
    main(sys.argv)
