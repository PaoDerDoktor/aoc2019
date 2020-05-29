from intcomputer import Intcomputer

with open("inputs.txt", "r+") as inputs:
    raw_intcode = ''.join(inputs.readlines())

    intcode = [int(elt) for elt in raw_intcode.split(',')]

    intcom = Intcomputer(intcode)
    intcom.run()


    while(True):
        try:
            print("Output -->",intcom.output())
        except StopIteration:
            print("Nothing to output")
            break