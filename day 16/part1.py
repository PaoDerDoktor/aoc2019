from typing import List


class Pattern(object):
    """Fancy data structure used to iter over a pattern of ints"""
    
    def __init__(self, base: List[int]) -> None:
        """Initialize a Pattern object with a list of ints being it's base"""
        
        self.base: List[int] = base
        
    def get(self, index: int) -> int:
        """Returns value at given index if the pattern's base were to
           repeat endlessly"""
           
        return self.base[index % len(self.base)]
    

def get_pattern(step: int) -> List[int]:
    """Returns a generated list being thez pattern needed for given step"""
    
    return Pattern([ 0 for i in range(step)] +
                   [ 1 for i in range(step)] +
                   [ 0 for i in range(step)] +
                   [-1 for i in range(step)])
    
def apply_pattern_to(signal: List[int], step: int) -> int:
    """applies given step's pattern to given signal"""
    
    outputTotal: int = 0
    pattern: Pattern = get_pattern(step)
    for i in range(len(signal)):
        outputTotal += (signal[i] * pattern.get(i+1))
        
    return abs(outputTotal) % 10

def apply_phase_to(signal: List[int]) -> List[int]:
    """Applies a whole FFT phase to a given signal"""

    resultList: List[int] = []
    
    for step in range(len(signal)):
        resultList.append(apply_pattern_to(signal, step+1))
        
    return resultList

if __name__ == "__main__":
    with open("C:\\Projects\\aoc2019\\day 16\\inputs.txt", 'r') as inputs:
        signal: List[int] = [int(elt) for elt in inputs.readline()]
        
        for i in range(100):
            signal = apply_phase_to(signal)
            
        print(signal)
           
        finalStr = "" 
        for value in signal[:8]:
            finalStr += str(value)
        
        print(finalStr)