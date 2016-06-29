[![License](https://img.shields.io/badge/version-1.1-orange.svg)]()
[![License](https://img.shields.io/badge/license-GPL3-blue.svg)]()
[![License](https://img.shields.io/badge/python->%3D3.4-green.svg)]()

# FodtlMon

FodtlMon Last release : Version 1.1

What is it?
-----------

FodtlMon is a monitoring framework based on distributed first order linear temporal logic.

Installation
------------

You can install fodtlmon directly using pip3 :

    https://pypi.python.org/pypi/fodtlmon
    $ sudo pip3 install fodtlmon

Or manually :
You need PythonX.X.X >= Python3.4.0 installed on your system

    You need to install the following dependencies :

        $ sudo pip3 install antlr4-python3-runtime

To install the framework run setup.py:

        $ sudo python3 setup.py install


Usage
-----


    Usage : mon.py [OPTIONS] formula trace
      -h 	--help          	 display this help and exit
      -i 	--input= [file] 	 the input file
      -o 	--output= [path]	 the output file
      -f 	--formula       	 the formula
         	--iformula      	 path to file that contains the formula
      -t 	--trace         	 the trace
         	--itrace        	 path to file that contains the trace
      -1 	--ltl           	 use LTL monitor
         	--l2m=p|sa|sao       call ltl2mon
      -2 	--fotl          	 use FOTL monitor
      -3 	--dtl           	 use DTL monitor
      -4 	--fodtl         	 use FODTL monitor
         	--sys= [file]   	 run a system from json file
         	--rounds= int   	 number of rounds to run in the system
      -z 	--fuzzer        	 run fuzzing tester
			--server        	 start web service
			--port= int     	 server port number
            --opt= int           optimization level (O: Simplification, 1: Solver 2: Fixpoint, 3: Both simplification and fixpoint)

* formula format :

        formula ::= true | false | ~formula | P(t*) | formula (=> | & | '|') formula
        | @name(formula)
        | G formula | F formula | X formula | formula ( U | R ) formula
        | ![x1:type1 x2:type2 ...] formula | ?[x1:type1 x2:type2 ...] formula
	where: t can be a variable (x, y, ...), a constant ('foo', 'bar', ...), an interpreted predicate or a function and P an id.

* event format : {Predicate(args) | ....}
* trace format : {event1; event2; .... }

Examples
---------
	python3 mon.py -f "F(w('x'))" -t "{w(a)};{w(a)};{w(x)}; {w(a)}" -2
    Result       : Result Progression: ⊤ after 3 events.



Licensing
---------

GPL V3 . Please see the file called LICENSE.

Contacts
--------

###### Developer :
>   Walid Benghabrit        <Walid.Benghabrit@mines-nantes.fr>

###### Contributors :
>   Pr.Jean-Claude Royer  <Jean-Claude.Royer@mines-nantes.fr>  (Theory)  
>   Dr. Hervé Grall       <Herve.Grall@mines-nantes.fr>        (Theory)  

-------------------------------------------------------------------------------
Copyright (C) 2014-2016 Walid Benghabrit  
Ecole des Mines de Nantes - ARMINES  
ASCOLA Research Group  
A4CLOUD Project http://www.a4cloud.eu/

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
