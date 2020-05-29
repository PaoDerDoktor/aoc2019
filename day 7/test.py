from intcomputer import Intcomputer
from typing import List
from multiprocessing import Process, Pipe

with open("inputs.txt", 'r+') as raw_intcode:
    intcode: List[int] = [1, 0, 0, 0, 4, 0, 99]

    i, o = Pipe()

    ic = Intcomputer(intcode, "test", Intcomputer.IN_INTERNAL_LIST,
                     Intcomputer.OUT_PIPE)
    
    ic.set_out_pipe_connection(o)
    
    ic.run()

    print(int(i.recv()))