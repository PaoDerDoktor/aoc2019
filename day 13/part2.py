from intcom import *
from typing import List, Dict, Tuple
from enum import IntEnum
from multiprocessing import Pipe, Process


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
        
        self.processorIn, self.arcadeOut = Pipe(duplex=False)
        self.arcadeIn, self.processorOut = Pipe(duplex=False)
        
        self.processor: Process = piped_intcom_as_a_process(list_to_dict(gameProg),
                                                            self.processorIn, self.processorOut)
        
        self.screen: List[List[TILE_TYPE]] = [[0 for j in range(24)] for i in range(41)]
        
        self.score: int = 0
        
        self.ballX: int = -1
        self.hPaddleX: int = -1
        
    def _refresh_screen(self) -> None:
        """Refreshes the screen and the segment data"""
        
        while self.arcadeIn.poll(0.1):
            
            x = self.arcadeIn.recv()
            y = self.arcadeIn.recv()
            if x == -1 and y == 0:
                self.score = self.arcadeIn.recv()
            else:
                t = self.arcadeIn.recv()
                if t == TILE_TYPE.BALL:
                    self.ballX = x
                elif t == TILE_TYPE.H_PADDLE:
                    self.hPaddleX = x
                self.screen[x][y] = t
                
    def getJoystickBestInput(self) -> int:
        """Returns the best joystick position"""
        
        if self.hPaddleX == self.ballX:
            return 0
        elif self.hPaddleX < self.ballX:
            return 1
        else:
            return -1
    
    def check_for_blocks(self) -> bool:
        """Returns wether or not there still is any block in the grid"""
        
        for x in self.screen:
            for y in x:
                if y == TILE_TYPE.BLOCK:
                    return True
        return False
    
    def run(self) -> None:
        """Runs the Arcade machine"""
        
        self.processor.start()
        
        while self.processor.is_alive():
            self._refresh_screen()
            
            joystickInput = self.getJoystickBestInput()
            
            try:
                self.arcadeOut.send(joystickInput)
            except EOFError:
                break
            
            if self.check_for_blocks() == False:
                break
        
        print(f"===SCORE = {self.score}===")
        self.processor.join()
            
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
        intcode[0] = 2
        
        arcade: Arcade = Arcade(intcode)
        
        arcade.run()