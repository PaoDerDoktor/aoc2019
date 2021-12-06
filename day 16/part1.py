from math import floor

def pattern(n: int, i: int) -> int:
    return [0,1,0,-1][floor((i+1)/(n+1))%4]

def main():
    with open("day 16/inputs.txt", "r") as inFile:
        sequence: list[int] = [int(i) for i in inFile.readline()]
        
        for _ in range(100):
            nextSequence:list[int] = []
            for index, value in enumerate(sequence):
                if index >= round(len(sequence)/2):
                    nextSequence.append(abs(sum(sequence[index:]))%10)
                else:
                    subsequence: int = 0
                    for numIndex, num in enumerate(sequence[index:], start=index):
                        subsequence += num*pattern(index, numIndex)
                    nextSequence.append(abs(subsequence)%10)
            sequence = nextSequence
            
        print("".join(map(str, sequence[:8])))
        
if __name__ == "__main__":
    main()