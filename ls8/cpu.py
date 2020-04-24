import sys

# set OP codes
LDI = 0b10000010
PRN = 0b01000111
HLT = 0b00000001
MUL = 0b10100010
ADD = 0b10100000
PUSH = 0b01000101
POP = 0b01000110
CALL = 0b01010000
RET = 0b00010001
CMP = 0b10100111
JMP = 0b01010100
JNE = 0b01010110
JEQ = 0b01010101
AND = 0b10101000
OR = 0b10101010
XOR = 0b10101011
NOT = 0b01101001
SHL = 0b10101100
SHR = 0b10101100
MOD = 0b10100100

SP = 7

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.register = [0] * 8
        self.ram = [0] * 256
        self.pc = 0
        self.fl = 0

        # implement branchtable
        self.bt = {
            HLT: self.HLT,
            MUL: self.alu,
            ADD: self.alu,
            PUSH: self.PUSH,
            POP: self.POP,
            LDI: self.LDI,
            PRN: self.PRN,
            CALL: self.CALL,
            RET: self.RET,
            CMP: self.alu,
            JMP: self.JMP,
            JNE: self.JNE,
            JEQ: self.JEQ,
            AND: self.alu,
            OR: self.alu,
            XOR: self.alu,
            NOT: self.alu,
            SHL: self.alu,
            SHR: self.alu,
            MOD: self.alu
        }

    def load(self, filename):
        """Load a program into memory."""

        address = 0

        try:
            with open(filename) as f:
                for line in f:
                    # ignore # comments
                    comments_removed = line.split("#")
                    # remove spaces
                    num = comments_removed[0].strip()

                    # ignore blank lines
                    if num == '':
                        continue

                    # convert to integer
                    value = int(num, 2)

                    # write and increment
                    self.ram_write(address, value)
                    address += 1

        except FileNotFoundError:
            print(f" {sys.argv[0]}: {filename} not found")
            sys.exit(2)

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == ADD:
            self.register[reg_a] += self.register[reg_b]
            self.pc += 3

        elif op == MUL:
            self.register[reg_a] *= self.register[reg_b]
            self.pc += 3
        
        elif op == CMP:
            '''
            * `L` Less-than: during a `CMP`, set to 1 if registerA is less than registerB,
             zero otherwise.
*           `G` Greater-than: during a `CMP`, set to 1 if registerA is greater than
            registerB, zero otherwise.
            * `E` Equal: during a `CMP`, set to 1 if registerA is equal to registerB, zero
            otherwise.
            '''
            if self.register[reg_a] < self.register[reg_b]:
                self.fl = 0b00000001 # set flag to 1
            
            elif self.register[reg_a] > self.register[reg_b]:
                self.fl = 0b00000010 # set flag to 2
            
            elif self.register[reg_a] == self.register[reg_b]:
                self.fl = 0b00000100 # set flag to 4
            self.pc += 3

        elif op == AND:
            self.register[reg_a] = self.register[reg_a] & self.register[reg_b]
            self.pc += 3
        
        elif op == OR:
            self.register[reg_a] = self.register[reg_a] or self.register[reg_b]
            self.pc += 3

        elif op == XOR:
            self.register[reg_a] = self.register[reg_a] ^ self.register[reg_b]
            self.pc += 3

        elif op == NOT:
            self.register[reg_a] = ~self.register[reg_a]
            self.pc += 2

        elif op == SHL:
            self.register[reg_a] = self.register[reg_a] << self.register[reg_b]
            self.pc += 3

        elif op == SHR:
            self.register[reg_a] = self.register[reg_a] >> self.register[reg_b]
            self.pc += 3

        elif op == MOD:
            if self.register[reg_b] == 0:
                print("ERROR: Cannot divide by 0")
                sys.exit(1)
            self.register[reg_a] %= self.register[reg_b]
            self.pc += 3
        

     
        else:
            raise Exception("Unsupported ALU operation")
    
    def ram_read(self, address_to_read):
        return self.ram[address_to_read]

    def ram_write(self, address_to_write, value):
        self.ram[address_to_write] = value

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.register[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        while True:
            # read memory address stored in pc, set that to ir, read command
            ir = self.pc
            op = self.ram_read(ir)

            # get operand_a and _b in case we need them
            operand_a = self.ram_read(ir + 1)
            operand_b = self.ram_read(ir + 2)

            if op in self.bt:
                if op in [ADD, MUL, CMP]:
                    self.bt[op](op, operand_a, operand_b)
                elif op >> 6 == 0:
                    self.bt[op]()
                elif op >> 6 == 1:
                    self.bt[op](operand_a)
                elif op >> 6 == 2:
                    self.bt[op](operand_a, operand_b)
            else:
                print(f"Unknown instruction: {op}")
                sys.exit(1)

    # set register at operand_a to value of operand_b
    def LDI(self, operand_a, operand_b):
        self.register[operand_a] = operand_b
        self.pc += 3
    
    # print operand
    def PRN(self, operand_a):
        print(self.register[operand_a])
        self.pc += 2

    # copy register value to ram, decrement sp
    def PUSH(self, reg_a):
        self.register[SP] -= 1
        self.ram[self.register[SP]] = self.register[reg_a]
        self.pc += 2

    # copy ram to register, increment sp
    def POP(self, reg_a):
        self.register[reg_a] = self.ram[self.register[SP]]
        self.register[SP] += 1
        self.pc += 2

    def HLT(self):
        sys.exit(0)

    def CALL(self, reg_a):
        # compute return address
        return_addr = self.pc + 2

        # push on to stack
        self.register[SP] -= 1
        self.ram[self.register[SP]] = return_addr

        # set the PC to the value in the given register
        self.pc = self.register[reg_a]

    def RET(self):
        # pop return address from top of stack 
        return_addr = self.ram[self.register[SP]]
        self.register[SP] += 1

        # set the pc countner
        self.pc = return_addr

    def JMP(self, reg_a):
        # set the pc to the address stored in given register
        self.pc = self.register[reg_a]
    
    def JNE(self, reg_a):
        # if E flag is false/0, jump to address in given register
        if self.fl != 0b00000100:
            self.JMP(reg_a)
        else:
            self.pc +=2
    
    def JEQ(self, reg_a):
        # if `equal` flag is true, jump to address stored in given register
        if self.fl == 0b00000100:
            self.JMP(reg_a)
        else:
            self.pc += 2

