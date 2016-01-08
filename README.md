# FODTLMON

FODTLMON Last release : Version BETA 1.0 08/01/2016

What is it?
-----------

FODTLMON is a monitoring framework based on distributed first order linear temporal logic.

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
         	--l2m           	 call ltl2mon also
      -2 	--fotl          	 use FOTL monitor
      -3 	--dtl           	 use DTL monitor
      -4 	--fodtl         	 use FODTL monitor
         	--sys= [file]   	 Run a system from json file
         	--rounds= int   	 Number of rounds to run in the system
      -z 	--fuzzer        	 run fuzzing tester


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
Copyright (C) 2014-2015 Walid Benghabrit  
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