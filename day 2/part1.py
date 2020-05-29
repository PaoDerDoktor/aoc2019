with open("inputs.txt", "r+") as inputs:
    raw_intcode = ''.join(inputs.readlines())

    intcode = [int(elt) for elt in raw_intcode.split(',')]
    
    ptr = 0

    #PREWORK

    intcode[1] = 12
    intcode[2] = 2

    while (intcode[ptr] != 99):
        if intcode[ptr] == 1:
            intcode[intcode[ptr+3]] = intcode[intcode[ptr+1]] + intcode[intcode[ptr+2]]
        elif intcode[ptr] == 2:
            intcode[intcode[ptr+3]] = intcode[intcode[ptr+1]] * intcode[intcode[ptr+2]]
        else:
            raise ValueError('Error ! Bad opcode detected at index '+ptr+' : '+intcode[ptr])
            break
        ptr += 4
    
    res = ''
    for i in range(len(intcode)-1):
        res += str(intcode[i])+','
    res += str(intcode[-1])

    print(res)
    print()
    print(intcode[0])

#VALID