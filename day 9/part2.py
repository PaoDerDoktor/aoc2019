from typing import Dict
from intcomputer import Intcomputer, list_to_dict

with open("c:\\projects\\aoc2019\\day 9\\inputs.txt", "r") as inputs:
    intcode: Dict[int, int] = list_to_dict([int(elt) for elt in inputs.readline().split(',')])
    
    ic = Intcomputer(intcode, "BOOST", Intcomputer.IN_INTERNAL_LIST, Intcomputer.OUT_STDOUT)
    
    ic.list_input(1)
    
    ic.run()