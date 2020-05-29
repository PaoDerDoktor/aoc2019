with open("inputs.txt", "r+") as inputs:
    res = 0
    weights = inputs.readlines()
    for weight in weights:
        subres = int(weight)//3 - 2
        while (subres > 0):
            res += subres
            subres = subres//3 - 2
    print(res)

# VALID