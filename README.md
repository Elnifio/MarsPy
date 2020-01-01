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

Then, you should see a `.py` file under `mips` folder. **move this file to the src folder** (since I don't know how to import module in different folder XD) and then you could run the model using `python3 $FILE_NAME.py`.

For instance, a complete procedure to run `sum.asm` should be:
1. `cd` to src folder (and check you have installed Python!)
2. run `python3 parser.py`
3. type in `sum.asm`
4. `mv ./mips/sum.py .` 
5. `python3 sum.py`

## Model usage:

