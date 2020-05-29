from sys import maxsize

with open("inputs.txt", "r+") as inputs:
    wires = ["R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51","U98,R91,D20,R16,D67,R40,U7,R15,U6,R7"]#inputs.readlines()
    wire_1 = [[elt[0], int(elt[1:])] for elt in wires[0].split(',')]
    wire_2 = [[elt[0], int(elt[1:])] for elt in wires[1].split(',')]

    pts_1 = [(0, 0)]
    pts_2 = [(0, 0)]

    directions = {"U": (0, 1), "D": (0, -1), "R": (1, 0), "L": (-1, 0)}

    for mov in wire_1:
        direction = directions[mov[0]]
        pts_1.append((pts_1[-1][0]+direction[0]*mov[1], pts_1[-1][1]+direction[1]*mov[1]))

    for mov in wire_2:
        direction = directions[mov[0]]
        pts_2.append((pts_2[-1][0]+direction[0]*mov[1], pts_2[-1][1]+direction[1]*mov[1]))

    minimalCross = maxsize

    for i in range(2, len(pts_1)):
        for j in range(2, len(pts_2)):
            if ((pts_1[i-1][1] == pts_1[i][1] and pts_2[j-1][1] != pts_2[j][1] and
                 ((pts_1[i-1][0] <= pts_2[j][0] and pts_2[j][0] <= pts_1[i][0]) or
                  (pts_1[i][0]   <= pts_2[j][0] and pts_2[j][0] <= pts_1[i-1][0])) and
                 ((pts_2[j-1][1] <= pts_1[i][1] and pts_1[i][1] <= pts_2[j][1]) or
                  (pts_2[j][1]   <= pts_1[i][1] and pts_1[i][1] <= pts_1[j-1][1])))):
                if (minimalCross > abs(pts_2[j][0])+abs(pts_1[i][1])):
                    minimalCross = abs(pts_2[j][0])+abs(pts_1[i][1])
            elif (pts_1[i-1][0] == pts_1[i][0] and pts_2[j-1][0] != pts_2[j][0] and
                  ((pts_2[j-1][0] <= pts_1[i][0] and pts_1[i][0] <= pts_2[j][0]) or
                   (pts_2[j][0]   <= pts_1[i][0] and pts_1[i][0] <= pts_1[j-1][0])) and
                  ((pts_1[i-1][1] <= pts_2[j][1] and pts_2[j][1] <= pts_1[i][1]) or
                   (pts_1[i][1]   <= pts_2[j][1] and pts_2[j][1] <= pts_1[i-1][1]))):
                if (minimalCross > abs(pts_1[i][0])+abs(pts_2[j][1])):
                    minimalCross = abs(pts_1[i][0])+abs(pts_2[j][1])

    print(minimalCross)

# VALID