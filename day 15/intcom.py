from __future__ import annotations
from typing import Dict, List, Union
from multiprocessing import Process
from multiprocessing.connection import PipeConnection
from io import TextIOWrapper
from sys import stdin, stdout
from enum import IntEnum

    #####################
    # OPCODES CONSTANTS #
    #####################
        
class OPCODE(IntEnum):
        """Intcom's Opcodes enumeration"""
        ADD = 1  # Addition
        MUL = 2  # Multiplication
        IN  = 3  # Input
        OUT = 4  # Output
        JIT = 5  # Jump if True
        JIF = 6  # Jump if False
        LT  = 7  # Less Than
        EQ  = 8  # Equals
        URB = 9  # Update relative base
        HLT = 99 # Halt
        
    ############################
    # ARGUMENT TYPES CONSTANTS #
    ############################
    
class ARG_TYPE(IntEnum):
    """Intcom's argument types enum"""
    VALUE   = 0 # Argument is a value
    ADDRESS = 1 # Argument is a destination
    OPCODE  = 2 # Argument is the opcode
    
    ######################################
    # INSTRUCTIONS ARGS SHAPES CONSTANTS #
    ######################################
    
INSTR_ARG_SHAPE: Dict[OPCODE, List[ARG_TYPE]] = {
    OPCODE.ADD: [ARG_TYPE.OPCODE, ARG_TYPE.VALUE, ARG_TYPE.VALUE, ARG_TYPE.ADDRESS],
    OPCODE.MUL: [ARG_TYPE.OPCODE, ARG_TYPE.VALUE, ARG_TYPE.VALUE, ARG_TYPE.ADDRESS],
    OPCODE.IN:  [ARG_TYPE.OPCODE, ARG_TYPE.ADDRESS],
    OPCODE.OUT: [ARG_TYPE.OPCODE, ARG_TYPE.VALUE],
    OPCODE.JIT: [ARG_TYPE.OPCODE, ARG_TYPE.VALUE, ARG_TYPE.VALUE],
    OPCODE.JIF: [ARG_TYPE.OPCODE, ARG_TYPE.VALUE, ARG_TYPE.VALUE],
    OPCODE.LT:  [ARG_TYPE.OPCODE, ARG_TYPE.VALUE, ARG_TYPE.VALUE, ARG_TYPE.ADDRESS],
    OPCODE.EQ:  [ARG_TYPE.OPCODE, ARG_TYPE.VALUE, ARG_TYPE.VALUE, ARG_TYPE.ADDRESS],
    OPCODE.URB: [ARG_TYPE.OPCODE, ARG_TYPE.VALUE],
    OPCODE.HLT: [ARG_TYPE.OPCODE]
}

    ############################
    # ARGUMENT MODES CONSTANTS #
    ############################
    
class ARG_MODE(IntEnum):
    """Intcom's argument modes enumeration"""
    POS = 0 # Positional mode : arg is an address
    IMM = 1 # Immediate mode : arg is a value
    REL = 2 # Relative mode : arg is an address relative to current "relative base pointer" value

    ########################
    # IO METHODS CONSTANTS #
    ########################
        
class IO_METHOD(IntEnum):
    """Intcom's Input/Output methods enumeration"""
    TIOW = 0 # TextIOWrapper expected
    LIST = 1 # List expected
    PIPE = 2 # Multiprocessing Connection expected

    ################
    # INTCOM CLASS #
    ################

