from typing import Set, Dict
from collections.abc import MutableMapping
from sys import maxsize

class OrbitNode(object):
    """Class representing a Node in an Orbit graph"""

    def __init__(self, name:str="COM", neighbors:Set[str]=set()) -> None:
        """Initializes an OrbitNode"""

        self.name:str = name
        self.neighbors:Set[str] = neighbors


    def addNeighbor(self, newNeighbor:str) -> bool:
        """Tries to add an Orbit to this Node's neighbors set, and returns
            wether or not this has been achieved"""
    
        len_buffer:int = len(self.neighbors)
        self.neighbors.add(newNeighbor)
        
        return len_buffer < len(self.neighbors)


    def __str__(self) -> str:
        """Node to string formatter"""

        res: str = self.name + ")["
        for neighbor in self.neighbors:
            res += neighbor + ", "
        return res[:-2] + "]"



def dijkstra(orbitsGraph:Dict[str, OrbitNode], sourceNodeKey:str) -> int:
    buffer: Set[str] = set()
    dist: Dict[str, int] = dict()
    prev: Dict[str, str] = dict()
    
    for nodeKey in orbitsGraph:
        dist[nodeKey] = maxsize
        prev[nodeKey] = None
        buffer.add(nodeKey)
    dist[sourceNodeKey] = 0
    
    while len(buffer) != 0:
        closerKey:str = list(buffer)[0]
        
        for nodeKey in buffer:
            if dist[nodeKey] <= dist[closerKey]:
                closerKey = nodeKey
                
        buffer.remove(closerKey)
        
        for neighbor in orbitsGraph[closerKey].neighbors:
            distanceBuffer = dist[closerKey] + 1
            
            if distanceBuffer < dist[neighbor]:
                dist[neighbor] = distanceBuffer
                prev[neighbor] = closerKey
                
    return {"dist":dist, "prev":prev}


with open("inputs.txt", "r+") as inputs:
    orbitsGraph: Dict[str, OrbitNode] = {}

    elts:Set[str] = set()

    for line in inputs.readlines():
        if line[-1] == "\n":
            line = line[:-1]
        center, orbiter = line.split(")")
        
        if center in orbitsGraph:
            orbitsGraph[center].addNeighbor(orbiter)
        else:
            orbitsGraph[center] = OrbitNode(center, {orbiter})
            
        if orbiter in orbitsGraph:
            orbitsGraph[orbiter].addNeighbor(center)
        else:
            orbitsGraph[orbiter] = OrbitNode(orbiter, {center})

    res:Dict[Dict[str, int], Dict[str, str]] = dijkstra(orbitsGraph, "YOU")

    print(int(res["dist"]["SAN"])-2)