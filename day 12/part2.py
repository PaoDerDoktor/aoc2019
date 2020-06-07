from typing import List, Dict, Tuple, Set
from copy import deepcopy
import matplotlib.pyplot as plt
from math import gcd, prod
from pprint import pprint


def parse(lines: List[str]) -> List['Moon']:
    """Parses the input"""

    names: List[str] = ["Europe", "Io", "Callisto", "Ganymède"]
    moons: List['Moon'] = []

    for lineNmbr in range(len(lines)):
        moon: 'Moon' = Moon(names[lineNmbr], XYZ(0, 0, 0))
        
        line = lines[lineNmbr]
        
        if line[-1:] == "\n":
            line = line[:-1]
        line = line[1:-1] # Removing "<" & ">"
        
        dataset = line.split(', ')

        for axisKV in dataset:
            k, v = axisKV.split('=')
            moon.pos[k] = int(v)

        moons.append(moon)

    return moons


def lcm(l: List[int]) -> int:
    """Returns lcm of given integers"""
    
    lcm: int = l[0]
    for i in l[1:]:
        lcm = int(lcm*i/gcd(lcm, i))
    return lcm


class XYZ(object):
    """Structure to contain XYZ values"""
    
    def __init__(self, x: int, y: int, z: int) -> None:
        """Builds a structure from XYZ value"""
        
        self.x = x
        self.y = y
        self.z = z
        
    def __getitem__(self, axis: str) -> int:
        """Returns x, y or z axis if correct string is sent"""
        
        if axis == 'x':
            return self.x
        elif axis == 'y':
            return self.y
        elif axis == 'z':
            return self.z
        else:
            raise KeyError(f"XYZ struct doesn't have any XYZ[{axis}] element.")
        
    def __setitem__(self, axis: str, val: int) -> None:
        """Sets x, y or z axis by a value"""
        
        if axis == 'x':
            self.x = val
        elif axis == 'y':
            self.y = val
        elif axis == 'z':
            self.z = val
        else:
            raise KeyError(f"XYZ struct doesn't have any XYZ[{axis}] element.")
        
    def __str__(self) -> str:
        """Stringify the XYZ object"""
        
        return f"XYZ(x={self.x}, y={self.y}, z={self.z})"
        
    def get_copy(self) -> 'XYZ':
        """Returns a copy of the structure"""
        
        return XYZ(self.x, self.y, self.z)


class Moon(object):
    """Class representing a moon"""
    
    def __init__(self, name: str, pos: XYZ, vel: XYZ=XYZ(0, 0, 0)) -> None:
        """Builds a moon from a name and a position"""
        
        self.name = name
        self.pos = pos.get_copy()
        self.vel = XYZ(0, 0, 0)
        
    def __str__(self) -> str:
        """Stringify the Moon object"""
        
        return f"Moon(name='{self.name}', pos={self.pos}, vel={self.vel})"
        
    def get_copy(self) -> 'Moon':
        """Returns a copy of the structure"""
        
        return Moon(self.name, self.pos.get_copy(), self.vel.get_copy())
    

class System(object):
    """Class representing moon system"""
    
    def __init__(self, moons: List[Moon]) -> None:
        """Builds a system from a list of moon"""
        
        self.moons: List[Moon] = deepcopy(moons)
        self.moonNumber: int = len(moons)
        self.step: int = 0
        
        self.cache: List[List[Moon]] = [[moon.get_copy() for moon in moons]]
    
    def __str__(self) -> str:
        """Stringify the System object"""
        
        res: str = "System(moons=["
        for moon in self.moons:
            res += str(moon) + ", "
        res = res[:-1]
        return res + f"], step={self.step})"
    
    def get_copy(self) -> 'System':
        """Returns a copy of the System object"""
        
        systemCopy = System(self.moons)
        systemCopy.step = self.step
        systemCopy.cache = self.cache
        
        return systemCopy
    
    def _apply_gravity(self) -> None:
        """Applies gravity to the moons's velocities"""
        
        for moon in self.moons:
            for otherMoon in self.moons:
                for axis in 'xyz':
                    if moon.pos[axis] < otherMoon.pos[axis]:
                        moon.vel[axis] += 1
                    elif moon.pos[axis] > otherMoon.pos[axis]:
                        moon.vel[axis] -= 1
    
    def _apply_velocity(self) -> None:
        """Applies their velocities to each planets"""
        
        for moon in self.moons:
            for axis in 'xyz':
                moon.pos[axis] += moon.vel[axis]
                
    def simulate_once(self) -> None:
        """Simulate forward by one step"""
        
        self._apply_gravity()
        self._apply_velocity()
        
        self.cache.append([moon.get_copy() for moon in self.moons])
        
        self.step += 1
        
    def simulate_multi(self, n: int) -> None:
        """Simulate a given number of steps"""
        
        for i in range(n):
            self.simulate_once()
        
if __name__ == '__main__':
    with open('C:\\projects\\aoc2019\\day 12\\inputs.txt', 'r') as inputs:
        moonOrigins: List[Moon] = parse(inputs.readlines())
        system: System = System(moonOrigins)
        
        for moon in system.moons:
            print(moon)
            
        print("====SIMULATION====")
        system.simulate_multi(1000000)
        
        for moon in system.moons:
            print(moon)
            
        print("====SIM DETAILS====")
        print(f"cache length : {len(system.cache)}")
        print(f"current step : {system.step}")
        
    backToNormalStepsMask: List[List[bool]] = []
    
    for pastSituation in system.cache:
        dimMask: List[bool] = []
        
        for axis in 'xyz':
            if (pastSituation[0].pos[axis] == system.cache[0][0].pos[axis] and pastSituation[0].vel[axis] == 0 and
                    pastSituation[1].pos[axis] == system.cache[0][1].pos[axis] and pastSituation[1].vel[axis] == 0 and
                    pastSituation[2].pos[axis] == system.cache[0][2].pos[axis] and pastSituation[2].vel[axis] == 0 and
                    pastSituation[3].pos[axis] == system.cache[0][3].pos[axis] and pastSituation[3].vel[axis] == 0):
                dimMask.append(True)
            else:
                dimMask.append(False)
        backToNormalStepsMask.append(dimMask)
        
    trueIndexes: Dict[int, List[bool]] = {}
    
    for pastSituationIndex in range(len(backToNormalStepsMask)):
        if bool(sum(backToNormalStepsMask[pastSituationIndex])) == True:
            trueIndexes[pastSituationIndex] = backToNormalStepsMask[pastSituationIndex]
    
    print("====TRUE INDEXES====")
    for index in trueIndexes.keys():
        print(f"{index} : {trueIndexes[index]}")
        
    axisPeriods: List[int] = [None, None, None]
    
    for index in trueIndexes.keys():
        for axis in range(3):
            if (trueIndexes[index][axis] == True and index-1 in trueIndexes):
                if (trueIndexes[index-1][axis] == True and axisPeriods[axis] == None):
                    axisPeriods[axis] = index
                    
    print(lcm(axisPeriods))