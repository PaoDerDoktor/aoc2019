from intcom import *
from typing import List, Dict
from sys import stdin, stdout
from io import StringIO
from multiprocessing import Pipe
from multiprocessing.connection import Connection

    ################
    # CUSTOM TESTS #
    ################

def test_intcom() -> None:
    """Simple test to see if Intcom object constructs correctly"""
    
    ic: Intcom = Intcom(list_to_dict([99]), "Dio Brando",
                        inputMethod=IO_METHOD.LIST, outputMethod=IO_METHOD.LIST,
                        inputSrc=[], outputDest=[])
    
    assert ic.name == "Dio Brando"
    assert ic.inputMethod == IO_METHOD.LIST
    assert ic.outputMethod == IO_METHOD.LIST
    assert ic.inputSrc == []
    assert ic.outputDest == []
    assert ic.ram[0] == 99
    assert ic.halt == True


def test_run() -> None:
    """Simple run test"""
    
    ic: Intcom = Intcom(list_to_dict([99]), "Dio Brando",
                        inputMethod=IO_METHOD.LIST, outputMethod=IO_METHOD.LIST,
                        inputSrc=[], outputDest=[])
    
    ic.run()
    
    assert ic.halt == True


def test_add() -> None:
    """Simple add test"""
    
    ic: Intcom = Intcom(list_to_dict([1, 0, 0, 0, 99]), "Dio Braddo",
                        inputMethod=IO_METHOD.LIST, outputMethod=IO_METHOD.LIST,
                        inputSrc=[], outputDest=[])

    ic.run()
    
    assert ic.ram[0] == 2


def test_mul() -> None:
    """Simple mul test"""
    
    ic: Intcom = Intcom(list_to_dict([2, 0, 0, 0, 99]), "Dio Muldo",
                        inputMethod=IO_METHOD.LIST, outputMethod=IO_METHOD.LIST,
                        inputSrc=[], outputDest=[])
    
    ic.run()
    
    assert ic.ram[0] == 4


def test_in_TIOW(monkeypatch) -> None:
    """Simple stdin input test"""
    
    monkeypatch.setattr('sys.stdin.read', (lambda: '1\n'))
    
    ic: Intcom = Intcom(list_to_dict([3, 0, 99]), "Tiow Brando",
                        inputMethod=IO_METHOD.TIOW, outputMethod=IO_METHOD.LIST,
                        inputSrc=stdin, outputDest=[])
    
    ic.run()
    
    assert ic.ram[0] == 1


def test_in_LIST() -> None:
    """Simple list input test"""
    
    inList: List[int] = []
    
    ic: Intcom = Intcom(list_to_dict([3, 0, 99]), "Dio Brandist",
                        inputMethod=IO_METHOD.LIST, outputMethod=IO_METHOD.LIST,
                        inputSrc=inList, outputDest=[])
    
    inList.append(1)
    
    ic.run()
    
    assert ic.ram[0] == 1


def test_in_PIPE() -> None:
    """Simple pipe input test"""
    
    out, enter = Pipe(False)
    
    ic : Intcom = Intcom(list_to_dict([3, 0, 99]), "Pipo Brando",
                        inputMethod=IO_METHOD.PIPE, outputMethod=IO_METHOD.LIST,
                        inputSrc=out, outputDest=[])
    
    enter.send(1)
    
    ic.run()
    
    assert ic.ram[0] == 1


def test_out_TIOW() -> None:
    """Simple TextIOWrapper output test"""
    
    ic : Intcom = Intcom(list_to_dict([4, 0, 99]), "Tiow Brandout",
                        inputMethod=IO_METHOD.LIST, outputMethod=IO_METHOD.TIOW,
                        inputSrc=[], outputDest=stdout)
    
    ic.run()
    
    stdout.seek(0, 0)
    
    captured = stdout.read()
    assert captured == b'Output -> 4\n'


def test_out_LIST() -> None:
    """Simple List output test"""
    
    out: List[int] = []
    
    ic : Intcom = Intcom(list_to_dict([4, 0, 99]), "Diout Brandist",
                        inputMethod=IO_METHOD.LIST, outputMethod=IO_METHOD.LIST,
                        inputSrc=[], outputDest=out)
    
    ic.run()
    
    assert out.pop() == 4


def test_out_PIPE() -> None:
    """Simple Pipe output test"""
    
    out, enter = Pipe(False)
    
    ic : Intcom = Intcom(list_to_dict([4, 0, 99]), "Pipo Brandout",
                        inputMethod=IO_METHOD.LIST, outputMethod=IO_METHOD.PIPE,
                        inputSrc=[], outputDest=enter)
    
    ic.run()
    
    assert out.recv() == 4


