from typing import List, Dict, Tuple
from intcom import *
from multiprocessing import Pipe, Process
from multiprocessing.connection import Connection
from time import sleep


class HPRobot(object):
    """Class representing a 'Hull-Painting Robot'"""

    def __init__(self, brainCode: List[int]) -> None:
        """Initializes robot's brain, information pipes, location and movement vector."""

        brainToCamera, cameraToBrain = Pipe()
        brainToLegs, legsToBrain = Pipe()
        
        self.cameraToBrain: Connection = cameraToBrain
        self.legsToBrain: Connection = legsToBrain

        self.brain: Process = piped_intcom_as_a_process(
            list_to_dict(brainCode), brainToCamera, brainToLegs)

        self.location: Tuple[int, int] = (0, 0)
        self.directionVector: Tuple[int, int] = (0, 1)

        self.grid: Dict[int, Dict[int, str]] = {0: {0: '.'}}

    def _get_camera_output(self) -> int:
        """Returns camera output of current location"""

        return int(self.grid[self.location[0]][self.location[1]] == '#')

    def _move_to_next(self) -> None:
        """Moves the bot according to it's vector"""

        self.location = (self.location[0] + self.directionVector[0],
                         self.location[1] + self.directionVector[1])
        if self.location[0] not in self.grid:
            self.grid[self.location[0]] = {self.location[1]:'.'}
        elif self.location[1] not in self.grid[self.location[0]]:
            self.grid[self.location[0]][self.location[1]] = '.'

    def _rotate_right_angle(self, clockwise: bool) -> None:
        """Rotates the bot 90° clockwise or anti-clockwise"""

        if clockwise:
            if self.directionVector == (0, 1): # ---- --> UP
                self.directionVector = (1, 0)
            elif self.directionVector == (1, 0): # -- --> RIGHT
                self.directionVector = (0, -1)
            elif self.directionVector == (0, -1): # - --> DOWN
                self.directionVector = (-1, 0)
            elif self.directionVector == (-1, 0): # - --> LEFT
                self.directionVector = (0, 1)
        elif not clockwise:
            if self.directionVector == (0, 1): # ---- --> UP
                self.directionVector = (-1, 0)
            elif self.directionVector == (-1, 0): # - --> LEFT
                self.directionVector = (0, -1)
            elif self.directionVector == (0, -1): # - --> DOWN
                self.directionVector = (1, 0)
            elif self.directionVector == (1, 0): # -- --> RIGHT
                self.directionVector = (0, 1)

    def _paint(self, color: int) -> None:
        """Paints current location white if color==1, black if color==0"""

        if color == 0:
            self.grid[self.location[0]][self.location[1]] = '.'
        else:
            self.grid[self.location[0]][self.location[1]] = '#'

    def run(self) -> None:

        self.brain.start()
        
        while True:
            
            
            self.cameraToBrain.send(self._get_camera_output())
            
            try:
                color: int = self.legsToBrain.recv()
                self._paint(color)
            except EOFError: # If brain stopped sending
                break
            
            rotation: int = self.legsToBrain.recv()
            self._rotate_right_angle(bool(rotation))
            
            self._move_to_next()
        
        self.brain.join()


if __name__ == '__main__':
    with open("c:\\projects\\aoc2019\\day 11\\inputs.txt", "r") as inputs:
        intcode: Dict[int, int] = list_to_dict(
            [int(elt) for elt in inputs.readline().split(',')])

        robot: HPRobot = HPRobot(intcode)
        robot.run()

        total: int = 0
        for x in robot.grid:
            total += len(robot.grid[x])

        print(total)
