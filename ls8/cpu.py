"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""
    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0b00000000] * 256
        self.register = [0] * 8
        self.pc = 0
        self.instruction = {
            "0010": self.ldi,
            "0111": self.prn,
            "0001": self.hlt
        }
    def ram_read(self, address):
        #return value stored
        return self.ram[address]
    
    def ram_write(self, value, address):
        self.ram[address] = value

    def load(self):
        """Load a program into ram."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    # def trace(self):
    #     """
    #     Handy function to print out the CPU state. You might want to call this
    #     from run() if you need help debugging.
    #     """

    #     print(f"TRACE: %02X | %02X %02X %02X |" % (
    #         self.pc,
    #         #self.fl,
    #         #self.ie,
    #         self.ram_read(self.pc),
    #         self.ram_read(self.pc + 1),
    #         self.ram_read(self.pc + 2)
    #     ), end='')

    #     for i in range(8):
    #         print(" %02X" % self.reg[i], end='')

    #     print()

    def run(self):
        while True:
            ir = self.ram[self.pc]
            # print("pc: ", self.pc)
            byte = bin(ir)[2:].zfill(8)
            # print("byte ", byte)
            deconstruct = "0b" + byte
            # print("deconstruct ", deconstruct)
            aa = deconstruct[2:4]
            b = deconstruct[4:5]
            c = deconstruct[5:6]
            dddd = deconstruct[6:]
            opA = None
            opB = None

            # print("aa", aa)

            if aa == "01":
                self.pc += 1
                opA = self.ram[self.pc]
            elif aa== "10":
                self.pc += 1
                opA = self.ram[self.pc]
                self.pc += 1
                opB = self.ram[self.pc]
            # print("opa: ", opA)
            # print("opb: ", opB)
            # print("dddd: ", dddd)

            if opA is not None and opB is not None:
                self.instruction[dddd](opA, opB)
            elif opA is None and opB is not None:
                self.instruction[dddd](opB)
            elif opA is not None and opB is None:
                self.instruction[dddd](opA)
            else:
                self.instruction[dddd]()

    def ldi(self, opA, opB):
        self.register[opA] = opB
        self.pc += 1

    def prn(self, opA):
        print(self.register[opA])
        self.pc += 1

    def hlt(self):
        exit()