def test_jit() -> None:
    """Simple jump-if-true test"""
    
    out: List[int] = []
    out2: List[int] = []
    
    ic : Intcom = Intcom(list_to_dict([5, 9, 11, 4, 10, 99, 4, 9, 99, 1, 0, 6]), "Jito Brando",
                        inputMethod=IO_METHOD.LIST, outputMethod=IO_METHOD.LIST,
                        inputSrc=[], outputDest=out)
    ic2 : Intcom = Intcom(list_to_dict([5, 10, 11, 4, 10, 99, 4, 9, 99, 1, 0, 6]), "Jitwo Brando",
                        inputMethod=IO_METHOD.LIST, outputMethod=IO_METHOD.LIST,
                        inputSrc=[], outputDest=out2)
    
    ic.run()
    ic2.run()
    
    assert out.pop() == 1
    assert out2.pop() == 0


def test_jif() -> None:
    """Simple jump-if-false test"""
    
    out: List[int] = []
    out2: List[int] = []
    
    ic : Intcom = Intcom(list_to_dict([6, 9, 11, 4, 9, 99, 4, 10, 99, 1, 0, 6]), "Jifo Brando",
                        inputMethod=IO_METHOD.LIST, outputMethod=IO_METHOD.LIST,
                        inputSrc=[], outputDest=out)
    ic2 : Intcom = Intcom(list_to_dict([6, 10, 11, 4, 9, 99, 4, 10, 99, 1, 0, 6]), "Jiftwo Brando",
                        inputMethod=IO_METHOD.LIST, outputMethod=IO_METHOD.LIST,
                        inputSrc=[], outputDest=out2)
    
    ic.run()
    ic2.run()
    
    assert out.pop() == 1
    assert out2.pop() == 0


def test_lt() -> None:
    """Simple less-than test"""
    
    out: List[int] = []
    out2: List[int] = []
    
    ic : Intcom = Intcom(list_to_dict([7, 7, 8, 9, 4, 9, 99, 0, 1, 0]), "Giorno Giovanna",
                        inputMethod=IO_METHOD.LIST, outputMethod=IO_METHOD.LIST,
                        inputSrc=[], outputDest=out)
    ic2 : Intcom = Intcom(list_to_dict([7, 7, 8, 9, 4, 9, 99, 1, 0, 0]), "Giorntwo Giovanna",
                        inputMethod=IO_METHOD.LIST, outputMethod=IO_METHOD.LIST,
                        inputSrc=[], outputDest=out2)
    
    ic.run()
    ic2.run()
    
    assert out.pop() == 1
    assert out2.pop() == 0


def test_eq() -> None:
    """Simple equals test"""
    
    out: List[int] = []
    out2: List[int] = []
    
    ic : Intcom = Intcom(list_to_dict([8, 7, 8, 9, 4, 9, 99, 1, 1, 0]), "Dio Dio",
                        inputMethod=IO_METHOD.LIST, outputMethod=IO_METHOD.LIST,
                        inputSrc=[], outputDest=out)
    ic2 : Intcom = Intcom(list_to_dict([8, 7, 8, 9, 4, 9, 99, 1, 0, 0]), "Brando Brando",
                        inputMethod=IO_METHOD.LIST, outputMethod=IO_METHOD.LIST,
                        inputSrc=[], outputDest=out2)
    
    ic.run()
    ic2.run()
    
    assert out.pop() == 1
    assert out2.pop() == 0


def test_urb() -> None:
    """Simple urb test"""
    
    ic : Intcom = Intcom(list_to_dict([9, 1, 99]), "-Dio v2's Egypt Palace", # Y'know, cause -Dio is relative Dio, Dio V2 is update Dio, and Egypt Palace is Dio's base... Haha
                        inputMethod=IO_METHOD.LIST, outputMethod=IO_METHOD.LIST,
                        inputSrc=[], outputDest=[])
    
    ic.run()
    
    assert ic.relBase == 1
    
def test_immediate_value() -> None:
    """Simple test for positional value arguments, using addition"""
    
    ic : Intcom = Intcom(list_to_dict([1101, 1, 3, 5, 99, 0]), "Dio's World",
                        inputMethod=IO_METHOD.LIST, outputMethod=IO_METHOD.LIST,
                        inputSrc=[], outputDest=[])
    
    ic.run()
    
    assert ic.ram[5] == 4
    
