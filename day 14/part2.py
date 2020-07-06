from typing import List, Dict, Tuple
from pprint import pprint
from math import ceil
from sys import maxsize
from copy import deepcopy
import matplotlib.pyplot as plt


def parse(lines: List[str]) -> Dict[str, Tuple[int, Dict[str, int]]]:
    """Parses input file"""

    recipes: Dict[str, Tuple[int, Dict[str, int]]] = {}
    for rawLine in lines:
        if rawLine[-1] == "\n":
            line = rawLine[:-1]
        else:
            line = rawLine

        ingredientsStr, resultStr = line.split(' => ')

        resultMultiplier, resultKey = resultStr.split(' ')
        resultMultiplier = int(resultMultiplier)

        ingredientsDict: Dict[str, int] = {}

        for ingredientStr in ingredientsStr.split(', '):
            ingredientMultiplier, ingredientKey = ingredientStr.split(' ')
            ingredientMultiplier = int(ingredientMultiplier)

            ingredientsDict[ingredientKey] = ingredientMultiplier
        recipes[resultKey] = (resultMultiplier, ingredientsDict)
    return recipes

def create_inventory(recipes: Dict[str, Tuple[int, Dict[str, int]]]) -> Dict[str, int]:
    """Creates an inventory able to contain a set of recipe's possible leftovers

    Args:
        recipes (Dict[str, Tuple[int, Dict[str, int]]]): Set of recipes

    Returns:
        Dict[str, int]: A dictionnary mapping every of the recipe set's outputs to an amount
    """
    
    inventory: Dict[str, int] = {}
    for outputKey in recipes:
        inventory[outputKey] = 0
        
    return inventory

def cost(recipes: Dict[str, Tuple[int, Dict[str, int]]], neededKey: str, neededAmount: int, leftovers: Dict[str, int]) -> int:
    """Computes the ORE cost of a given product amount, given recipes and leftovers

    Args:
        recipes (Dict[str, Tuple[int, Dict[str, int]]]): Dictionary of recipes
        neededKey (str): The key (in the recipes) of the product to build
        neededAmount (int): The amount of the product to build
        leftovers (Dict[str, int]): The leftovers already present in the nano-factory

    Returns:
        int: The ORE amount computed
    """
    
    if neededKey == "ORE":
        return neededAmount
    
    ingredients: Dict[str, int] = recipes[neededKey][1]
    productAmountByOp: int = recipes[neededKey][0]
    availableAmount: int = leftovers[neededKey]
    
        # MANAGING LEFTOVERS
        
    if availableAmount >= neededAmount:
        leftovers[neededKey] -= neededAmount
        return 0
    
    leftovers[neededKey] = 0
    neededAmount -= availableAmount
        
        # COMPUTING NUMBER OF REACTIONS
        
    reactionsAmount: int = ceil(neededAmount / productAmountByOp)

        # PUTTING UNUSED INTO LEFTOVERS
        
    leftovers[neededKey] += (reactionsAmount*productAmountByOp) - neededAmount
    
        # RECURSIVE CALL TO GET INGREDIENTS'S COSTS
        
    totalCost: int = 0
    for ingredientKey in ingredients.keys():
        ingredientNeededAmount: int = ingredients[ingredientKey] * reactionsAmount
        totalCost += cost(recipes, ingredientKey, ingredientNeededAmount, leftovers)
        
    return totalCost


if __name__ == '__main__':
    with open("C:\\Projects\\aoc2019\\day 14\\inputs.txt", 'r') as inputs:
        recipes: Dict[str, Tuple[int, Dict[str, int]]] = parse(inputs)
        
        print("cost for one fuel =", cost(recipes, "FUEL", 1, create_inventory(recipes)))
        print("===COUNTING===")
        
        leftOre: int = 1000000000000
        
        leftovers: Dict[str, int] = create_inventory(recipes)
        
        initialCost: int = cost(recipes, "FUEL", 1, create_inventory(recipes))
        
        totalBuiltFuel: int = 0
        
        while leftOre // initialCost > 0:
            productsCost = cost(recipes, "FUEL", (leftOre // initialCost), leftovers)
            print("endedOne")
            totalBuiltFuel += leftOre // initialCost
            leftOre -= productsCost
            
        productsCost = cost(recipes, "FUEL", 1, leftovers)
        
        while productsCost <= leftOre:
            leftOre -= productsCost
            totalBuiltFuel += 1
            productsCost = cost(recipes, "FUEL", 1, leftovers)
            
        print("total built fuel =", totalBuiltFuel)
        