import sys
import re
from SymbolTable import SymbolTable
from Parser import Parser
from Code import Code

# Working assembler. Prettify the code.

def main():
    #args = sys.argv
    args = ['test.asm']
    if len(args) != 1:
        print("Invalid amount of arguments!")
        return
    
    symbol_table = SymbolTable('symbols.json')
    coder = Code('instructions.json')

    code = []
    with open(args[0], "r") as file:
        
        # Add labels in symbol table.
        for line in file:
            if line[0] == '/':
                continue
            cleaned_line = re.sub(r"[ \n\t]", "", line)
            if cleaned_line != '': 
                if cleaned_line[0] == '(':
                    symbol_table.add_entry(re.sub(r"[()]", "", cleaned_line), len(code))
                else:
                    code.append(cleaned_line)
    
    with open(args[0].split('.')[0] + '.hack', 'w') as file:

        memory_address=16
        for line in code:
            it = Parser.instruction_type(line)
            if it == 'A_INSTRUCTION':
                s = Parser.symbol(line)
                if s.isdigit():
                    memory_address=int(s)+1
                    file.write('0' + format(int(s), '015b') + "\n")
                    continue

                elif not symbol_table.contains(s):
                    symbol_table.add_entry(s, memory_address)
                    memory_address += 1
                
                file.write('0' + format(int(symbol_table.get_address(s)), '015b') + "\n")

            if it == 'C_INSTRUCTION':
                dest = coder.dest(str(Parser.dest(line)))
                comp = coder.comp(Parser.comp(line))
                jump = coder.jump(str(Parser.jump(line)))
                file.write('111'+ comp + dest + jump + "\n")


if __name__ == "__main__":
    main()