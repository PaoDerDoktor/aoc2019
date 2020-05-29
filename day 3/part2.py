from sys import maxsize

with open("inputs.txt", "r+") as inputs:
    wires = inputs.readlines()
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

    steps_1 = 0
    
    for i in range(0, len(pts_1) - 1):
        steps_2 = 0
        for j in range(0, len(pts_2) - 1):
            if (i != 0 and j != 0 and
                    pts_1[i][1] == pts_1[i+1][1] and pts_2[j][1] != pts_2[j+1][1] and # If wire_1 is (here) horizontal
                    min(pts_1[i][0], pts_1[i+1][0]) <= pts_2[j][0] <= max(pts_1[i][0], pts_1[i+1][0]) and
                    min(pts_2[j][1], pts_2[j+1][1]) <= pts_1[i][1] <= max(pts_2[j][1], pts_2[j+1][1])):
                if (minimalCross > steps_1 + steps_2 + abs(pts_2[j][0] - pts_1[i-1][0]) + abs(pts_1[i][1] - pts_2[j-1][1])):
                    minimalCross = steps_1 + steps_2 + abs(pts_2[j][0] - pts_1[i-1][0]) + abs(pts_1[i][1] - pts_2[j-1][1])
            elif (i != 0 and j != 0 and
                    pts_1[i][0] == pts_1[i+1][0] and pts_2[j][0] != pts_2[j+1][0] and
                    min(pts_2[j][0], pts_2[j+1][0]) <= pts_1[i][0] <= max(pts_2[j][0], pts_2[j+1][0]) and
                    min(pts_1[i][1], pts_1[i+1][1]) <= pts_2[j][1] <= max(pts_1[i][1], pts_1[i+1][1])):
                if (minimalCross > steps_1 + steps_2 + abs(pts_1[i][0] - pts_2[j-1][0]) + abs(pts_2[j][1] - pts_1[i-1][1])):
                    minimalCross = steps_1 + steps_2 + abs(pts_1[i][0] - pts_2[j-1][0]) + abs(pts_2[j][1] - pts_1[i-1][1])
            steps_2 += wire_2[j][1]
        steps_1 += wire_1[i][1]

    print(minimalCross)

# VALID