def test_hybrid_value() -> None:
    """Simple test for hybrid-modded value arguments, using addition"""
    
    ic: Intcom = Intcom(list_to_dict([101, 5, 0, 5, 99, 0]), "DIO",
                       inputMethod=IO_METHOD.LIST, outputMethod=IO_METHOD.LIST,
                       inputSrc=[], outputDest=[])
    
    ic.run()
    
    assert ic.ram[5] == 106
    
def test_rel_value() -> None:
    """Simple test for relative value arguments, using addition"""
    
    ic: Intcom = Intcom(list_to_dict([1201, 0, -1, 3, 109, 2, 1201, 1, 0, 11, 99, 0]), "-(Dio Brando)",
                       inputMethod=IO_METHOD.LIST, outputMethod=IO_METHOD.LIST,
                       inputSrc=[], outputDest=[])
    
    ic.run()
    
    print(ic.ram)
    assert ic.ram[11] == 1200
    
# No HALT test, as the first test already is testing HALT Opcode

    #############
    # AOC TESTS #
    #############

def test_aoc_day2_part1_test1() -> None:
    """Test 1 from Part 1 of Day 2 on AOC website"""
    
    inList: List[int] = []
    outList: List[int] = []
    
    ic: Intcom = Intcom(list_to_dict([1,0,0,0,99]), "Day 2 - Part 1 - Test 1",
                       inputMethod=IO_METHOD.LIST, outputMethod=IO_METHOD.LIST,
                       inputSrc=inList, outputDest=outList)
    
    ic.run()
    
    assert ic.ram == list_to_dict([2,0,0,0,99])
    
    
def test_aoc_day2_part1_test2() -> None:
    """Test 2 from Part 1 of Day 2 on AOC website"""
    
    inList: List[int] = []
    outList: List[int] = []
    
    ic: Intcom = Intcom(list_to_dict([2,3,0,3,99]), "Day 2 - Part 1 - Test 2",
                       inputMethod=IO_METHOD.LIST, outputMethod=IO_METHOD.LIST,
                       inputSrc=inList, outputDest=outList)
    
    ic.run()
    
    assert ic.ram == list_to_dict([2,3,0,6,99])
    
    
def test_aoc_day2_part1_test3() -> None:
    """Test 3 from Part 1 of Day 2 on AOC website"""
    
    inList: List[int] = []
    outList: List[int] = []
    
    ic: Intcom = Intcom(list_to_dict([2,4,4,5,99,0]), "Day 2 - Part 1 - Test 3",
                       inputMethod=IO_METHOD.LIST, outputMethod=IO_METHOD.LIST,
                       inputSrc=inList, outputDest=outList)
    
    ic.run()
    
    assert ic.ram == list_to_dict([2,4,4,5,99,9801])
    

def test_aoc_day2_part1_test4() -> None:
    """Test 4 from Part 1 of Day 2 on AOC website"""
    
    inList: List[int] = []
    outList: List[int] = []
    
    ic: Intcom = Intcom(list_to_dict([1,1,1,4,99,5,6,0,99]), "Day 2 - Part 1 - Test 4",
                       inputMethod=IO_METHOD.LIST, outputMethod=IO_METHOD.LIST,
                       inputSrc=inList, outputDest=outList)
    
    ic.run()
    
    assert ic.ram == list_to_dict([30,1,1,4,2,5,6,0,99])
    
    
def test_aoc_day5_part1_test1() -> None:
    """Test 1 from Part 1 of Day 5 on AOC website"""
    
    inList: List[int] = []
    outList: List[int] = []
    
    ic: Intcom = Intcom(list_to_dict([1101,100,-1,4,0]), "Day 5 - Part 1 - Test 1",
                       inputMethod=IO_METHOD.LIST, outputMethod=IO_METHOD.LIST,
                       inputSrc=inList, outputDest=outList)
    
    ic.run()
    
    assert ic.ram == list_to_dict([1101,100,-1,4,99])
    
    
def test_aoc_day5_part2_test1() -> None:
    """Test 1 from Part 2 of Day 5 on AOC website"""
    
    inList: List[int] = []
    outList: List[int] = []
    
    ic: Intcom = Intcom(list_to_dict([3,9,8,9,10,9,4,9,99,-1,8]), "Day 5 - Part 2 - Test 1.1",
                       inputMethod=IO_METHOD.LIST, outputMethod=IO_METHOD.LIST,
                       inputSrc=inList, outputDest=outList)
    
    inList.append(8)
    
    ic.run()
    
    assert outList.pop() == 1
    
    inList2: List[int] = []
    outList2: List[int] = []
    
    ic2: Intcom = Intcom(list_to_dict([3,9,8,9,10,9,4,9,99,-1,8]), "Day 5 - Part 2 - Test 1.2",
                       inputMethod=IO_METHOD.LIST, outputMethod=IO_METHOD.LIST,
                       inputSrc=inList2, outputDest=outList2)
    
    inList2.append(0)
    
    ic2.run()
    
    assert outList2.pop() == 0
    
    