class Intcom(object):
    """Intcom class"""
    
        ###############
        # CONSTRUCTOR #
        ###############

    def __init__(self, prog:Dict[int, int], name: str="Default Intcom", *,
                 inputMethod: IO_METHOD=IO_METHOD.TIOW, outputMethod: IO_METHOD=IO_METHOD.TIOW,
                 inputSrc: Union[TextIOWrapper, Connection, List]=stdin,
                 outputDest: Union[TextIOWrapper, Connection, List]=stdout) -> None:
        """Initializes an Intcom

        Arguments:
            prog {Dict[int, int]} -- The AOC2019Intcode program to run

        Keyword Arguments:
            inputMethod {IO_METHOD} -- The Input method. See Intcom's class constants for more infos (default: {IO_METHOD.TIOW})
            outputMethod {IO_METHOD} -- The output method. See Intcom's class constants for more infos (default: {IO_METHOD.TIOW})
            name {str} -- The name of the computer (default: {"Default Intcom"})
            inputSrc {Union[TextIOWrapper, Connection, List]} -- The input source for the Intcom (default: {sys.stdin})
            outputDest {Union[TextIOWrapper, Connection, List]} -- The output destination for the Intcom (default: {sys.stdout})
        """
        
        self.ram: Dict[int, int] = dict(prog) # Intcom's RAM is initialized with a deepcopy of parameter-given program
        self.name: str = name
        self.inputMethod: IO_METHOD = inputMethod
        self.outputMethod: IO_METHOD = outputMethod
        
        if inputMethod == IO_METHOD.TIOW and not isinstance(inputSrc, type(stdin)) and not isinstance(inputSrc, TextIOWrapper):
            raise TypeError(f"CONSTRUCTION ERROR : Provided input method is 0 (TIOW) but input source type is not an instance of {type(stdin)}.")
        elif inputMethod == IO_METHOD.LIST and not isinstance(inputSrc, list):
            raise TypeError(f"CONSTRUCTION ERROR : Provided input method is 1 (LIST) but input source type is not an instance of list.")
        elif inputMethod == IO_METHOD.PIPE and not isinstance(inputSrc, PipeConnection):
            raise TypeError(f"CONSTRUCTION ERROR : Provided input method is 2 (PIPE) but input source type is not an instance of multiprocessing.Connection.")
        elif inputMethod != IO_METHOD.TIOW and inputMethod != IO_METHOD.LIST and inputMethod != IO_METHOD.PIPE:
            raise NotImplementedError(f"CONSTRUCTION ERROR : Provided input method is invalid : {inputMethod}")
        else:
            self.inputSrc: {Union[TextIOWrapper, Connection, List]} = inputSrc
            
        if outputMethod == IO_METHOD.TIOW and not isinstance(outputDest, type(stdout)) and not isinstance(outputDest, TextIOWrapper):
            raise TypeError(f"CONSTRUCTION ERROR : Provided output method is 0 (TIOW) but output destination type is not an instance of {type(stdout)}.")
        elif outputMethod == IO_METHOD.LIST and not isinstance(outputDest, list):
            raise TypeError(f"CONSTRUCTION ERROR : Provided output method is 1 (LIST) but output destination type is not an instance of list.")
        elif outputMethod == IO_METHOD.PIPE and not isinstance(outputDest, PipeConnection):
            raise TypeError(f"CONSTRUCTION ERROR : Provided output method is 2 (PIPE) but output destination type is not an instance of multiprocessing.Connection.")
        elif outputMethod != IO_METHOD.TIOW and outputMethod != IO_METHOD.LIST and outputMethod != IO_METHOD.PIPE:
            raise NotImplementedError(f"CONSTRUCTION ERROR : Provided output method is invalid : {outputMethod}")
        else:
            self.outputDest: {Union[TextIOWrapper, Connection, List]} = outputDest
            
        self.instPtr: int = 0 # Points to current instruction's Opcode's address
        self.relBase: int = 0 # Points to current "relative arg mode"'s base address
        
        self.args: Dict[int, int] = dict() # Contains current instruction's arguments's values
        self.argModes: Dict[int, ARG_MODE] = dict() # Contains current instruction's argument's modes
        self.opcode: OPCODE = None # Contains current opcode
        
        self.halt: bool = True # Tells wether or not the Intcom is currently halted

        ###############
        # CPU METHODS #
        ###############
        
    def _load(self, addr:int) -> int:
        """Loads a value from RAM

        Arguments:
            addr {int} -- Address to load

        Returns:
            int -- Value of RAM at given address
            
        Raises:
            ValueError -- Access to a negative address is forbidden
        """
        
        if addr < 0:
            raise ValueError(f"RAM ACCESS ERROR : Loading a negative address is forbidden (addr:{addr} / ptr:{self.instPtr})")
        elif addr not in self.ram:
            self.ram[addr] = 0
            return 0
        else:
            return self.ram[addr]
        
    def _write(self, addr:int, val:int) -> None:
        """Writes a given value to a given address in the RAM
        
        Arguments:
            addr {int} -- The address where to write the value
            val {int} -- The value to write
        
        Raises:
            ValueError -- Access to a negative address is forbidden
        """
        
        if addr < 0:
            raise ValueError(f"RAM ACCESS ERROR : Writing to a negative address is forbidden (addr:{addr} / ptr:{self.instPtr})")
        else:
            self.ram[addr] = val            
                
    def _fetch(self) -> None:
        """Implementation of a classic CPU's cycle's FETCH stage. Fills Intcom's properties
        with current instruction's value, and increment instPtr"""
        
        rawOpcode: int = self._load(self.instPtr)
        
        self.opcode = OPCODE(rawOpcode % 100) # Ones and Tens digits are the actual opcode.
        # All the other digits (even implicit 0s) are argument modes
        
        self.args = [self._load(self.instPtr+i)
                     for i in range(1,len(INSTR_ARG_SHAPE[self.opcode]))]
        
        self.argModes = []
        
        rawOpcode //= 10
        for i in range(len(INSTR_ARG_SHAPE[self.opcode])-1):
            rawOpcode //= 10
            self.argModes.append(rawOpcode%10)
        
        self.instPtr += len(INSTR_ARG_SHAPE[self.opcode])
        
    def _decode(self) -> None:
        """Implementation of a classic CPU's cycle's DECODE stage. Resolves arguments values."""
        
        for argIndex in range(len(self.args)):
            if INSTR_ARG_SHAPE[self.opcode][argIndex+1] == ARG_TYPE.VALUE:
                if self.argModes[argIndex] == ARG_MODE.IMM: # - --> Immediate mode doesn't change the value
                    self.args[argIndex] = self.args[argIndex]
                elif self.argModes[argIndex] == ARG_MODE.POS: # --> Positional mode loads given value
                    self.args[argIndex] = self._load(self.args[argIndex]) 
                elif self.argModes[argIndex] == ARG_MODE.REL: # --> Relative mode loads given value with relative base's offset
                    self.args[argIndex] = self._load(self.args[argIndex] + self.relBase)
                else:
                    raise NotImplementedError(f"ARGMODE ERROR : Argument mode {self.argModes[argIndex]} is not implemented (@ {self.instPtr})")
            
            elif INSTR_ARG_SHAPE[self.opcode][argIndex+1] == ARG_TYPE.ADDRESS:
                if self.argModes[argIndex] == ARG_MODE.IMM: # - --> Immediate mode raises an error
                    raise ValueError(f"ARGMODE ERROR : Address arguments can't be in immediate mode (@ {self.instPtr})")
                elif self.argModes[argIndex] == ARG_MODE.POS: # --> Positional mode doesn't change anything
                    self.args[argIndex] = self.args[argIndex]
                elif self.argModes[argIndex] == ARG_MODE.REL: # --> Relative mode just adds the offset to the value
                    self.args[argIndex] += self.relBase
                else:
                    raise NotImplementedError(f"ARGMODE ERROR : Argument mode {self.argModes[argIndex]} is not implemented (@ {self.instPtr})")

            else:
                raise NotImplementedError(f"ARGTYPE ERROR : Argument shape for opcode {self.opcode} does not exist.")
    
    def _execute(self) -> None:
        
        """Implementation of a classic CPU's cycle's DECODE stage. Executes the opcode's associated function"""
        
        if self.opcode == OPCODE.ADD:
            self._add()
        elif self.opcode == OPCODE.MUL:
            self._mul()
        elif self.opcode == OPCODE.IN:
            self._in()
        elif self.opcode == OPCODE.OUT:
            self._out()
        elif self.opcode == OPCODE.JIT:
            self._jit()
        elif self.opcode == OPCODE.JIF:
            self._jif()
        elif self.opcode == OPCODE.LT:
            self._lt()
        elif self.opcode == OPCODE.EQ:
            self._eq()
        elif self.opcode == OPCODE.URB:
            self._urb()
        elif self.opcode == OPCODE.HLT:
            print("HALT")
        else:
            raise NotImplementedError(f"OPCODE ERROR : opcode is undefined (opcode : {self.opcode} / ptr : {self.instPtr})")

        ######################
        # EXECUTIONS METHODS #
        ######################
        
    def _add(self) -> None:
        """Executes an addition instruction"""
        
        self._write(self.args[2], self.args[0]+self.args[1])
        
    def _mul(self) -> None:
        """Executes a multiplication instruction"""
        
        self._write(self.args[2], self.args[0]*self.args[1])
        
    def _in(self) -> None:
        """Executes an input instruction

        Raises:
            NotImplementedError: Raises an error if input method is invalid
        """
        
        if self.inputMethod == IO_METHOD.TIOW:
            buffer: str = self.inputSrc.read()
            if buffer[-1:] == '\n':
                buffer = buffer[:-1]
            self._write(self.args[0], int(buffer))
        elif self.inputMethod == IO_METHOD.LIST:
            self._write(self.args[0], int(self.inputSrc.pop()))
        elif self.inputMethod == IO_METHOD.PIPE:
            self._write(self.args[0], int(self.inputSrc.recv()))
        else:
            raise NotImplementedError(f"VALUE ERROR : input method is invalid : {self.inputMethod}")
        
    def _out(self) -> None:
        """Executes an output instruction

        Raises:
            NotImplementedError: Raises an error if output method is invalid
        """
        if self.outputMethod == IO_METHOD.TIOW:
            self.outputDest.write("Output -> "+str(self.args[0])+"\n")
        elif self.outputMethod == IO_METHOD.LIST:
            self.outputDest.insert(0, self.args[0])
        elif self.outputMethod == IO_METHOD.PIPE:
            self.outputDest.send(self.args[0])
        else:
            raise NotImplementedError(f"VALUE ERROR : output method is invalid : {self.outputMethod}")
        
    def _jit(self) -> None:
        """Executes a jump-if-true instruction"""
        
        if self.args[0] != 0:
            self.instPtr = self.args[1]
    
    def _jif(self) -> None:
        """Executes a jump-if-false instruction"""
        
        if self.args[0] == 0:
            self.instPtr = self.args[1]
            
    def _lt(self) -> None:
        """Executes a less-than instruction"""
        
        self._write(self.args[2], int(self.args[0] < self.args[1]))
        
    def _eq(self) -> None:
        """Executes an equals instruction"""
        
        self._write(self.args[2], int(self.args[0] == self.args[1]))
        
    def _urb(self) -> None:
        """Executes a update-relative-base instruction"""
        
        self.relBase += self.args[0]
        
    def _hlt(self) -> None:
        """Executes a halt instruction"""
        
        self.halt = True
        
    def run(self) -> None:
        """Runs the intcom with a classic CPU cycle (FETCH->DECODE->EXECUTE)"""
        
        self.halt = False # Down the halt flag to show the program starts running
        
        while not self.halt:
            self._fetch()
            self._decode()
            self._execute()
            
    # FUNCTIONS

    
def list_to_dict(l: List[int]) -> Dict[int, int]:
    """Takes an intcode as a list, and returns it as a dict ready to init an intcomputer's ram."""

    return {i: l[i] for i in range(len(l))}


def _run_piped_intcom(intcode: Dict[int, int], inPipe: PipeConnection, outPipe: PipeConnection) -> None:
    """Runs a computer specifically created"""

    ic: Intcomputer = Intcom(intcode, "Piped Intcom",
                             inputMethod=IO_METHOD.PIPE, outputMethod=IO_METHOD.PIPE,
                             inputSrc=inPipe, outputDest=outPipe)
    ic.run()


def piped_intcom_as_a_process(intcode: Dict[int, int], inPipe: PipeConnection, outPipe: PipeConnection) -> Process:
    """Returns a process ready to run specified intcode, I/O made by passed pipes"""

    return Process(target=_run_piped_intcom, args=(intcode, inPipe, outPipe))