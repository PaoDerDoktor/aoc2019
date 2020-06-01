from typing import List, Any, Dict, Tuple, Iterator, Generic, VT
from math import sqrt, atan2, cos, sin, pi
from copy import deepcopy


# CLASSES


class PolarPoint(object):
    """Data structure representing a point in a polar grid"""

    def __init__(self, distance: float, angle: float) -> None:
        self.distance: float = distance
        self.angle: float = angle

    def __str__(self) -> str:
        return f"PolarPoint(r={self.distance}, t={self.angle})"

    def __eq__(self, o: Any) -> bool:
        if not isinstance(o, PolarPoint):
            return False
        else:
            return self.distance == o.distance and self.angle == o.angle


class GridPoint(object):
    """Class representing a 2D Point"""

    def __init__(self, x: int, y: int) -> None:
        self.x: int = x
        self.y: int = y

    def __str__(self) -> str:
        return f"GridPoint({self.x}, {self.y})"

    def __eq__(self, o: Any) -> bool:
        if not isinstance(o, GridPoint):
            return False
        else:
            return o.x == self.x and o.y == self.y


class Grid(Generic[VT]):
    """Simple class representing a grid"""

    def __init__(self, grid: List[List[VT]]) -> None:
        self.grid: List[List[VT]] = grid

    def __getitem__(self, key: GridPoint) -> VT:
        return self.grid[key.x][key.y]

    def __getitem__(self, key: int) -> VT:
        return self.grid[key]

    def __setitem__(self, key: GridPoint, val: VT) -> None:
        self.grid[key.x][key.y] = val

    def __iter__(self) -> Iterator:
        return iter(self.grid)

    def __len__(self) -> int:
        return len(self.grid)

    def count_asteroids(self) -> int:
        """Returns the total count of '#' in the grid"""
        total: int = 0
        for col in grid:
            for char in col:
                if char == '#':
                    total += 1
        return total


class PolarGrid(object):
    """Class representing a polar grid for more convenience when studying Polar Coordinates"""

    def __init__(self, pole: GridPoint, axis: Tuple[float, float] = (0, -1), correct: bool = True) -> None:
        self.pole: GridPoint = pole
        self.axis: Tuple[float, float] = axis
        self.correct = True  # correcting the offset of the axis when converting

    def convert_grid_point_to_polar_point(self, point: GridPoint) -> PolarPoint:
        return PolarPoint(sqrt(pow(point.x - self.pole.x, 2) + pow(point.y - self.pole.y, 2)),
                          atan2(point.x - self.pole.x, point.y - self.pole.y))

    def convert_polar_point_to_grid_point(self, point: PolarPoint) -> GridPoint:
        if not self.correct:
            return GridPoint(round(self.pole.x + point.distance*cos(point.angle)),
                             round(self.pole.y + point.distance*sin(point.angle)))
        else:
            return GridPoint(round(self.pole.x + point.distance*sin(point.angle)),
                             round(self.pole.y + point.distance*cos(-point.angle)))

        # FUNCTIONS


def correct_grid_dim_order(grid: List[List[VT]]) -> List[List[VT]]:
    """Corrects passed [y][x]-accessible grid by making it [x][y], returns the result"""

    return [list(i) for i in zip(*grid)]


def pretty_str_corrected_grid(grid: Grid) -> str:
    """Returns a "Pretty-print" string representing a [x][y]-accessible grid"""

    res: str = ''
    for y in range(len(grid[0])):
        for x in range(len(grid)):
            res += str(grid[x][y])
        res += '\n'

    return res


def get_all_detected_asteroids_from(location: GridPoint, grid: Grid) -> Dict[float, PolarPoint]:
    """Returns every asteroids detected from a given location as a list of polar points"""

    detectedAsteroids: Dict[float, PolarPoint] = {}
    polarGrid: PolarGrid = PolarGrid(location)

    for x in range(len(grid)):
        for y in range(len(grid)):
            if grid[x][y] == "#" and (x, y) != (location.x, location.y):
                pt: PolarPoint = polarGrid.convert_grid_point_to_polar_point(
                    GridPoint(x, y))

                if (pt.angle not in detectedAsteroids.keys() or
                        detectedAsteroids[pt.angle].distance > pt.distance):
                    detectedAsteroids[pt.angle] = pt

    return detectedAsteroids


def paint_all_detected_asteroids_from(location: GridPoint, grid: Grid) -> List[GridPoint]:
    """Returns every asteroids detected from a given location as a list of polar points. Also paints the grid with destruction infos"""

    detectedAsteroids: Dict[float, PolarPoint] = {}
    polarGrid: PolarGrid = PolarGrid(location)

    grid[location] = "X"

    for x in range(len(grid)):
        for y in range(len(grid)):
            if grid[x][y] == "#" and (x, y) != (location.x, location.y):
                pt: PolarPoint = polarGrid.convert_grid_point_to_polar_point(
                    GridPoint(x, y))

                if (pt.angle not in detectedAsteroids.keys() or
                        detectedAsteroids[pt.angle].distance > pt.distance):
                    detectedAsteroids[pt.angle] = pt

    angleToGridPoint: Dict[float, GridPoint] = {}
    for angle in detectedAsteroids:
        pt: GridPoint = polarGrid.convert_polar_point_to_grid_point(
            detectedAsteroids[angle])
        grid[pt] = '@'
        angleToGridPoint[angle] = pt

    sortedAngles: List[float] = list(angleToGridPoint.keys())
    sortedAngles.sort()

    negAngles: List[GridPoint] = []
    posAngles: List[GridPoint] = []

    for angle in sortedAngles:
        if angle >= 0:
            posAngles.append(angleToGridPoint[angle])
        else:
            negAngles.insert(0, angleToGridPoint[angle])

    return posAngles+negAngles


def get_best_station_location(grid: Grid) -> Tuple[GridPoint, int]:
    """Return the location of the asteroid having the most direct line-of-sights with other asteroids, with the number of it's detectable asteroids"""

    bestAmmount: int = -1
    bestLocation: GridPoint = None
    for x in range(len(grid)):
        for y in range(len(grid)):
            if grid[x][y] == "#":
                pt: GridPoint = GridPoint(x, y)
                localAmmount: int = len(
                    get_all_detected_asteroids_from(pt, grid))

                if bestAmmount < localAmmount:
                    bestAmmount = localAmmount
                    bestLocation = pt

    return (bestLocation, bestAmmount)


def obliterate(grid: Grid, stationLocation: GridPoint) -> List[GridPoint]:
    """E X T E R M I N A T U S"""

    log: List[GridPoint] = []
    while grid.count_asteroids() > 0:
        log += paint_all_detected_asteroids_from(stationLocation, grid)
        
    return log

# MAIN


with open("C:\\projects\\aoc2019\\day 10\\inputs.txt", "r") as inputs:
    rawGrid: List[List[str]] = [list(i[:-1]) for i in inputs.readlines()]

    grid: Grid = Grid(correct_grid_dim_order(rawGrid))

    bestStationLocation, bestStationDetectionsAmmout = get_best_station_location(
        grid)

    print("Best station's location :", bestStationLocation)
    print("Best station's detections ammount :", bestStationDetectionsAmmout)

    log: List[GridPoint] = obliterate(grid, bestStationLocation)
    
    twoHundredth: GridPoint = log[199]
    
    print(twoHundredth.x*100 + twoHundredth.y)
    
    #I'm never doing it again.