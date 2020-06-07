from typing import List, Dict, Tuple


def parse(lines: List[str]) -> List[Dict[str, int]]:
    """Parses the input"""
    
    coordinates: List[Dict[str, int]] = list()
        
    for line in lines:
        dataDict: Dict[str, int] = dict()
        
        if line[-1:] == "\n":
            line = line[:-1]
        
        line = line[1:-1]
        dataset = line.split(', ')
        
        for data in dataset:
            k, v = data.split('=')
            dataDict[k] = int(v)
        
        coordinates.append(dataDict)
        
    return coordinates


class System(object):
    """Class representing a gravitational system"""

    def __init__(self, objects: List[Dict[str, int]]) -> None:
        """Initializes a System with it's objects"""
        
        self.objectsXYZ: List[Dict[str, int]] = objects
        self.objectsVelocities: List[Dict[str, int]] = []
        for i in range(len(objects)):
            self.objectsVelocities.append({'x':0, 'y':0, 'z':0})
        
        self.step: int = 0

    def _apply_gravity_to(self, i: int) -> None:
        """Applies gravity to one object
        
        Arguments:
            i {int} -- The index in the System of the targetted object
        """
        
        for axis in 'xyz':
            for obj in self.objectsXYZ:
                if (obj[axis] < self.objectsXYZ[i][axis]):
                    self.objectsVelocities[i][axis] -= 1
                elif (obj[axis] > self.objectsXYZ[i][axis]):
                    self.objectsVelocities[i][axis] += 1
    
    def _apply_velocity(self, i: int) -> None:
        """Applies velocity to one object

        Arguments:
            i {int} -- The index in the System of the targetted object
        """
        
        for axis in 'xyz':
            self.objectsXYZ[i][axis] += self.objectsVelocities[i][axis]
            
    def _get_potential_energy(self, i: int) -> int:
        """Returns the computed potential energy of an object

        Arguments:
            i {int} -- The index in the System of the targetted object

        Returns:
            int -- Potential energy of given object
        """

        total: int = 0
        for axis in 'xyz':
            total += abs(self.objectsXYZ[i][axis])
        return total
    
    def _get_kinetic_energy(self, i: int) -> int:
        """Returns the computed kinetic energy of an object

        Arguments:
            i {int} -- The index in the System of the targetted object

        Returns:
            int -- Potential energy of given object
        """
        
        total: int = 0
        for axis in 'xyz':
            total += abs(self.objectsVelocities[i][axis])
        return total
    
    def _get_energy(self, i: int) -> int:
        """Returns the total energy of an object
        
        Arguments:
            i {int} -- The index in the System of the targetted object
        
        Returns:
            int -- Total energy of given object
        """
        
        return self._get_kinetic_energy(i) * self._get_potential_energy(i)
    
    def get_total_energy(self) -> int:
        """Computes total energy amount in the System
        
        Returns:
            int -- The totalenergy amount in the System
        """
        
        total: int = 0
        for i in range(len(self.objectsXYZ)):
            total += self._get_energy(i)
            
        return total
            
    def _simulate_step(self) -> None:
        """Simulates a step forward in the System"""
        
        for i in range(len(self.objectsXYZ)):
            self._apply_gravity_to(i)
        
        for j in range(len(self.objectsXYZ)):
            self._apply_velocity(j)
        
        self.step += 1
            
    def simulate_steps(self, steps: int=1) -> None:
        """Simulates given number of steps in the System

        Keyword Arguments:
            steps {int} -- Number of steps to simulate (default: {1})
        """
        
        for i in range(steps):
            self._simulate_step()


if __name__ == '__main__':
    with open("inputs.txt", "r") as inputs:
        
        objectsXYZ: List[Dict[str, int]] = parse(inputs.readlines())
        
        system: System = System(objectsXYZ)
        
        system.simulate_steps(1000)
        
        print(system.objectsXYZ)
        
        print(system.get_total_energy())