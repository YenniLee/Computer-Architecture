"""
Number Bases 
------------
12 apples
0xC apples
1100 apples (in binary)

Binary   Base 2
Octal    Base 8
Decimal  Base 10
Hex      Base 16
         Base 64

# ff 7f 00 (values of red blue yellow)

to let python know that a number is in binary add 0b
a = 0b1101
a = 0xFF to let python know it is a hexadecimal number

Binary to Hex 
-------------
4 binary digits == 1 hex digit

bit is short for binary digits

11010011

1101 0011 
  d   3

0b11010011 == 0xd3 (binary --> hex converesion)

0xff 
    f       f
  1111    1111 
  0b11111111  == 255  == 0xff


Byte is 8 bits
"""

# Write a program in Python that runs programs

# PRINT_BEEJ = 1
# HALT = 2
# SAVE_REG = 3 # Store a value in a register (in the LS8 called LDI)
# PRINT_REG = 4 # corresponds to PRN in the LS8

# memory = [
#     PRINT_BEEJ,
#     SAVE_REG,    # SAVE R0, 37 store 37 in R0  the opcode (instruction byte)
#     0, # R0 operand ('argument')
#     37, # 37 operand('argument')
#     PRINT_BEEJ,
#     PRINT_REG, # PRINT_REG R0
#     0, # R0
#     HALT
# ]

# register = [0] * 8 # like variables R0-R7

# pc = 0 # Program Counter, the address of the current instruction
# running = True

# while running:
#     inst = memory[pc]

#     if inst == PRINT_BEEJ:
#         print("Beej!")
#         pc += 1
    
#     elif inst == SAVE_REG:
#         reg_num = memory[pc + 1]
#         value = memory[pc + 2]
#         register[reg_num] = value
#         pc += 3
    
#     elif inst == PRINT_REG:
#         reg_num = memory[pc + 1]
#         value = register[reg_num]
#         print(value)
#         pc += 2


#     elif inst == HALT:
#         running = False

#     else:
#         print("Unknown Instruction")
#         running = False

'''
Given an object/dictionary with keys and values that consist of both strings and integers, design an algorithm to calculate and return the sum of all of the numeric values.
For example, given the following object/dictionary as input:
{
  "cat": "bob",
  "dog": 23,
  19: 18,
  90: "fish"
}
Your algorithm should return 41, the sum of the values 23 and 18.
'''

def nums_sums(x):
    total = 0
    
    for i in x:
        if type(x[i]) == int:
            total += x[i]
     
    return total
        
print(nums_sums({
    "cat": "bob",
  "dog": 23,
  19: 18,
  90: "fish"
}))
    



