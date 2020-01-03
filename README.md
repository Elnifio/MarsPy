# MarsPy
A MIPS Assembler and Runtime Simulator implemented in Python

This Simulator includes two parts: a parser that translates `.asm` file to `.py` file, and a model that reads in instructions line by line and executes them. 

If you wish to use these codes, Python 3.7+ is recommended (since this is the version installed on my computer. I'm not sure if this is compatible with other versions).

## Parser usage:
If you wish to use the parser, you should first check if you have installed required Python version, and then pull all contents in the `src` folder to your computer. 

After that, open the terminal (command palette), and `cd` to the src folder, and use `ls` to check if all contents are present if necessary. 

Put your `.asm` file under `src/mips` folder, and run command `python3 parser.py` (Might be different on PC). 
you will be prompted to enter the file name, 
please enter **full file name, including `.asm`, but not including its folder name**. 
For instance, if you wish to parse `sum.asm` which is under `src` folder, you should now enter `sum.asm`.

Then, you should see a `.py` file under `mips` folder. **Move this file to the src folder** and then you could run the model using `python3 $FILE_NAME.py`.

For instance, a complete procedure to run `sum.asm` should be:
1. `cd` to src folder (and check you have installed Python!)
2. run `python3 parser.py`
3. type in `sum.asm`
4. `mv ./mips/sum.py .` 
5. `python3 sum.py`

## Model usage:
You should use the `model.run_instructions(insts, memory, registers_to_print={}, step_by_step=False, debug=False)` method for running the model. 
The parameter list is defined as follow:

1. insts: A dictionary containing all MIPS instructions. Every element is a key-value set of structure <Instruction Address - Instruction Basic>, such as `"0x00003000": "addi $8, $9, 12"`. Notice that register aliases should not be used here. 
2. memory: A sim_mem.Memory object (or any other objects with equivalent methods)
3. registers_to_print: an iterable object which contains all registers that needs to be printed. The program will print out the register and its corresponding value before and after running the model. Default set to {} (which means no registers are printed)
4. step_by_step: A Boolean that toggles the step-by-step mode. Under step-by-step mode, instructions will be printed out each time before its execution and pause until Enter (Return) key is pressed. Default set to False.
5. debug: A Boolean that toggles the Debug mode. Under debug mode, all registers will be printed when an Error is catched for debugging. Default set to False.
  
You could see `model.py` for more detailed description, or see `samples.py` for sample programs.

## Using Samples.py
Samples.py contains 5 sample programs. You could run them using `python3 samples.py`, and select the corresponding program according to the prompt. 

#### Sample introductions
sum: calculate `0 + 1 + 2 + 3 + 4`, result stored in `$8`.

sumArray: stores the list `[7, 8, 9, 10, 8]` to memory, and sums using a loop. Result stored in `$8`.

Fibonacci: Calculate the largest Fibonacci number smaller than 100. Result stored in `$8` and memory address 0x0. (The first Fibonacci number larger than 100 is stored in 0x4)

Matrix Multiplication: Calculate the product of two matrices using triple loops. Matrix size (no larger than 10 * 10) and every entry of the two matrices should be entered. Result printed to output. 

Make Patterns: Generates and prints binary patterns of given length using recursion. Pattern length should be entered. Result printed to output. 

- - -
## Defects & Differences with MARS
Because I cannot find a substitution for `fgets` in Python, I cannot implement a similar function. 
Hence, the simulator cannot recognize `syscall 12` (which is Read Character). 
Meanwhile, some MIPS codes should be modified to adapt to the new `syscall 8`. 
Because `input()` method cannot limit the lenght of input string, 
*Return* key should be pressed each time to store the corresponding value to the memory. 
As a result, we cannot implement the same function as fgets() in C, 
and therefore cannot implement the "Read Character" function. 

> For instance, if we restrict the length of the string read in to be 2 (which means `$a1 = 3`), the system will not automatically continue when more than two characters are entered. Instead, the system will always expect a *Return* signal after input finished. However, in MARS and C, the system will force stop the input and continues the program when the string length limit is reached. 

The second defect is that this simulator cannot calculate float and double calculations, including general "divide" operation. Only some basic and frequent commands are supported. 

The third defect is that **Pseudo-codes cannot be recognized** (such as Load Address and Load Immediate). In addition, some more "convenient" operations cannot be completed automatically (for instance, we cannot calculate `ori $8, $9, -1` directly. The effect of this instruction is simply `$8 = $9 | 0x0000FFFF`).

For .ascii and .asciiz:

When several arguments are given for a `.asciiz & .ascii` argument, this simulator would include any characters used to split these arguments, while MARS will store every values to the memory correctly. 
For instance, consider this code: 
```
.data 0x0
asterisk: .asciiz "*"
period: .asciiz "."
start: .asciiz "S"
finish: .asciiz "F"
space: .asciiz " "
newline: .asciiz "\n"
pound: .ascii "this is a test for storing \"#\"" "this is another annotation"
quote: .asciiz "\""
```
MARS would define the address of `pound` at `0x0C`, and the address of `quote` at `0x46`. 

However, this simulator would give the address of `quote` at `0x48`, including the space between these two arguments. 

> This operation is strongly deprecated, since under this circumstance we cannot directly access the second value using Labels and `la` instructions. It might also cause some malfunctions in this simulator since the memory address is not exactly the same and extra arguments are added to functions when calculating (especially `syscall 4` for printing the string) the result. 

This simulator **cannot recognize continuous spaces** due to a severe structural defect. If you wish to print continuous spaces, please be aware of this defect. We recommend you to print white space using an independent function, instead of storing them into `.asciiz` literal. 

For every operations that involves immediates, if hexadecimal literals are entered, this simulator cannot recognize 2's Complement representation. All hex literals are treated as Signed Representation. 

## Other contents
Nearly every module has comments. If you have any questions about a function, we recommend you read the comments first.
If you have any other questions, please raise issues under this project. 

