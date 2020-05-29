from typing import List, Dict

class OrbitTree(object):
    """Class representing a tree of direct orbits linked to each others"""

    def __init__(self, root:str="COM", level:int=0, nextTrees:List['OrbitTree']=[]) -> None:
        """Initiate an OrbitTree with it's root's name, it's level in the
            super-tree and it's followers"""

        self.root:str = root
        self.level:int = level
        self.nextTrees: List['OrbitTree'] = nextTrees


    def seek_subtree_by_root(self, filter:"str") -> 'OrbitTree':
        """Recursively seeks and returns a subtree by the name of its root"""

        for tree in self.nextTrees:
            if (tree.root == filter):
                return tree
            else:
                check: 'OrbitTree' = tree.seek_subtree_by_root(filter)
                if check != None:
                    return check


    def add_next(self, newTree:'OrbitTree') -> None:
        """Add a follower to this tree"""
        if newTree == None:
            pass
        else:
            newTree.level = self.level+1
            self.nextTrees.append(newTree)


    def has_followers(self) -> bool:
        """Returns wether or not this tree has any follower"""

        return len(self.nextTrees) != 0


    def checksum(self) -> int:
        """Iteratively adds every subtree's level, thus getting the orbit checksum"""

        treeStack: List[OrbitTree] = [self]
        visited : List[OrbitTree] = []

        total:int = 0
        while(len(treeStack) != 0):
            if treeStack[-1] in visited:
                treeStack.pop()
            elif not treeStack[-1].has_followers():
                total += treeStack[-1].level
                treeStack.pop()
            else:
                total += treeStack[-1].level
                visited.append(treeStack[-1])
                treeStack += treeStack[-1].nextTrees
        print(len(visited))
        return total


    def __str__(self) -> str:
        res: str = self.root + ")["
        for tree in self.nextTrees:
            res += tree.root + ", "
        return res[:-2] + "]"



def build_orbit_trees(data:Dict[str, List[str]], rootKey:str, previousTree:OrbitTree) -> OrbitTree:
    """Recursively build an orbit Tree"""

    if rootKey in data:
        if previousTree == None:
            level = 0
        else:
            level = previousTree.level+1

        newTree:OrbitTree = OrbitTree(rootKey, level, 
            [build_orbit_trees(data, n, OrbitTree(n, level)) for n in data[rootKey]])

        return newTree
    else:
        return OrbitTree(rootKey, previousTree.level+1)



with open("inputs.txt", "r+") as inputs:
    orbits: Dict[str, List[str]] = {}

    for line in inputs.readlines():
        if line[-1] == "\n":
            line = line[:-1]
        center, orbiter = line.split(")")
        if center not in orbits.keys():
            orbits[center] = [orbiter]
        else:
            orbits[center].append(orbiter)

    rootTree = build_orbit_trees(orbits, "COM", None)

    print(rootTree.checksum())