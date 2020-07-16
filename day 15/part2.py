from intcom import Intcom, piped_intcom_as_a_process, list_to_dict
from multiprocessing import Pipe, Process
from multiprocessing.connection import PipeConnection
from typing import List, Dict, Tuple, Set, Union
from sys import maxsize
from queue import Queue


# A tile is a 2-int-tuple containing X and Y coordinates (0,0) being the starting tile
Tile = Tuple[int, int]


class Droid(object):
    """Class representing a repair droid"""

    def __init__(self, remoteCode: List[int]) -> None:
        """Initialize the repair droid with an intcode"""

        remoteIn, droidOut = Pipe(duplex=False)
        droidIn, remoteOut = Pipe(duplex=False)

        startingTile: Tile = (0, 0)

        self.droidIn: PipeConnection = droidIn
        self.droidOut: PipeConnection = droidOut

        self.remote: Process = piped_intcom_as_a_process(list_to_dict(remoteCode),
                                                         remoteIn, remoteOut)

        self.wallTiles: Set[Tile] = set()
        # Starting tile is always empty
        self.emptyTiles: Set[Tile] = set({startingTile})
        # Stack, should start as [(-1, 0), (0, -1), (1, 0)]
        self.unknownTiles: List[Tile] = []
        self.path: List[Tile] = []  # First path should simply be [(0, 1)]

        self.droidTile: Tile = startingTile
        self.oxygenTile: Tile = None

        self.shortestPathLength: int = 0
        self.fillingTime: int = 0

    def _get_nearby_from(self, location: Tile) -> List[Tile]:
        """Returns every tiles directly south, north, east and west from a given tile"""

        return [
            (location[0]-1, location[1]),
            (location[0],   location[1]-1),
            (location[0]+1, location[1]),
            (location[0],   location[1]+1)
        ]

    def _get_possible_moves(self, tiles: List[Tile]) -> List[Tile]:
        """Returns a list containing every tile from a given list to which the droid can move
           for sure"""

        return [t for t in tiles if t in self.emptyTiles]

    def _get_unmarked(self, tiles: List[Tile]) -> List[Tile]:
        """Returns a list containing every tile from a given list that are not marked"""

        return [t for t in tiles if t not in self.emptyTiles.union(set(self.unknownTiles)).union(self.wallTiles)]

    def _mark_as_unknown(self, tiles: List[Tile]) -> None:
        """Marks every tile in the list as unknown"""

        self.unknownTiles.extend(
            [t for t in tiles if t not in self.unknownTiles])

    def _dijkstra(self, start: Tile, end: Tile) -> List[Tile]:
        """Dijkstra search algorithm, usable as a pathfinding algorithm by the droid"""

        distance: Dict[Tile, int] = {}
        parent: Dict[Tile, Tile] = {}
        unexplored: Set[Tile] = set(self.emptyTiles).union(
            set(self._get_possible_moves(self._get_nearby_from(start)))).union({end})

        for emptyTile in unexplored:
            distance[emptyTile] = maxsize
            parent[emptyTile] = None

        distance[start] = 0

        while len(unexplored) > 0:
            minDistance: int = maxsize
            minDistanceTile: Tile = None

            for testedTile in unexplored:
                if distance[testedTile] <= minDistance:
                    minDistanceTile = testedTile
                    minDistance = distance[testedTile]

            unexplored.remove(minDistanceTile)

            if minDistanceTile == end:
                path: List[Tile] = [end]
                currentParent = parent[end]
                while currentParent != None:
                    path.append(currentParent)
                    currentParent = parent[currentParent]
                return path[:-1]

            neighbors: List[Tile] = self._get_possible_moves(
                self._get_nearby_from(minDistanceTile))
            if end in self._get_nearby_from(minDistanceTile) and end not in neighbors:
                neighbors.append(end)

            for neighbor in neighbors:
                if neighbor in unexplored:
                    newDistance: int = distance[minDistanceTile] + 1

                    if newDistance < distance[neighbor]:
                        parent[neighbor] = minDistanceTile
                        distance[neighbor] = newDistance
                        
    def _dijkstra_complete_eval(self, source: Tile) -> Dict[str, Union[Dict[Tile, Tile], Dict[Tile, int]]]:
        """Dijkstra algorithm implemented so that it associate a distance to
           every node"""
           
        distance: Dict[Tile, int] = {}
        parent: Dict[Tile, Tile] = {}
        unexplored: Set[Tile] = set(self.emptyTiles)
        
        for emptyTile in unexplored:
            distance[emptyTile] = maxsize
            parent[emptyTile] = None
            
        distance[source] = 0
        
        while len(unexplored) > 0:
            minDistance: int = maxsize
            minDistanceTile: Tile = None
            
            for testedTile in unexplored:
                if distance[testedTile] <= minDistance:
                    minDistanceTile = testedTile
                    minDistance = distance[testedTile]
                    
            unexplored.remove(minDistanceTile)
            
            for neighbor in self._get_possible_moves(self._get_nearby_from(minDistanceTile)):
                if neighbor in unexplored:
                    newDistance: int = distance[minDistanceTile] + 1

                    if newDistance < distance[neighbor]:
                        parent[neighbor] = minDistanceTile
                        distance[neighbor] = newDistance
                        
        return {'parent': parent, 'distance': distance}

    def _apply_mov(self, destination: Tile, status: int) -> None:
        """Apply a movement given a destination and a status"""

        if status == 0:  # The destination is a wall tile
            print("wall !")
            self.wallTiles.add(destination)
        else:
            self.droidTile = destination
            if status == 1:  # The destination is an empty tile
                self.emptyTiles.add(destination)
            else:  # The destination is the oxygen tile
                print("found oxygen !")
                self.emptyTiles.add(destination)
                self.oxygenTile = destination

    def _get_mov_command(self, destination: Tile) -> None:
        """Returns the command needed to go from the droid's location to a destination"""

        offset = (destination[0] - self.droidTile[0],
                  destination[1] - self.droidTile[1])

        if offset == (-1, 0):  # West
            return 3
        elif offset == (0, -1):  # South
            return 2
        elif offset == (1, 0):  # East
            return 4
        elif offset == (0, 1):  # North
            return 1
        else:
            raise ValueError(f"Offset is not valid : {offset}")

    def searchForDoubles(self):
        return len(self.unknownTiles) != len(set(self.unknownTiles))

    def run(self) -> None:

        self.remote.start()

        started: bool = False
        self._mark_as_unknown(self._get_unmarked(
            self._get_nearby_from(self.droidTile)))

        i: int = 0  # iter counter

        while not started or len(self.unknownTiles) > 0:
            started = True
            i += 1
            print("ITER :", i)

            print("start =", self.droidTile)

            if len(self.path) == 0:
                print("renewing path")
                nextTarget: Tile = self.unknownTiles.pop()
                while nextTarget == self.droidTile:
                    nextTarget = self.unknownTiles.pop()
                print("unknownTiles check =", nextTarget in self.unknownTiles)

                self.path = self._dijkstra(self.droidTile, nextTarget)

            destination: Tile = self.path.pop()

            self.droidOut.send(self._get_mov_command(destination))

            self._apply_mov(destination, self.droidIn.recv())

            self._mark_as_unknown(self._get_unmarked(
                self._get_nearby_from(self.droidTile)))
            print("stop =", self.droidTile)

        self.remote.kill()

        self.shortestPathLength = len(self._dijkstra((0, 0), self.oxygenTile))
        
        # Now getting filling time
        
        fillingTime: int = 0
        distance: Dict[Tile, int] = self._dijkstra_complete_eval(self.oxygenTile)['distance']
        
        for tile in distance.keys():
            if fillingTime < distance[tile]:
                fillingTime = distance[tile]
                
        self.fillingTime = fillingTime


if __name__ == "__main__":
    with open("C:\\Projects\\aoc2019\\day 15\\inputs.txt", "r") as inputs:
        intcode = [int(elt) for elt in inputs.readline().split(',')]

        droid: Droid = Droid(intcode)

        droid.run()
        print("=== FINISHED CARTOGRAPHY ===")
        print("Oxygen distance :", droid.shortestPathLength)
        print("Filling time :", droid.fillingTime)