def test_aoc_day5_part2_test2() -> None:
    """Test 2 from Part 2 of Day 5 on AOC website"""
    
    inList: List[int] = []
    outList: List[int] = []
    
    ic: Intcom = Intcom(list_to_dict([3,9,7,9,10,9,4,9,99,-1,8]), "Day 5 - Part 2 - Test 2.1",
                       inputMethod=IO_METHOD.LIST, outputMethod=IO_METHOD.LIST,
                       inputSrc=inList, outputDest=outList)
    
    inList.append(7)
    
    ic.run()
    
    assert outList.pop() == 1
    
    inList2: List[int] = []
    outList2: List[int] = []
    
    ic2: Intcom = Intcom(list_to_dict([3,9,7,9,10,9,4,9,99,-1,8]), "Day 5 - Part 2 - Test 2.2",
                       inputMethod=IO_METHOD.LIST, outputMethod=IO_METHOD.LIST,
                       inputSrc=inList2, outputDest=outList2)
    
    inList2.append(9)
    
    ic2.run()
    
    assert outList2.pop() == 0
    

def test_aoc_day5_part2_test3() -> None:
    """Test 3 from Part 2 of Day 5 on AOC website"""
    
    inList: List[int] = []
    outList: List[int] = []
    
    ic: Intcom = Intcom(list_to_dict([3,3,1108,-1,8,3,4,3,99]), "Day 5 - Part 2 - Test 3.1",
                       inputMethod=IO_METHOD.LIST, outputMethod=IO_METHOD.LIST,
                       inputSrc=inList, outputDest=outList)
    
    inList.append(8)
    
    ic.run()
    
    assert outList.pop() == 1
    
    inList2: List[int] = []
    outList2: List[int] = []
    
    ic2: Intcom = Intcom(list_to_dict([3,3,1108,-1,8,3,4,3,99]), "Day 5 - Part 2 - Test 3.2",
                       inputMethod=IO_METHOD.LIST, outputMethod=IO_METHOD.LIST,
                       inputSrc=inList2, outputDest=outList2)
    
    inList2.append(0)
    
    ic2.run()
    
    assert outList2.pop() == 0
    

def test_aoc_day5_part2_test4() -> None:
    """Test 4 from Part 2 of Day 5 on AOC website"""
    
    inList: List[int] = []
    outList: List[int] = []
    
    ic: Intcom = Intcom(list_to_dict([3,3,1107,-1,8,3,4,3,99]), "Day 5 - Part 2 - Test 4.1",
                       inputMethod=IO_METHOD.LIST, outputMethod=IO_METHOD.LIST,
                       inputSrc=inList, outputDest=outList)
    
    inList.append(7)
    
    ic.run()
    
    assert outList.pop() == 1
    
    inList2: List[int] = []
    outList2: List[int] = []
    
    ic2: Intcom = Intcom(list_to_dict([3,3,1107,-1,8,3,4,3,99]), "Day 5 - Part 2 - Test 4.2",
                       inputMethod=IO_METHOD.LIST, outputMethod=IO_METHOD.LIST,
                       inputSrc=inList2, outputDest=outList2)
    
    inList2.append(9)
    
    ic2.run()
    
    assert outList2.pop() == 0
    
    
def test_aoc_day5_part2_test5() -> None:
    """Test 5 from Part 2 of Day 5 on AOC website"""
    
    inList: List[int] = []
    outList: List[int] = []
    
    ic: Intcom = Intcom(list_to_dict([3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9]), "Day 5 - Part 2 - Test 5.1",
                       inputMethod=IO_METHOD.LIST, outputMethod=IO_METHOD.LIST,
                       inputSrc=inList, outputDest=outList)
    
    inList.append(1)
    
    ic.run()
    
    assert outList.pop() == 1
    
    inList2: List[int] = []
    outList2: List[int] = []
    
    ic2: Intcom = Intcom(list_to_dict([3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9]), "Day 5 - Part 2 - Test 5.2",
                       inputMethod=IO_METHOD.LIST, outputMethod=IO_METHOD.LIST,
                       inputSrc=inList2, outputDest=outList2)
    
    inList2.append(0)
    
    ic2.run()
    
    assert outList2.pop() == 0
    
    
