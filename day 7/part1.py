from intcomputer import Intcomputer
from typing import List
from itertools import permutations
from multiprocessing import Pool
from functools import partial
from time import time


def amplifier_test(intcode: List[int], settings: List[int]) -> int:
    signal: int = 0
    for setting in settings:
        ic: Intcomputer = Intcomputer(
            intcode, inputMethod=Intcomputer.IN_INTERNAL_LIST, outputMethod=Intcomputer.OUT_INTERNAL_LIST)
        ic.list_input(setting)
        ic.list_input(signal)
        ic.run()
        signal = ic.list_output()
    return signal


if __name__ == '__main__':
    begin = time()
    with open("inputs.txt", 'r+') as raw_intcode:
        intcode: List[int] = [int(elt)
                              for elt in raw_intcode.readline().split(',')]

        settings: List[int] = list(permutations([0, 1, 2, 3, 4]))

        res: List[int]
        with Pool(None) as p:
            res = p.map(partial(amplifier_test, intcode), settings)

        print(max(res), time() - begin)
