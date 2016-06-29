#!/usr/bin/python3.4
"""
fodtlmon version 1.1
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
from fodtlmon.ltl.test import *
from fodtlmon.dtl.test import *
from fodtlmon.fotl.test import *
from fodtlmon.fodtl.test import *
from fodtlmon.parser.Parser import *
from fodtlmon.webservice.webservice import *
from fodtlmon.tests.benchmark import *

###################
# Main
###################
def main(argv):
    """
    Main mon
    :param argv: console arguments
    :return:
    """
    input_file = None
    output_file = None
    monitor = None
    formula = None
    trace = None
    iformula = None
    itrace = None
    isys = None
    online = False
    fuzzer = False
    l2m = False
    debug = False
    rounds = 1
    server_port = 8080
    webservice = False
    optimize = Optimzation.NONE

    help_str_extended = "fodtlmon V 1.1 .\n" + \
                        "For more information see fodtlmon home page\n Usage : mon.py [OPTIONS] formula trace" + \
                        "\n  -h \t--help          " + "\t display this help and exit" + \
                        "\n  -i \t--input= [file] " + "\t the input file" + \
                        "\n  -o \t--output= [path]" + "\t the output file" + \
                        "\n  -f \t--formula       " + "\t the formula" + \
                        "\n     \t--iformula      " + "\t path to file that contains the formula" + \
                        "\n  -t \t--trace         " + "\t the trace" + \
                        "\n     \t--itrace        " + "\t path to file that contains the trace" + \
                        "\n  -1 \t--ltl           " + "\t use LTL monitor" + \
                        "\n     \t--l2m=p|sa|sao  " + "\t call ltl2mon" + \
                        "\n  -2 \t--fotl          " + "\t use FOTL monitor" + \
                        "\n  -3 \t--dtl           " + "\t use DTL monitor" + \
                        "\n  -4 \t--fodtl         " + "\t use FODTL monitor" + \
                        "\n  -5 \t--fodtl         " + "\t use FODTL monitor" + \
                        "\n     \t--sys= [file]   " + "\t run a system from json file" + \
                        "\n     \t--rounds= int   " + "\t number of rounds to run in the system" + \
                        "\n  -z \t--fuzzer        " + "\t run fuzzing tester" + \
                        "\n  -d \t--debug         " + "\t enable debug mode" + \
                        "\n     \t--server        " + "\t start web service" + \
                        "\n     \t--port= int     " + "\t server port number" + \
                        "\n     \t--opt= int      " + "\t optimization level (O: Simplification, 1: Solver, " \
                                                      "2: Fixpoint, 3: Both simplification and fixpoint)" + \
                        "\n\nReport fodtlmon bugs to walid.benghabrit@mines-nantes.fr" + \
                        "\nfodtlmon home page: <https://github.com/hkff/fodtlmon>" + \
                        "\nfodtlmon is a free software released under GPL 3"

    # Checking options
    try:
        opts, args = getopt.getopt(argv[1:], "hi:o:f:t:12345zd",
                                   ["help", "input=", "output=", "trace=", "formula=" "ltl", "fotl", "dtl",
                                    "fodtl", "sys=", "fuzzer", "itrace=", "iformula=", "rounds=", "l2m=", "debug",
                                    "server", "port=", "opt=", "bench"])
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
        elif opt in ("-5", "--bench"):
            monitor = InstrumentedMon
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
            l2m = arg
        elif opt in ("-d", "--debug"):
            debug = True
        elif opt in "--server":
            webservice = True
        elif opt in "--port":
            server_port = int(arg)
        elif opt in "--opt":
            a = int(arg)
            if -1 <= a <= 3:
                optimize = Optimzation(a)
            else:
                print("Invalid optimization level %s\n"
                      " Valid are optimization levels are (O: Simplification, 1: Solver, "
                      "2: Fixpoint, 3: Both simplification and fixpoint)" % arg)
                exit(-1)

    if webservice:
        Webservice.start(server_port)
        return

    if fuzzer:
        if monitor is Ltlmon:
            run_ltl_tests(monitor="ltl", alphabet=["P"], constants=["a", "b", "c"], trace_lenght=100, formula_depth=5,
                          formula_nbr=10000, debug=debug)
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
        fl = eval(formula[1:]) if formula.startswith(":") else FodtlParser.parse(formula)
        mon = monitor(fl, tr)
        res = mon.monitor(debug=debug, optimization=optimize, output=output_file)
        print("")
        print("Trace        : %s" % tr)
        print("Formula      : %s" % fl)
        print("Code         : %s" % fl.toCODE())
        print("PPrint       : %s" % fl.prefix_print())
        print("TSPASS       : %s" % fl.toTSPASS())
        print("LTLFO        : %s" % fl.toLTLFO())
        print("Result       : %s" % res)
        print("Rewrite      : %s" % mon.rewrite)
        if l2m:
            l2m_mode = "-p"
            if l2m == "sa": l2m_mode = "-sa"
            elif l2m == "sao": l2m_mode = ""

            res = ltlfo2mon(fl.toLTLFO(), tr.toLTLFO(), mon=l2m_mode)
            print("ltl2mon : %s" % res)
