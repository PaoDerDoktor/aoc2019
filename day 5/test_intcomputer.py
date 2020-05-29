from intcomputer import Intcomputer

assert type(Intcomputer("[99]")) == Intcomputer

def test_loading() -> None:
    ic = Intcomputer([1101, 1, 1, 3, 4, 3, 99])
    assert ic.ram == [1101, 1, 1, 3, 4, 3, 99]

def test_positional_add() -> None:
    ic = Intcomputer([1, 0, 0, 3, 99])
    ic.run()
    assert ic.ram[3] == 2

def test_immediate_add() -> None:
    ic = Intcomputer([1101, 1, 1, 3, 99])
    ic.run()
    assert ic.ram[3] == 2

def test_positional_mul() -> None:
    ic = Intcomputer([2, 0, 0, 3, 99])
    ic.run()
    assert ic.ram[3] == 4

def test_immediate_mul() -> None:
    ic = Intcomputer([1102, 2, 2, 3, 99])
    ic.run()
    assert ic.ram[3] == 4

def test_in() -> None:
    ic = Intcomputer([3, 1, 99])
    ic.input(1)
    ic.run()
    assert ic.ram[1] == 1

def test_out() -> None:
    ic = Intcomputer([4, 1, 99])
    ic.run()
    assert ic.output() == 1

def test_fifo() -> None:
    ic = Intcomputer([3, 9, 3, 10, 4, 9, 4, 10, 99, 0, 0])
    ic.input(1)
    ic.input(2)
    ic.run()
    assert ic.output() == 1
    assert ic.output() == 2

def test_jit() -> None:
    ic = Intcomputer([1105, 1, 6, 104, 0, 99, 1105, 0, 12, 104, 1, 99, 104, 0, 99])
    ic.run()
    assert ic.output() == 1

def test_jif() -> None:
    ic = Intcomputer([1106, 0, 6, 104, 0, 99, 1106, 1, 12, 104, 1, 99, 104, 0, 99])
    ic.run()
    assert ic.output() == 1

def test_lt() -> None:
    ic = Intcomputer([1107, 2, 3, 9, 1107, 3, 2, 11, 104, 0, 104, 0, 99])
    ic.run()
    assert ic.output() == 1
    assert ic.output() == 0

def test_eq() -> None:
    ic = Intcomputer([1108, 3, 3, 9, 1108, 3, 4, 11, 104, 0, 104, 0, 99])
    ic.run()
    assert ic.output() == 1
    assert ic.output() == 0

def test_halt() -> None:
    ic = Intcomputer([99])
    ic.run()
    assert ic.halt == True and ic.ptr == 0