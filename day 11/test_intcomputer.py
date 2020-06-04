from intcomputer import Intcomputer, piped_intcomputer_as_a_process, list_to_dict
from multiprocessing import Pipe, Process
from time import sleep
import pytest

assert type(Intcomputer(list_to_dict([99]))) == Intcomputer


def test_loading() -> None:
    ic = Intcomputer(list_to_dict([1101, 1, 1, 3, 4, 3, 99]))
    assert ic.ram == list_to_dict([1101, 1, 1, 3, 4, 3, 99])


def test_positional_add() -> None:
    ic = Intcomputer(list_to_dict([1, 0, 0, 3, 99]))
    ic.run()
    assert ic.ram[3] == 2


def test_immediate_add() -> None:
    ic = Intcomputer(list_to_dict([1101, 1, 1, 3, 99]))
    ic.run()
    assert ic.ram[3] == 2


def test_positional_mul() -> None:
    ic = Intcomputer(list_to_dict([2, 0, 0, 3, 99]))
    ic.run()
    assert ic.ram[3] == 4


def test_immediate_mul() -> None:
    ic = Intcomputer(list_to_dict([1102, 2, 2, 3, 99]))
    ic.run()
    assert ic.ram[3] == 4


def test_console_in(monkeypatch) -> None:
    monkeypatch.setattr('builtins.input', lambda x: '1')
    ic = Intcomputer(list_to_dict([3, 1, 99]))
    ic.run()
    assert ic.ram[1] == 1


def test_internal_list_in() -> None:
    ic = Intcomputer(list_to_dict([3, 1, 99]), 'test', Intcomputer.IN_INTERNAL_LIST)
    ic.list_input(1)
    ic.run()
    assert ic.ram[1] == 1


def test_pipe_in() -> None:
    ic = Intcomputer(list_to_dict([3, 1, 99]), 'test', Intcomputer.IN_PIPE)
    i, o = Pipe()
    ic.set_in_pipe_connection(i)
    o.send(1)
    ic.run()
    assert ic.ram[1] == 1


def test_console_out(capsys) -> None:
    ic = Intcomputer(list_to_dict([4, 1, 99]))
    ic.run()
    assert capsys.readouterr().out == "Output --> 1\n"


def test_internal_list_out() -> None:
    ic = Intcomputer(list_to_dict([4, 1, 99]), outputMethod=Intcomputer.OUT_INTERNAL_LIST)
    ic.run()
    assert ic.list_output() == 1


def tets_pipe_out() -> None:
    ic = Intcomputer(list_to_dict([4, 1, 99]), outputMethod=Intcomputer.OUT_PIPE)
    i, o = Pipe()
    ic.set_out_pipe_connection(o)
    assert i.recv() == 1


def test_fifo_internal_list() -> None:
    ic = Intcomputer(list_to_dict([3, 9, 3, 10, 4, 9, 4, 10, 99, 0, 0]), 'test',
                     Intcomputer.IN_INTERNAL_LIST, Intcomputer.OUT_INTERNAL_LIST)
    ic.list_input(1)
    ic.list_input(2)
    ic.run()
    assert ic.list_output() == 1
    assert ic.list_output() == 2


def test_jit() -> None:
    ic = Intcomputer(list_to_dict([105, 1, 6, 104, 0, 99, 105, 0, 12, 104, 1, 99, 4, 0, 99]),
                     'test', Intcomputer.IN_INTERNAL_LIST, Intcomputer.OUT_INTERNAL_LIST)
    ic.run()
    assert ic.list_output() == 1


def test_jif() -> None:
    ic = Intcomputer(list_to_dict([6, 0, 6, 4, 0, 99, 106, 1, 12, 4, 1, 99, 4, 0, 99]),
                     'test', Intcomputer.IN_INTERNAL_LIST, Intcomputer.OUT_INTERNAL_LIST)
    ic.run()
    assert ic.list_output() == 1


def test_lt() -> None:
    ic = Intcomputer(list_to_dict([1107, 2, 3, 9, 1107, 3, 2, 11, 104, 0, 104, 0, 99]),
                     'test', Intcomputer.IN_INTERNAL_LIST, Intcomputer.OUT_INTERNAL_LIST)
    ic.run()
    assert ic.list_output() == 1
    assert ic.list_output() == 0


def test_eq() -> None:
    ic = Intcomputer(list_to_dict([1108, 3, 3, 9, 1108, 3, 4, 11, 104, 0, 104, 0, 99]),
                     'test', Intcomputer.IN_INTERNAL_LIST, Intcomputer.OUT_INTERNAL_LIST)
    ic.run()
    assert ic.list_output() == 1
    assert ic.list_output() == 0
    
def test_relative_simple_mul() -> None:
    ic = Intcomputer(list_to_dict([109, 4, 2202, -1, -2, 7, 104, 0, 99]), outputMethod=Intcomputer.OUT_INTERNAL_LIST)
    ic.run()
    assert ic.list_output() == -2202
    
def test_relative_simple_add() -> None:
    ic = Intcomputer(list_to_dict([109, 4, 2201, -1, -2, 7, 104, 0, 99]), outputMethod=Intcomputer.OUT_INTERNAL_LIST)
    ic.run()
    assert ic.list_output() == 2200

def test_halt() -> None:
    ic = Intcomputer(list_to_dict([99]))
    ic.run()
    assert ic.halt == True and ic.ptr == 0
    
def test_process() -> None:
    intcode = list_to_dict([104, 1, 99])
    
    icInEntrance, icInOut = Pipe()
    icOutEntrance, icOutOut = Pipe()  
    
    process:Process = piped_intcomputer_as_a_process(intcode, icInOut, icOutEntrance)
    process.start()
    process.join()
    
    assert icOutOut.recv() == 1

def test_process_pipe_io() -> None:
    intcode = list_to_dict([3, 5, 4, 5, 99, 0])
    
    icInEntrance, icInOut = Pipe()
    icLinkEntrance, icLinkOut = Pipe()
    icOutEntrance, icOutOut = Pipe()
    
    pIN = piped_intcomputer_as_a_process(intcode, icInOut, icLinkEntrance)
    pOUT = piped_intcomputer_as_a_process(intcode, icLinkOut, icOutEntrance)
    
    icInEntrance.send(1)
    
    pIN.start()
    pOUT.start()
    
    pIN.join()
    pOUT.join()
    
    assert icOutOut.recv() == 1
    
def test_extended_memory() -> None:
    intcode = list_to_dict([4, 888, 99])
    intcode2 = list_to_dict([1101, 1, 1, 888, 4, 888, 99])
    
    ic = Intcomputer(intcode, outputMethod=Intcomputer.OUT_INTERNAL_LIST)
    ic2 = Intcomputer(intcode2, outputMethod=Intcomputer.OUT_INTERNAL_LIST)
    ic.run()
    ic2.run()
    
    assert ic.list_output() == 0
    assert ic.ram[888] == 0
    
    assert ic2.list_output() == 2
    assert ic2.ram[888] == 2
