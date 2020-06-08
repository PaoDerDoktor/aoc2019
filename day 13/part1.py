from intcom import *
from typing import List, Dict
from enum import IntEnum
from copy import deepcopy


class TILE_TYPE(IntEnum):
    """Enumeration of the possible tile types"""
    
    EMPTY    = 0
    WALL     = 1
    BLOCK    = 2
    H_PADDLE = 3
    BALL     = 4


class Arcade(object):
    """A class representing an Acade machine"""
    
    def __init__(self, gameProg: List[int]) -> None:
        """Builds an Arcade machine from a code"""
        
        self.processorIn: List[int] = []
        self.processorOut: List[int] = []
        
        self.processor: Intcom = Intcom(list_to_dict(gameProg), 'Arcade Game',
                                        inputMethod=IO_METHOD.LIST, outputMethod=IO_METHOD.LIST,
                                        inputSrc=self.processorIn, outputDest=self.processorOut)
        
        self.screen: List[List[TILE_TYPE]] = [[0 for j in range(24)] for i in range(41)]
        
        
    def run(self) -> None:
        """Runs the Arcade machine"""
        
        self.processor.run()
        
        while len(self.processorOut):
            x: int = self.processorOut.pop()
            y: int = self.processorOut.pop()
            t: int = self.processorOut.pop()
            
            self.screen[x][y] = t
            
    def screen_str(self) -> str:
        """Returns a string representing the screen"""
        
        res: str = ""
        for y in range(len(self.screen[0])):
            for x in range(len(self.screen)):
                if self.screen[x][y] == TILE_TYPE.EMPTY:
                    res += '.'
                elif self.screen[x][y] == TILE_TYPE.BLOCK:
                    res += '#'
                elif self.screen[x][y] == TILE_TYPE.H_PADDLE:
                    res += '-'
                elif self.screen[x][y] == TILE_TYPE.WALL:
                    res += '@'
                elif self.screen[x][y] == TILE_TYPE.BALL:
                    res += 'O'
            res += "\n"
        return res
                

        
if __name__ == '__main__':
    with open("C:\\Projects\\aoc2019\\day 13\\inputs.txt", 'r') as inputs:
        intcode = [int(elt) for elt in inputs.readline().split(',')]
        
        arcade: Arcade = Arcade(intcode)
        
        arcade.run()
        
        totalBlocks: int = 0
        for row in arcade.screen:
            for tile in row:
                if tile == TILE_TYPE.BLOCK:
                    totalBlocks += 1
                    
        print(totalBlocks)
        
        print(arcade.screen_str())