from typing import List, Dict
from logging import *

class Intcomputer(object):
    """Intcode computer class"""

    OP_ADD = 1
    OP_MUL = 2
    OP_IN  = 3
    OP_OUT = 4
    OP_JIT = 5 # Jump if != 0 (jump-if-true)
    OP_JIF = 6 # Jump if == 0 (jump-if-false)
    OP_LT = 7 # less-than
    OP_EQ = 8 # equals
    OP_HALT = 99

    def __init__(self, intcode:List[int], name:str = "default_computer") -> None:
        """Initiate an intcode computer with an intcode"""

        self.ram: List[int] = intcode[::]
        self.ptr: int = 0

            # Defining storage for opcodes and args

        self.opcode: int = 99
        self.args: List[int] = [0, 0, 0]
        self.argModes: List[int] = [0, 0, 0]

            # Defining storage for I/O

        self.stdout: List[int] = []
        self.stdin: List[int] = []

            # Defining flags

        self.halt = False


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
        elif (self.opcode == self.OP_HALT):
            return 1
        else:
            raise NotImplementedError(f"INVALID OPCODE : {self.opcode} @ {self.ptr}")


    def _fetch(self):
        """Parses instruction"""

        operator = self._load(self.ptr) # Get operator at current pointer

            # Opcode
        self.opcode = operator % 100 # Get operator's tens and ones digits as opcode

            # Arguments and Argument modes
        operator //= 10

        for i in range(self._get_instruction_length()-1):
            operator //= 10
            self.argModes[i] = operator % 10
            self.args[i] = self._load(self.ptr+i+1)


    def _load(self, addr:int) -> int:
        """Returns value at given address"""

        return self.ram[addr]


    def _load_indirect(self, addr:int) -> int:
        """Returns value at address specified by the pointer at given address"""

        return self.ram[self.ram[addr]]

    
    def _write(self, value:int, addr:int) -> None:
        """Writes specified value at specified address in RAM"""

        self.ram[addr] = value
    
    
    def _resolve_arg(self, argNumber:int) -> int:
        """Fetch given argument's value"""

        mode = self.argModes[argNumber]
        value = self.args[argNumber]

        if mode == 1: # --------------- Immediate mode
            return value
        elif mode == 0: # ------------- Positional mode
            return self._load(value)
        else: # ----------------------- Error
            raise NotImplementedError(f"INVALID PARAMETER MODE : {mode} @ {self.ptr}")


    def _add(self) -> None:
        """Executes addition operation"""

        self._write(self._resolve_arg(0) + self._resolve_arg(1), self.args[2])
        self.ptr += 4


    def _mul(self) -> None:
        """Executes multiplication operation"""

        self._write(self._resolve_arg(0) * self._resolve_arg(1), self.args[2])
        self.ptr += 4


    def _in(self) -> None:
        """Executes input"""

        if len(self.stdin) == 0 :
            self._write(int(input("Input  <-- ")), self.args[0])
        else:
            self._write(self.stdin.pop(), self.args[0])
        self.ptr += 2

    
    def _out(self) -> None:
        """Executes output"""

        self.stdout.insert(0, self._resolve_arg(0))
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

        self._write(int(self._resolve_arg(0) < self._resolve_arg(1)), self.args[2])
        self.ptr += 4

    
    def _eq(self) -> None:
        self._write(int(self._resolve_arg(0) == self._resolve_arg(1)), self.args[2])
        self.ptr += 4


    def _halt(self) -> None:
        """Raises halt flag"""

        self.halt = True


    def output(self) -> int:
        """Returns first output"""

        if len(self.stdout) == 0:
            raise StopIteration("Output stack is empty")
        else:
            return self.stdout.pop()

    
    def input(self, val:int) -> None:
        """Adds an input"""

        self.stdin.insert(0, val)


    def run(self) -> None:
        """Runs the intcode"""

        while not self.halt:
            self._fetch()
            
            if (self.opcode == self.OP_ADD):
                self._add()
            elif (self.opcode == self.OP_MUL):    
                self._mul()
            elif (self.opcode == self.OP_IN):
                self._in()
            elif (self.opcode == self.OP_OUT):
                self._out()
            elif (self.opcode == self.OP_JIT):
                self._jit()
            elif (self.opcode == self.OP_JIF):
                self._jif()
            elif (self.opcode == self.OP_LT):
                self._lt()
            elif (self.opcode == self.OP_EQ):
                self._eq()
            elif (self.opcode == self.OP_HALT):
                self._halt()
            else:
                raise NotImplementedError(f"INVALID OPCODE : {self.opcode} @ {self.ptr}")