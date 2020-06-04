from typing import List, Dict, IO
from logging import *
from sys import stdout, stdin
from multiprocessing import Pipe, Process
from multiprocessing.connection import Connection


class Intcomputer(object):
    """Intcode computer class"""

    # Opcodes

    OP_ADD = 1
    OP_MUL = 2
    OP_IN = 3
    OP_OUT = 4
    OP_JIT = 5  # Jump if != 0 (jump-if-true)
    OP_JIF = 6  # Jump if == 0 (jump-if-false)
    OP_LT = 7  # less-than
    OP_EQ = 8  # equals
    OP_URB = 9  # update relative base
    OP_HALT = 99

    # Input methods

    IN_STDIN = 0
    IN_INTERNAL_LIST = 1
    IN_PIPE = 2

    # Output methods

    OUT_STDOUT = 0
    OUT_INTERNAL_LIST = 1
    OUT_PIPE = 2
    
    # States
    
    STATE_RUNNING = 0
    STATE_HALTED = 1
    STATE_ERROR = 2

    def __init__(self, intcode: Dict[int, int], name: str = "default_computer",
                 inputMethod: int = 0,  # IN_STDIN
                 outputMethod: int = 0  # OUT_STDOUT
                 ) -> None:
        """Initiate an intcode computer with an intcode"""

        self.name: str = name

        # Initializing RAM and pointers

        self.ram: Dict[int, int] = dict(intcode)
        self.ptr: int = 0
        self.relativeBasePtr: int = 0

        # Defining I/O methods

        self.inputMethod: int = inputMethod
        self.outputMethod: int = outputMethod

        # Defining storage for opcodes and args

        self.opcode: int = 99
        self.args: List[int] = [0, 0, 0]
        self.argModes: List[int] = [0, 0, 0]

        # Defining flags

        self.halt: bool = False

        # Preparing shallow I/O storage

        self.input: object
        self.output: object

        if inputMethod == self.IN_STDIN:
            self.input: IO = stdin
        elif inputMethod == self.IN_INTERNAL_LIST:
            self.input: List[int] = list()
        elif inputMethod == self.IN_PIPE:
            self.input: Conection = Pipe()[0]
        else:
            raise NotImplementedError(f"INVALID INPUT MODE : {inputMethod}")

        if outputMethod == self.OUT_STDOUT:
            self.output: IO = stdout
        elif outputMethod == self.OUT_INTERNAL_LIST:
            self.output: List[int] = list()
        elif outputMethod == self.OUT_PIPE:
            self.output: Connection = Pipe()[0]
        else:
            raise NotImplementedError(f"INVALID OUTPUT MODE : {outputMethod}")
        
        # Defining shallow state pipe
        
        self.statePipe: Connection = Pipe()[0]

    def set_in_pipe_connection(self, inConnection: Connection) -> None:
        """Sets input pipe connection if in IN_PIPE mode"""

        if self.inputMethod == self.IN_PIPE:
            self.input = inConnection
        else:
            raise ValueError(f"ERROR : INPUT IS NOT IN PIPE MODE")

    def set_out_pipe_connection(self, outConnection: Connection) -> None:
        """Sets output pipe connection if in IN_PIPE mode"""

        if self.outputMethod == self.OUT_PIPE:
            self.output = outConnection
        else:
            raise ValueError(f"ERROR : OUTPUT IS NOT IN PIPE MODE")
        
    def set_state_pipe_connection(self, stateConection: Connection) -> None:
        """Sets state pipe connection"""
        
        self.statePipe = stateConection

    def _in_from_stdin(self) -> int:
        return int(input("Input  <-- "))

    def _in_from_internal_list(self) -> int:
        return self.input.pop()

    def _in_from_pipe(self) -> int:
        return int(self.input.recv())

    def _out_from_stdout(self, val: int) -> None:
        print("Output -->", val)

    def _out_from_internal_list(self, val: int) -> None:
        self.output.insert(0, val)

    def _out_from_pipe(self, val: int) -> None:
        self.output.send(int(val))

    def _get_instruction_length(self) -> int:
        """Returns total length (opcode included) of current instruction"""

        if (self.opcode == self.OP_ADD):
            return 4
        elif (self.opcode == self.OP_MUL):
            return 4
        elif (self.opcode == self.OP_IN):
            return 2
        elif (self.opcode == self.OP_OUT):
            return 2
        elif (self.opcode == self.OP_JIT):
            return 3
        elif (self.opcode == self.OP_JIF):
            return 3
        elif (self.opcode == self.OP_LT):
            return 4
        elif (self.opcode == self.OP_EQ):
            return 4
        elif (self.opcode == self.OP_URB):
            return 2
        elif (self.opcode == self.OP_HALT):
            return 1
        else:
            raise NotImplementedError(
                f"INVALID OPCODE : {self.opcode} @ {self.ptr}")

    def _fetch(self):
        """Parses instruction"""

        operator = self._load(self.ptr)  # Get operator at current pointer

        # Opcode
        self.opcode = operator % 100  # Get operator's tens and ones digits as opcode

        # Arguments and Argument modes
        operator //= 10

        for i in range(self._get_instruction_length()-1):
            operator //= 10
            self.argModes[i] = operator % 10
            self.args[i] = self._load(self.ptr+i+1)

    def _load(self, addr: int) -> int:
        """Returns value at given address"""

        if addr < 0:
            raise IndexError(
                f"RAM ACCESS ERROR : INDEX CAN'T BE NEGATIVE ({addr})")
        elif addr in self.ram:
            return self.ram[addr]
        else:
            self.ram[addr] = 0
            return 0

    def _write(self, value: int, addr: int) -> None:
        """Writes specified value at specified address in RAM"""
        if addr < 0:
            raise IndexError(
                f"RAM ACCESS ERROR : INDEX CAN'T BE NEGATIVE ({addr}) @ {self.ptr} == {self.ram[self.ptr]}")
        else:
            self.ram[addr] = value

    def _resolve_arg(self, argNumber: int) -> int:
        """Fetch given argument's value"""

        mode: int = self.argModes[argNumber]
        value: int = self.args[argNumber]

        if mode == 1:  # ----------------- Immediate mode
            return value
        elif mode == 0:  # --------------- Positional mode
            return self._load(value)
        elif mode == 2:  # --------------- Relative mode
            return self._load(value + self.relativeBasePtr)
        else:  # ------------------------ Error
            raise NotImplementedError(
                f"INVALID PARAMETER MODE : {mode} @ {self.ptr}")

    def _resolve_write_addr_arg(self, argNumber: int) -> int:
        """Fetch given argument's value as an adress where to write data"""

        mode: int = self.argModes[argNumber]
        value: int = self.args[argNumber]

        if mode == 1:  # ----------------- Immediate mode
            raise ValueError(
                f"INVALID PARAMETER MODE : {mode} @ {self.ptr} (CAN'T WRITE TO IMMEDIATE MODE)")
        elif mode == 0:  # --------------- Positional mode
            return value
        elif mode == 2:  # --------------- Relative mode
            return value + self.relativeBasePtr
        else:  # ------------------------ Error
            raise NotImplementedError(
                f"INVALID PARAMETER MODE : {mode} @ {self.ptr}")

    def _add(self) -> None:
        """Executes addition operation"""

        self._write(self._resolve_arg(0) + self._resolve_arg(1),
                    self._resolve_write_addr_arg(2))
        self.ptr += 4

    def _mul(self) -> None:
        """Executes multiplication operation"""

        self._write(self._resolve_arg(0) * self._resolve_arg(1),
                    self._resolve_write_addr_arg(2))
        self.ptr += 4

    def _out(self) -> None:
        """Executes output operation"""

        val: int = self._resolve_arg(0)
        if self.outputMethod == self.OUT_STDOUT:
            self._out_from_stdout(val)
        elif self.outputMethod == self.OUT_INTERNAL_LIST:
            self._out_from_internal_list(val)
        elif self.outputMethod == self.OUT_PIPE:
            self._out_from_pipe(val)
        else:
            raise NotImplementedError(
                f"INVALID OUTPUT MODE : {self.outputMethod}")
        self.ptr += 2

    def _in(self) -> None:
        """Executes input operation"""

        if self.inputMethod == self.IN_STDIN:
            self._write(self._in_from_stdin(), self._resolve_write_addr_arg(0))
        elif self.inputMethod == self.IN_INTERNAL_LIST:
            if self.argModes[0] == 2:
                self._write(self._in_from_internal_list(),
                            self._resolve_write_addr_arg(0))
            else:
                self._write(self._in_from_internal_list(),
                            self._resolve_write_addr_arg(0))
        elif self.inputMethod == self.IN_PIPE:
            self._write(self._in_from_pipe(), self._resolve_write_addr_arg(0))
        else:
            raise NotImplementedError(
                f"INVALID INPUT MODE : {self.inputMethod}")
        self.ptr += 2

    def _jit(self) -> None:
        """Executes jump-if-true operation"""

        if (self._resolve_arg(0) != 0):
            self.ptr = self._resolve_arg(1)
        else:
            self.ptr += 3

    def _jif(self) -> None:
        """Executes jump-if-false operation"""

        if (self._resolve_arg(0) == 0):
            self.ptr = self._resolve_arg(1)
        else:
            self.ptr += 3

    def _lt(self) -> None:
        """Executes less-than operation"""

        self._write(int(self._resolve_arg(0) <
                        self._resolve_arg(1)), self._resolve_write_addr_arg(2))
        self.ptr += 4

    def _eq(self) -> None:
        self._write(int(self._resolve_arg(0) ==
                        self._resolve_arg(1)), self._resolve_write_addr_arg(2))
        self.ptr += 4

    def _urb(self) -> None:
        self.relativeBasePtr += self._resolve_arg(0)
        self.ptr += 2

    def _halt(self) -> None:
        """Raises halt flag"""

        self.halt = True

    def list_output(self) -> int:
        """Returns first output of list if in INTERNAL LIST mode"""

        if self.outputMethod == self.OUT_INTERNAL_LIST:
            if len(self.output) == 0:
                raise StopIteration("Output stack is empty")
            else:
                return self.output.pop()
        else:
            raise ValueError(f"ERROR : INPUT IS NOT IN INTERNAL_LIST MODE")

    def list_input(self, val: int) -> None:
        """Adds an input in list if in INTERNAL LIST mode"""

        if self.inputMethod == self.IN_INTERNAL_LIST:
            self.input.insert(0, val)
        else:
            raise ValueError(f"ERROR : OUTPUT IS NOT IN INTERNAL_LIST MODE")

    def run(self) -> None:
        """Runs the intcode"""
        while not self.halt:
            self._fetch()
            
            if (self.opcode == self.OP_ADD):
                print("add")
                self.statePipe.send(Intcomputer.STATE_RUNNING)
                self._add()
            elif (self.opcode == self.OP_MUL):
                print("mul")
                self.statePipe.send(Intcomputer.STATE_RUNNING)
                self._mul()
            elif (self.opcode == self.OP_IN):
                print("in")
                self.statePipe.send(Intcomputer.STATE_RUNNING)
                self._in()
            elif (self.opcode == self.OP_OUT):
                print("out")
                self.statePipe.send(Intcomputer.STATE_RUNNING)
                self._out()
            elif (self.opcode == self.OP_JIT):
                print("jit")
                self.statePipe.send(Intcomputer.STATE_RUNNING)
                self._jit()
            elif (self.opcode == self.OP_JIF):
                print("jif")
                self.statePipe.send(Intcomputer.STATE_RUNNING)
                self._jif()
            elif (self.opcode == self.OP_LT):
                print("lt")
                self.statePipe.send(Intcomputer.STATE_RUNNING)
                self._lt()
            elif (self.opcode == self.OP_EQ):
                print("eq")
                self.statePipe.send(Intcomputer.STATE_RUNNING)
                self._eq()
            elif (self.opcode == self.OP_URB):
                print("urb")
                self.statePipe.send(Intcomputer.STATE_RUNNING)
                self._urb()
            elif (self.opcode == self.OP_HALT):
                print("halt")
                self.statePipe.send(Intcomputer.STATE_HALTED)
                self._halt()
            else:
                self.statePipe.send(Intcomputer.STATE_ERROR)
                raise NotImplementedError(
                    f"INVALID OPCODE : {self.opcode} @ {self.ptr}")
                
        self.input.close()
        self.output.close()
        self.statePipe.close()

    # FUNCTIONS


def _run_piped_intcomputer(intcode: List[int], inPipe: Connection, outPipe: Connection, statePipe: Connection) -> None:
    """Runs a computer specifically created"""

    ic: Intcomputer = Intcomputer(
        intcode, "piped computer", Intcomputer.IN_PIPE, Intcomputer.OUT_PIPE)
    ic.set_state_pipe_connection(statePipe)
    ic.set_in_pipe_connection(inPipe)
    ic.set_out_pipe_connection(outPipe)
    ic.run()


def piped_intcomputer_as_a_process(intcode: List[int], inPipe: Connection, outPipe: Connection, statePipe: Connection) -> Process:
    """Returns a process ready to run specified intcode, I/O made by passed pipes"""

    return Process(target=_run_piped_intcomputer, args=(intcode, inPipe, outPipe, statePipe))


def list_to_dict(l: List[int]) -> Dict[int, int]:
    """Takes an intcode as a list, and returns it as a dict ready to init an intcomputer's ram."""

    return {i: l[i] for i in range(len(l))}