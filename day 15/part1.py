from intcom import Intcom, piped_intcom_as_a_process, list_to_dict
from multiprocessing import Pipe, Process
from multiprocessing.connection import PipeConnection
from typing import List, Dict, Tuple, Set, Union
from sys import maxsize


# A tile is a 2-int-tuple containing X and Y coordinates (0,0) being the starting tile
Tile = Tuple[int, int]


class Droid(object):
    """Class representing a repair droid"""
    
    def __init__(self, remoteCode: List[int]) -> None:
        """Initialize the repair droid with an intcode"""
        
        remoteIn, droidOut = Pipe(duplex=False)
        droidIn, remoteOut = Pipe(duplex=False)
        
        startingTile: Tile = (0, 0)
        
        self.remoteIn: PipeConnection = remoteIn
        self.remoteOut: PipeConnection = remoteOut
        
        self.droidIn: PipeConnection = droidIn
        self.droidOut: PipeConnection = droidOut
        
        self.remote: Process = piped_intcom_as_a_process(list_to_dict(remoteCode),
                                                         self.remoteIn, self.remoteOut)
        
        self.wallTiles: Set[Tile] = set()
        self.emptyTiles: Set[Tile] = set({startingTile}) # Starting tile is always empty
        self.unknownTiles: List[Tile] = [] # Stack, should start as [(-1, 0), (0, -1), (1, 0)]
        self.path: List[Tile] = [] # First path should simply be [(0, 1)]
        
        self.droidTile: Tile = startingTile
        self.oxygenTile: Tile = None
        
        self.shortestPathLength: int = 0
        
    def _tile_is_marked(self, tile: Tile) -> bool:
        """Returns wether or not given tile is already marked as a wall, empty or unknown"""
        
        return ((tile in self.unknownTiles) or (tile in self.emptyTiles) or
                (tile in self.wallTiles))
    
    def _get_nearby_tiles(self, tile: Tile=None) -> List[Tile]:
        """Returns a list containing every tiles located directly left, right, up or under
           a given tile"""
           
        if tile == None:
            tile = self.droidTile
        
        offsetsList: List[Tuple[int, int]] = [(-1,0), (0,-1), (1,0), (0,1)]
        nearbyTiles: List[Tuple[int, int]] = []
        
        for offset in offsetsList:
            nearbyTiles.append((tile[0] + offset[0],
                                tile[1] + offset[1]))
            
        return nearbyTiles
    
    def _get_possible_moves(self, testedTiles: List[Tile]) -> List[Tile]:
        """Returns a list of every tile in the list that is empty"""
        
        possibleMoves: List[Tile] = []
        
        for tile in testedTiles:
            if tile in self.emptyTiles:
                possibleMoves.append(tile)
                
        return possibleMoves
        
    def _mark_unknown_tiles(self) -> None:
        """Adds nearby unmarked tiles to the unknown tiles's stack"""
        
        for nearbyTile in self._get_nearby_tiles():
            if not self._tile_is_marked(nearbyTile):
                self.unknownTiles.append(nearbyTile)
                
    def _dijkstra(self, start: Tile, end: Tile) -> Dict[str, Union[Dict[Tile, int], Dict[Tile, Tile]]]:
        """Dijkstra algorithm to find best path between a starting tile and an end tile"""
        
        buffer: Set[Tile] = set()
        distance: Dict[Tile, int] = {}
        fathers: Dict[Tile, Tile] = {}
        
        for tile in self.emptyTiles.union({end}):
            distance[tile] = maxsize
            fathers[tile] = None
            buffer.add(tile)
        distance[start] = 0
        
        while len(buffer) > 0:
            closestTile: Tile = list(buffer)[0]
            
            for tile in buffer:
                if distance[tile] <= distance[closestTile]:
                    closestTile = tile
                    
            buffer.remove(closestTile)
            
            for tile in self._get_possible_moves(self._get_nearby_tiles(closestTile)):
                distanceBuffer: int = distance[closestTile]+1
                
                if distanceBuffer < distance[tile]:
                    distance[tile] = distanceBuffer
                    fathers[tile] = closestTile
                    
        return {"distance": distance, "fathers": fathers}
    
    def _get_path_from_dijkstra(self, fathers: Dict[Tile, Tile], end: Tile) -> List[Tile]:
        """Returns the path needed to go from dijkstra's starting tile to given end tile"""
        
        path: List[Tile] = [end]
        currentTile: Tile = end
        
        while fathers[currentTile] != None:
            currentTile = fathers[currentTile]
            path.append(currentTile)
            
        return path[::-1]
    
    def _get_mov_command(self, start: Tile, destination: Tile) -> int:
        """Returns the movement command required to move from a starting
           tile to a given destination"""
           
        if start == None:
            start = self.droidTile
           
        offsetToCommand: Dict[Tuple[int, int], int] = {
            (0,-1): 3, (-1,0): 2, (0,1): 4, (1,0): 1
        } #  West       South      East      North
        
        destinationOffset = (destination[0] - self.droidTile[0],
                             destination[1] - self.droidTile[1])
        
        return offsetToCommand[destinationOffset]
    
    def _apply_movement(self, destination: Tile, status: int) -> None:
        """Applies movement : change the droid's location if needed, store the
           destination in the right set given a destination and a status"""
        
        if status == 0: # Hit a wall
            print("wall")
            self.wallTiles.add(destination)
        else:
            if status == 2:
                self.oxygenTile = destination
            
            self.droidTile = destination
            self.emptyTiles.add(destination)
           
    def run(self) -> None:
        """Runs the droid's program"""
        
        self.remote.start()
        
        started: bool = False
        while (not started) or (len(self.unknownTiles) > 0):
            print(self.droidTile)
            
            started = True

            if len(self.path) == 0:
                self._mark_unknown_tiles()
                
                nextTarget: Tile = self.unknownTiles.pop()
                
                print("target =",nextTarget)
                
                self.path = self._get_path_from_dijkstra(
                    self._dijkstra(self.droidTile, nextTarget)["fathers"], nextTarget
                )
                
            destination: Tile = self.path.pop()
            
            movCommand: int = self._get_mov_command(None, destination)
            
            self.droidOut.send(movCommand)
            status: int = self.droidIn.recv()
            
            self._apply_movement(destination, status)

        self.remote.kill()
        
        self.shortestPathLength = self._dijkstra((0,0), self.oxygenTile)["distance"][self.oxygenTile]
        
if __name__ == "__main__":
    with open("C:\\Projects\\aoc2019\\day 15\\inputs.txt", "r") as inputs:
        intcode = [int(elt) for elt in inputs.readline().split(',')]
        
        droid: Droid = Droid(intcode)
        
        droid.run()
        
        print(droid.shortestPathLength)