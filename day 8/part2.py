from typing import List

def get_layers(image:List[int], width:int, height:int) -> List[List[int]]:
    """Returns raw image int list as a list of layers"""
    layerSize: int = width*height
    
    layers: List[int] = []
    for i in range(0, len(image), layerSize):
        layers.append(image[i:i+layerSize])
    
    return layers

def resolve_image(layers:List[List[int]]) -> List[int]:
    """Resolves a single-layered image from a multi-layered one"""
    
    correctLayer: List[int] = []
    for pixelIndex in range(len(layers[0])):
        for layerIndex in range(len(layers)):
            if layers[layerIndex][pixelIndex] == 2 and layerIndex == len(layers)-1:
                correctLayer.append(1)
            elif layers[layerIndex][pixelIndex] == 2:
                continue
            else:
                correctLayer.append(layers[layerIndex][pixelIndex])
                break
            
    return correctLayer

def to_ppm(rawImage:List[int], width:int, height:int, filename:str="out.ppm") -> None:
    with open(filename, "w") as imageFile:
        imageFile.write("P1\n"+str(width)+"\n"+str(height)+"\n")
        for pxColor in rawImage:
            imageFile.write(str(pxColor)+"\n")

with open("inputs.txt", "r") as inputs:
    image:List[int] = [int(i) for i in inputs.read()]
    
    layers:List[List[int]] = get_layers(image, 25, 6)
    resolvedImage:List[int] = resolve_image(layers)
    
    to_ppm(resolvedImage, 25, 6)    