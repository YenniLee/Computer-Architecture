import sys

# Write a program in Python that runs programs

# Parse the command line
program_filename = sys.argv[1]

PRINT_BEEJ = 1
HALT = 2
SAVE_REG = 3   # Store a value in a register (in the LS8 called LDI)
PRINT_REG = 4  # corresponds to PRN in the LS8
PUSH = 5
POP = 6
CALL = 7
RET = 8

"""
memory = [
	PRINT_BEEJ,

	SAVE_REG,    # SAVE R0,37   store 37 in R0      the opcode
	0,  # R0     operand ("argument")
	37, # 37     operand

	PRINT_BEEJ,

	PRINT_REG,  # PRINT_REG R0
	0, # R0

	HALT
]
"""

memory = [0] * 256
register = [0] * 8   # like variables R0-R7

# R7 is the SP
SP = 7
register[SP] = 0xF4

# Load program into memory
address = 0

with open(program_filename) as f:
	for line in f:
		line = line.split('#')
		line = line[0].strip()

		if line == '':
			continue

		memory[address] = int(line)

		address += 1

#print(type(memory[0]))
#sys.exit()

pc = 0 # Program Counter, the address of the current instruction
running = True

while running:
	inst = memory[pc]

	if inst == PRINT_BEEJ:
		print("Beej!")
		pc += 1

	elif inst == SAVE_REG:
		reg_num = memory[pc + 1]
		value = memory[pc + 2]
		register[reg_num] = value
		pc += 3

	elif inst == PRINT_REG:
		reg_num = memory[pc + 1]
		value = register[reg_num]
		print(value)
		pc += 2
                          
	elif inst == PUSH:
		# decrement the stack pointer
		register[SP] -= 1   # address_of_the_top_of_stack -= 1

		# copy value from register into memory
		reg_num = memory[pc + 1]
		value = register[reg_num]  # this is what we want to push

		address = register[SP]    # addr of the new top of that stack
		memory[address] = value   # store the value on the stack

		pc += 2

	elif inst == POP:
		# copy value from register into memory
		reg_num = memory[pc + 1]

		address = register[SP]   # addr of item on the top of the stack
		value = memory[address]  # this is the value we popped

		register[reg_num] = value   # store the value in the register

		pc += 2

		# increment the stack pointer
		register[SP] += 1   # address_of_the_top_of_stack -= 1

	elif inst == CALL:
		# compute return address
		return_addr = pc + 2

		# push on the stack
		register[SP] -= 1
		memory[register[SP]] = return_addr

		# Set the PC to the value in the given register
		reg_num = memory[pc + 1]
		dest_addr = register[reg_num]

		pc = dest_addr

	elif inst == RET:
		# pop return address from top of stack
		return_addr = memory[register[SP]]
		register[SP] += 1

		# Set the pc
		pc = return_addr

	elif inst == HALT:
		running = False

	else:
		print("Unknown instruction")
		running = False


"""
Why does bitwise NOT (~) produce negative numbers?
​
It has to do with how negative numbers are represented in memory. It's done
with something called _2's Complement_.
​
For this week, we've been assuming all numbers are unsigned, i.e. only
positive.
​
Which means that an 8 bit 255 is 0b11111111. And 0 is 0b00000000.
​
But there's no room there for negatives.
​
So 2's complement was created. It uses the same bit patterns for positive
numbers, but reserves others for negatives.
​
Notably, any number with a 1 bit for the high (left) bit is a negative number.
​
The output of this program is:
​
    Signed:
​
      8 0b00001000
      7 0b00000111
      6 0b00000110
      5 0b00000101
      4 0b00000100
      3 0b00000011
      2 0b00000010
      1 0b00000001
      0 0b00000000
     -1 0b11111111
     -2 0b11111110
     -3 0b11111101
     -4 0b11111100
     -5 0b11111011
     -6 0b11111010
     -7 0b11111001
     -8 0b11111000
​
    Unsigned:
​
      8 0b00001000
      7 0b00000111
      6 0b00000110
      5 0b00000101
      4 0b00000100
      3 0b00000011
      2 0b00000010
      1 0b00000001
      0 0b00000000
    255 0b11111111
    254 0b11111110
    253 0b11111101
    252 0b11111100
    251 0b11111011
    250 0b11111010
    249 0b11111001
    248 0b11111000
​
Notice how the bit pattern for 255 is exactly the same as the bit pattern for
-1!
​
So the NOT is working... it's taking 0b00000000 and turning it into 0b11111111.
And that _would_ be 255 unsigned.
​
However, Python prints things out as _signed_ by default, so your 0b11111111
becomes -1.
​
You can override this behavior by bitwise ANDing the number with a mask to
force it positive, like the bin8() function does, below.
​
"""
​
def bin8(v):
    #             AND with 0b11111111
    #                vvv
    return f'0b{v & 0xff:08b}'
    #                    ^^^
    #     Print binary with field width 8 and pad with leading zeros
​
print("Signed:\n")
​
for i in range(8, -9, -1):
    print(f'{i:3} {bin8(i)}')
​
print("\nUnsigned:\n")
​
for i in range(8, -1, -1):
    print(f'{i:3} {bin8(i)}')
for i in range(255, 247, -1):
    print(f'{i:3} {bin8(i)}')



"""
Branchtable Notes
"""

def func1(a):
	print("func1", a)
​
def func2(a):
	print("func2", a)
​
def func3(a):
	print("func3", a)
​
def func4(a):
	print("func4", a)
​
def call_func(n, a):
	"""
	if n == 1:
		func1()
	elif n == 2:
		func2()
	elif n == 3:
		func3()
	elif n == 4:
		func4()
	"""
	branch_table = {
		1: func1,
		2: func2,
		3: func3,
		4: func4
	}
​
	# branch_table[n]()
	f = branch_table[n]
	f(a)
​
​
call_func(2, "hi")
call_func(4, "test")
call_func(1, "hello")
