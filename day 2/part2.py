with open("inputs.txt", "r+") as inputs:
    raw_intcode = ''.join(inputs.readlines())

    intcode = [int(elt) for elt in raw_intcode.split(',')]
    intcode_copy = []

    ptr = 0

    for i in range(0, 100):
        found = False
        for j in range(0, 100):
            intcode_copy = intcode.copy()
            intcode_copy[1] = i
            intcode_copy[2] = j

            while (intcode_copy[ptr] != 99):
                if intcode_copy[ptr] == 1:
                    intcode_copy[intcode_copy[ptr+3]] = intcode_copy[intcode_copy[ptr+1]] + intcode_copy[intcode_copy[ptr+2]]
                elif intcode_copy[ptr] == 2:
                    intcode_copy[intcode_copy[ptr+3]] = intcode_copy[intcode_copy[ptr+1]] * intcode_copy[intcode_copy[ptr+2]]
                else:
                    raise ValueError('Error ! Bad opcode detected at index '+ptr+' : '+intcode_copy[ptr])
                    break
                ptr += 4
            
            ptr = 0
            if intcode_copy[0] == 19690720:
                found = True
                break
        if found:
            break

    res = ''
    for i in range(len(intcode_copy)-1):
        res += str(intcode_copy[i])+','
    res += str(intcode_copy[-1])

    print(res)
    print()
    print(intcode_copy[1], intcode_copy[2])

#VALID