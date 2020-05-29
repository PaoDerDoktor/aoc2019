with open("inputs.txt", "r+") as inputs:
    min_range, max_range = [int(i) for i in inputs.readlines()[0].split("-")]

    candidates = []
    for i in range(min_range, max_range+1):
        i_s = str(i)
        is_candidate = False
        for j in range(1, len(i_s)):
            if (int(i_s[j-1]) > int(i_s[j])):
                is_candidate = False
                break
            
            if (int(i_s[j-1]) == int(i_s[j])):
                is_candidate = True
        
        if (is_candidate) :
            candidates.append(i)

    print(len(candidates))

# VALID