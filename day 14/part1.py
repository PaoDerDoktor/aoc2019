from typing import List, Dict, Tuple
from pprint import pprint
from math import ceil


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


def init_inventory(recipes: Dict[str, Tuple[int, Dict[str, int]]]) -> Dict[str, int]:
    """Initialize an inventory"""

    inventory: Dict[str, int] = {}
    for itemKey in recipes.keys():
        inventory[itemKey] = 0
    return inventory


def find_required_ore_amount_for(key: str, recipes: Dict[str, Tuple[int, Dict[str, int]]],
                                 inventory: Dict[str, int], logger: Dict[str, int]) -> int:
    """Returns required ore amount for given key in given recipe dict"""

    ingredients = (recipes[key])[1]

    total: int = 0
    for ingredientKey in ingredients.keys():
        ingredientAmount: int = ingredients[ingredientKey]
        if ingredientKey == 'ORE':
            total += ingredientAmount
        else:
            available: int = inventory[ingredientKey]
            toBuild: int = ingredientAmount - available
            numberOfReactions: int = ceil(toBuild / recipes[ingredientKey][0])
            
            resultAmount: int = numberOfReactions * recipes[ingredientKey][0]
            logger[ingredientKey] += resultAmount
            
            inventory[ingredientKey] = (resultAmount + available) - ingredientAmount
            
            if numberOfReactions == 0:
                total += 0
            else:
                for i in range(numberOfReactions):
                    total += find_required_ore_amount_for(ingredientKey, recipes, inventory, logger)
    return total


if __name__ == '__main__':
    with open("C:\\Projects\\aoc2019\\day 14\\inputs.txt", 'r') as inputs:
        recipes: Dict[str, Tuple[int, Dict[str, int]]
                      ] = parse(inputs.readlines())
        inventory = init_inventory(recipes)
        logger = init_inventory(recipes)
        

        print(find_required_ore_amount_for("FUEL", recipes, inventory, logger))
