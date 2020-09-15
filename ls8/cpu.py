"""CPU functionality."""


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # Ram 256 bytes
        self.RAM = [0] * 256
        # MAR Memory Address Register
        self.MAR = None
        # MDR Memory Data Register
        self.MDR = None
        # reg 8 bit
        self.reg = [0] * 8

        self.pc = 0

        self.running = False

    def load(self):
        """
        Load a program into memory.
        
        """

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010,  # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111,  # PRN R0
            0b00000000,
            0b00000001,  # HLT
        ]

        for instruction in program:
            self.RAM[address] = instruction
            address += 1

    # LDI: load "immediate", store a value in a register, or "set this register to this value".
    def LDI(self, loc, value):
        self.reg[loc] = value
        # self.pc += 3

    # PRN: a pseudo-instruction that prints the numeric value stored in a register
    def PRN(self, loc):
        print(self.reg[loc])
        # self.pc += 2

    # HLT: halt the CPU and exit the emulator
    def HLT(self):
        self.running = False

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def ram_read(self, address):
        return self.RAM[address]

    def ram_write(self, address, value):
        self.RAM[address] = value

    def run(self):
        # prebuilt functions
        LDI = 0b10000010
        PRN = 0b01000111
        HLT = 0b00000001
        """Run the CPU."""
        self.running = True
        # self.trace(self)
        while self.running:
            ir = self.ram_read(self.pc)

            if ir == LDI:
                self.LDI(2, self.RAM[2])
                self.pc += 3

            if ir == PRN:
                self.PRN(2)
                self.pc += 2

            if ir == HLT:
                self.HLT()
                # self.running = False
            else:
                print(f"Unknown instruction")