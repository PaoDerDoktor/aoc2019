from typing import List, Tuple, Iterator
from time import time
from operator import mul
    

def get_pattern(step: int) -> List[int]:
    """Returns a generated list being thez pattern needed for given step"""
    
    return ([0] * step + [ 1] * step +
            [0] * step + [-1] * step)
    
def access(pattern: List[int], index: int) -> int:
    """Returns the value from the pattern at specified index if the
       pattern were to repeat endlessly"""
       
    return pattern[index % len(pattern)]
        
def apply_pattern_to(signal: List[int], step: int) -> int:
    """applies given step's pattern to given signal"""
    
    pattern: List[int] = get_pattern(step)
    
    resultMap: Iterator = [access(pattern, i+1)*signal[i] for i in range(len(signal))]
    
    return abs(sum(resultMap)) % 10

def apply_phase_to(signal: List[int]) -> List[int]:
    """Applies a whole FFT phase to a given signal"""
    
    return [apply_pattern_to(signal, step) for step in range(1, len(signal)+1)]

if __name__ == "__main__":
    with open("C:\\Projects\\aoc2019\\day 16\\inputs.txt", 'r') as inputs:
        signal: List[int] = [int(elt) for elt in inputs.readline()]
        
        beginTime: float = time()
        
        print("getting offset...")
        offset: int = 0
        offsetStr: str = "" 
        for value in signal[:8]:
            offsetStr += str(value) 
        offset = int(offsetStr)
        
        print("starting !")
        print("========")
        
        phaseDurations: List[float] = []
        iterationsAmount: int = 100
        
        for i in range(iterationsAmount):
            print(f"ITERATION {i}")
            startTime: float = time()
            signal = apply_phase_to(signal)
            phaseDurations.append(time() - startTime)
           
        finalStr: str = "" 
        for value in signal[:8]:
            finalStr += str(value)
        
        print("========\nMessage :",finalStr)
        print("Total time :", time() - beginTime)
        print("Average phase time :", sum(phaseDurations) / iterationsAmount)
        
        #Idea : Group by pattern value ?