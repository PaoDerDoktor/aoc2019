from typing import List
from sys import maxsize

def check_for_corrupt(image:List[int], width:int, height:int) -> int:
    """Return the number of 2s multiplied by the number of 1s of the layer which has the less 0 digits"""
    
    layerSize: int = width*height
    layerNumber: int = int(len(image)/layerSize)
    
    layers:List[int] = []
    for i in range(0, len(image), layerSize):
        layers.append(image[i:i+layerSize])
    
    bestLayer:List[int] = layers[0]
    bestZeroesCount = maxsize
    for layer in layers:
        zeroes:int = layer.count(0)
        if zeroes < bestZeroesCount:
            bestZeroesCount = zeroes
            bestLayer = layer
    
    return bestLayer.count(1)*bestLayer.count(2)
        

with open("inputs.txt", "r") as inputs:
    image:List[int] = [int(i) for i in inputs.read()]
    
    print(check_for_corrupt(image, 25, 6))