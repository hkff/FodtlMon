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

import sys
import getopt
from ltl.ltlmon import *


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
    reduction = False
    help_str_extended = "fodtlmon V 0.1 .\n" + \
                        "For more information see fodtlmon home page\n Usage : mon.py [OPTIONS] formula trace" + \
                        "\n  -h \t--help          " + "\t display this help and exit" + \
                        "\n  -i \t--input= [file] " + "\t the input file" + \
                        "\n  -o \t--output= [path]" + "\t the output file" + \
                        "\n  -f \t--formula       " + "\t the formula" + \
                        "\n  -t \t--trace         " + "\t the trace" + \
                        "\n  -1 \t--ltl           " + "\t use LTL monitor" + \
                        "\n  -2 \t--fotl          " + "\t use FOTL monitor" + \
                        "\n  -3 \t--dtl           " + "\t use DTL monitor" + \
                        "\n  -4 \t--fodtl         " + "\t use FODTL monitor" + \
                        "\n  -r \t--reduction     " + "\t use on-fly reduction" + \
                        "\n\nReport fodtlmon bugs to walid.benghabrit@mines-nantes.fr" + \
                        "\nfodtlmon home page: <https://github.com/hkff/fodtlmon>" + \
                        "\nfodtlmon is a free software released under GPL 3"

    # Checking options
    try:
        opts, args = getopt.getopt(argv[1:], "hi:o:f:t:1234r",
                                   ["help", "input=", "output=", "trace=", "formula=" "ltl", "fotl", "dtl", "fodtl", "reduction"])
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
            monitor = Ltlmon()
        elif opt in ("-2", "--fotl"):
            print("Not yet implemented !")
            return
        elif opt in ("-3", "--dtl"):
            print("Not yet implemented !")
            return
        elif opt in ("-4", "--fodtl"):
            print("Not yet implemented !")
            return
        elif opt in ("-f", "--formula"):
            formula = arg
        elif opt in ("-t", "--trace"):
            trace = arg
        elif opt in ("-r", "--reduction"):
            reduction = True

    # print(argv)

    if None not in (monitor, trace, formula):
        tr = Trace().parse(trace)
        fl = eval(formula)
        res = monitor.monitor(fl, tr, reduction=reduction)
        # print(tr.contains(P.parse('P(b)')))
        print(res)
        # print(res.eval())
        # print(B3(res.eval()).value)

# Call the main
if __name__ == '__main__':
    main(sys.argv)
