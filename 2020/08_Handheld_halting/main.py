#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

# Read the program instructions
program = []
with open("input.txt", "r") as f:
    for line in f:
        (instruction, value) = [ (ins[0], int(ins[1])) for ins in re.findall(r"([a-z]*)\s([+|-][\d]+)", line) ][0]

        # Save the instruction in the program
        program.append([instruction, value])

# Run the program, checking whether one instruction has already been executed
def runProgram(thisProgram):
    executed = [0] * len(thisProgram)
    accumulator = 0
    pointer = 0
    while pointer < len(thisProgram):
        # If the current instruction has already been executed, break the loop
        if executed[pointer] == 1:
            break
        # Otherwise, run the instruction
        else:
            if thisProgram[pointer][0] == "acc":
                # Increase/decrease the accumulator
                accumulator += thisProgram[pointer][1]
                # Mark the instruction as executed
                executed[pointer] = 1
                # Add one to the pointer
                pointer += 1

            elif thisProgram[pointer][0] == "jmp":
                # Mark the instruction as executed
                executed[pointer] = 1
                # Add one to the pointer
                pointer += thisProgram[pointer][1]

            elif thisProgram[pointer][0] == "nop":
                # Mark the instruction as executed
                executed[pointer] = 1
                # Add one to the pointer
                pointer += 1
    return accumulator, pointer

accumulator = runProgram(program)[0]

print("Last value of the accumulator {}".format(accumulator))
print("\n----------\n")

# Fix the program by changin one jmp to nop or a nop to jmp
lastPointer = 0
accumulator = 0
# Find the positions of the jmp and nop instructions
jmpIndices = []
nopIndices = []
for i in range(len(program)):
    if program[i][0] == "jmp":
        jmpIndices.append(i)
    elif program[i][0] == "nop":
        nopIndices.append(i)

# Try changing a jmp to a nop
# The exit condition is that the last pointer is equal to the length of the program
i = 0
while lastPointer < len(program):
    # Modify the program
    program[jmpIndices[i]][0] = "nop"
    # Run the modified program
    accumulator, lastPointer = runProgram(program)
    # Put the program back in its original state
    program[jmpIndices[i]][0] = "jmp"
    # Add one to the index
    i += 1

# Try changing a nop to a jmp
# Check first if we found a successful fix before
if lastPointer != len(program):
    i = 0
    while lastPointer < len(program):
        # Modify the program
        program[nopIndices[i]][0] = "jmp"
        # Run the modified program
        accumulator, lastPointer = runProgram(program)
        # Put the program back in its original state
        program[nopIndices[i]][0] = "nop"
        # Add one to the index
        i += 1

print("Last value of the accumulator {}".format(accumulator))
