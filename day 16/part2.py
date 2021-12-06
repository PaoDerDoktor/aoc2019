def get_offset(sequence: list[int]) -> int:
    """Returns the offset of the message

    Args:
        sequence (list[int]): The original signal

    Returns:
        int: The offset
    """
        
    resultStr: str = ""
    for num in sequence[:7]:
        resultStr += str(num)
    return int(resultStr)
       
def main():
    with open("day 16/inputs.txt", "r") as inFile:
        sequence: list[int] = [int(i) for i in inFile.readline()]
        
        offset = get_offset(sequence) # will help to skip useless computing
        
        sequence = [sequence[_ % len(sequence)] for _ in range(offset, len(sequence)*10000)]
        
        for _ in range(100):
            backwardSums: list[int] = [0] # Because "the matrix" is upper triangular it's only influenced by it's rightmosts values
            subtotal: int = 0             # Used to keep track of previous sum's result
            for num  in sequence:
                subtotal += num
                backwardSums.append(subtotal)
            
            for i in range(len(sequence)):
                sequence[i] = abs(backwardSums[-1]-backwardSums[i])%10
            
        print("".join(map(str, sequence[:8])))
        
if __name__ == "__main__":
    main()