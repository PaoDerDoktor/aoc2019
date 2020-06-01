from typing import List, Any, Dict, Tuple
from math import sqrt

class GridVect(object):
    """Class representing a 2D Vector"""

    def __init__(self, x: int, y: int) -> None:
        self.x: int = x
        self.y: int = y

    def __add__(self, o: Any) -> 'GridVect':
        if isinstance(o, GridVect):
            return GridVect(self.x + o.x, self.y + o.y)

    def __mul__(self, o: Any) -> 'GridVect':
        if isinstance(o, float) or isinstance(o, int):
            return GridVect(self.x*o, self.y*o)
        elif isinstance(o, GridVect):
            return self.x*o.x + self.y*o.y

    def __str__(self) -> str:
        return f"GridVect({self.x}, {self.y})"
    
    def __eq__(self, o:Any) -> bool:
        if not isinstance(o, GridVect):
            return False
        else:
            return self.x == o.x and self.y == o.y

    def colinearity(self, o: 'GridVect') -> bool:
        """Checks if this vector and the one that is passed are colinear"""

        return (self.x*o.y - o.x*self.y) == 0
    
    def get_magnitude(self) -> float:
        """Returns the vector's length"""
        
        return sqrt(pow(self.x, 2) + pow(self.y, 2))
    
    def get_unit_dim(self) -> List[float]:
        """Returns a 2-uple containing x and y values of the vector's unit representation"""
        
        mag: float = self.get_magnitude()
        return [self.x/mag, self.y/mag]
    
    def same_direction(self, ov: 'GridVect') -> bool:
        """Returns wether or not this vector and the one passed have the same direction"""
        
        if self == ov:
            return True
        elif self.x == 0 or ov.x == 0:
            if self.x == ov.x == 0:
                return self.y*ov.y >= 0
            else:
                return False
        elif self.y == 0 or ov.y == 0:
            if self.y == ov.y == 0:
                return self.x*ov.x >= 0
            else:
                return False
        elif self.x*ov.x < 0 or self.y*ov.y < 0:
            return False
        else:
            return self.x/self.y == ov.x/ov.y
        
        #return self.get_unit_dim() == ov.get_unit_dim()

class GridPoint(object):
    """Class representing a 2D Point"""

    def __init__(self, x: int, y: int) -> None:
        self.x: int = x
        self.y: int = y

    def __str__(self) -> str:
        return f"GridPoint({self.x}, {self.y})"
    
    def __eq__(self, o:Any) -> bool:
        if not isinstance(o, GridPoint):
            return False
        else:
            return o.x == self.x and o.y == self.y


class GridRay(object):
    """Class representing a 2D Ray"""

    def __init__(self, origin: GridPoint, direction: GridVect) -> None:
        self.origin: GridPoint = origin
        self.direction: GridVect = direction

    def __str__(self) -> str:
        return f"Ray[{self.origin}->{self.direction}]"

    def intersect_grid_at(self, x: int, y: int) -> bool:
        """Returns wether or not the ray cross perfectly specified grid location"""

        checkVect: GridVect = GridVect(x - self.origin.x, y - self.origin.y)

        return self.direction.same_direction(checkVect)


class RayCaster(object):
    """Class organizing a ray casting"""

    def __init__(self, grid: List[List[str]]):
        self.grid: List[List[int]] = grid
        self.currentOrigin: GridPoint = None

    def get_asteroids_locations(self) -> List[GridPoint]:
        """Returns the list of every asteroid's location"""

        asteroids_locations: List[GridPoint] = list()
        for y in range(len(self.grid)):
            for x in range(len(self.grid[0])):
                if self.grid[y][x] == "#":
                    asteroids_locations.append(GridPoint(x, y))

        return asteroids_locations

    def access_grid_from_point(self, point: GridPoint) -> str:
        """Returns the value in the grid of a given point"""

        return self.grid[point.y][point.x]

    def _cast_rays(self) -> int:
        asteroids: List[GridPoint] = self.get_asteroids_locations()
        asteroids.remove(self.currentOrigin)

        uniqueHittingRays: List[GridRay] = list()

        for asteroid in asteroids:
            ray: GridRay = GridRay(self.currentOrigin, GridVect(
                asteroid.x - self.currentOrigin.x, asteroid.y - self.currentOrigin.y))

            colinear: bool = False
            for uniqueHittingRay in uniqueHittingRays:
                if uniqueHittingRay.direction.same_direction(ray.direction):
                    colinear = True
                    break

            if not colinear:
                uniqueHittingRays.append(ray)

        return len(uniqueHittingRays)

    def run(self) -> Dict[str, Any]:
        """Runs the RayCaster and returns the best location"""

        possible_origins: List[Point] = self.get_asteroids_locations()

        bestLocation: GridPoint = GridPoint(0, 0)
        bestMonitored: int = -1

        for origin in possible_origins:
            self.currentOrigin = origin
            
            currentMonitored: int = self._cast_rays()

            if currentMonitored > bestMonitored:
                bestMonitored = currentMonitored
                bestLocation = self.currentOrigin

        return {"location":bestLocation, "monitored":bestMonitored}

with open("C:\\projects\\aoc2019\\day 10\\inputs.txt", "r") as inputs:
    input: List[List[str]] = [list(i[:-1]) for i in inputs.readlines()]

    rc: RayCaster = RayCaster(input)
    res = rc.run()
    print(res["location"], res["monitored"])