with open("inputs.txt", "r+") as inputs:
    min_range, max_range = [int(i) for i in inputs.readlines()[0].split("-")]

    candidates = []
    for i in range(min_range, max_range+1):
        i_s = str(i)
        is_incremental = True

        c = 1
        foundPair = False
        for j in range(0, len(i_s)):

            if (j < len(i_s)-1 and i_s[j] > i_s[j+1]):
                is_incremental = False
                break

            if (j < len(i_s)-1 and i_s[j+1] == i_s[j]):
                c += 1
            elif (c == 2):
                c = 1
                foundPair = True
            else:
                c = 1
        
        if (is_incremental and foundPair) :
            candidates.append(i)

    print(len(candidates))