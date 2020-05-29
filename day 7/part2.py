from intcomputer import Intcomputer, piped_intcomputer_as_a_process
from typing import List, Dict
from itertools import permutations
from multiprocessing import Pool, Pipe, Process
from functools import partial
from time import time

def amplifier_test(intcode:List[int], settings:List[int]) -> int:
    """Return amplifier test for specified settings"""
    
    outA, inB = Pipe()
    outB, inC = Pipe()
    outC, inD = Pipe()
    outD, inE = Pipe()
    outE, inA = Pipe()
    
    pA = piped_intcomputer_as_a_process(intcode, inA, outA)
    pB = piped_intcomputer_as_a_process(intcode, inB, outB)
    pC = piped_intcomputer_as_a_process(intcode, inC, outC)
    pD = piped_intcomputer_as_a_process(intcode, inD, outD)
    pE = piped_intcomputer_as_a_process(intcode, inE, outE)
    
    outE.send(settings[0])
    outA.send(settings[1])
    outB.send(settings[2])
    outC.send(settings[3])
    outD.send(settings[4])
    
    outE.send(0)
    
    pA.start()
    pB.start()
    pC.start()
    pD.start()
    pE.start()
    
    pA.join()
    pB.join()
    pC.join()
    pD.join()
    pE.join()
    
    return inA.recv()

if __name__ == '__main__':
    begin = time()
    with open("C:\\Projects\\aoc2019\\day 7\\inputs.txt", 'r+') as raw_intcode:
        intcode:List[int] = [int(elt) for elt in raw_intcode.readline().split(',')]
        
        settings:List[int] = list(permutations([5, 6, 7, 8, 9]))
        
        res:List[int] = [amplifier_test(intcode, setting) for setting in settings]
        #with Pool(None) as p:
            #res = p.map(partial(amplifier_test, intcode), settings)
            
        print(max(res), time() - begin)