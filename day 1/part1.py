with open("inputs.txt", "r+") as inputs:
    res = 0
    weights = inputs.readlines()
    for weight in weights:
        res += int(weight)//3 - 2
    print(res)

# VALID