def test_aoc_day5_part2_test6() -> None:
    """Test 6 from Part 2 of Day 5 on AOC website"""
    
    inList: List[int] = []
    outList: List[int] = []
    
    ic: Intcom = Intcom(list_to_dict([3,3,1105,-1,9,1101,0,0,12,4,12,99,1]), "Day 5 - Part 2 - Test 6.1",
                       inputMethod=IO_METHOD.LIST, outputMethod=IO_METHOD.LIST,
                       inputSrc=inList, outputDest=outList)
    
    inList.append(1)
    
    ic.run()
    
    assert outList.pop() == 1
    
    inList2: List[int] = []
    outList2: List[int] = []
    
    ic2: Intcom = Intcom(list_to_dict([3,3,1105,-1,9,1101,0,0,12,4,12,99,1]), "Day 5 - Part 2 - Test 6.2",
                       inputMethod=IO_METHOD.LIST, outputMethod=IO_METHOD.LIST,
                       inputSrc=inList2, outputDest=outList2)
    
    inList2.append(0)
    
    ic2.run()
    
    assert outList2.pop() == 0
    
    
def test_aoc_day5_part2_test7() -> None:
    """Test 7 from Part 2 of Day 5 on AOC website"""
    
    inList: List[int] = []
    outList: List[int] = []
    
    ic: Intcom = Intcom(list_to_dict([3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,
                                      1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,
                                      999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99]),
                       "Day 5 - Part 2 - Test 7.1",
                       inputMethod=IO_METHOD.LIST, outputMethod=IO_METHOD.LIST,
                       inputSrc=inList, outputDest=outList)
    
    inList.append(7)
    
    ic.run()
    
    assert outList.pop() == 999
    
    inList2: List[int] = []
    outList2: List[int] = []
    
    ic2: Intcom = Intcom(list_to_dict([3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,
                                      1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,
                                      999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99]),
                       "Day 5 - Part 2 - Test 7.2",
                       inputMethod=IO_METHOD.LIST, outputMethod=IO_METHOD.LIST,
                       inputSrc=inList2, outputDest=outList2)
    
    inList2.append(8)
    
    ic2.run()
    
    assert outList2.pop() == 1000
    
    inList3: List[int] = []
    outList3: List[int] = []
    
    ic3: Intcom = Intcom(list_to_dict([3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,
                                      1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,
                                      999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99]),
                       "Day 5 - Part 2 - Test 7.3",
                       inputMethod=IO_METHOD.LIST, outputMethod=IO_METHOD.LIST,
                       inputSrc=inList3, outputDest=outList3)
    
    inList3.append(9)
    
    ic3.run()
    
    assert outList3.pop() == 1001
    

def test_aoc_day9_part1_test1() -> None:
    """Test 1 from Part 1 of Day 9 on AOC website"""
    
    inList: List[int] = []
    outList: List[int] = []
    
    ic: Intcom = Intcom(list_to_dict([109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99]),
                       "Day 9 - Part 1 - Test 1",
                       inputMethod=IO_METHOD.LIST, outputMethod=IO_METHOD.LIST,
                       inputSrc=inList, outputDest=outList)
    
    ic.run()
    
    assert outList[::-1] == [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99]
    

def test_aoc_day9_part1_test2() -> None:
    """Test 2 from Part 1 of Day 9 on AOC website"""
    
    inList: List[int] = []
    outList: List[int] = []
    
    ic: Intcom = Intcom(list_to_dict([1102,34915192,34915192,7,4,7,99,0]),
                       "Day 9 - Part 1 - Test 2",
                       inputMethod=IO_METHOD.LIST, outputMethod=IO_METHOD.LIST,
                       inputSrc=inList, outputDest=outList)
    
    ic.run()
    
    assert len(str(outList.pop())) == 16
    

def test_aoc_day9_part1_test3() -> None:
    """Test 3 from Part 1 of Day 9 on AOC website"""
    
    inList: List[int] = []
    outList: List[int] = []
    
    ic: Intcom = Intcom(list_to_dict([104,1125899906842624,99]),
                       "Day 9 - Part 1 - Test 3",
                       inputMethod=IO_METHOD.LIST, outputMethod=IO_METHOD.LIST,
                       inputSrc=inList, outputDest=outList)
    
    ic.run()
    
    assert outList.pop() == 1125899906842624