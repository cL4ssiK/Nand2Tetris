import re

class Parser:

    def __init__(self, symbol_table, file):
        self.symbol_table = symbol_table
        self.parse(file)

    def parse(self, file):
        pass

    def symbol( line):
        return re.sub(r"[@()]", "", line)
    
    def dest(line):
        l = line.split('=')
        if len(l)>1:
            return l[0]
        return None
    
    def comp(line):
        l=line.split('=')
        return l[len(l)-1].split(';')[0]

    def jump(line):
        l = line.split(';')
        if len(l)>1:
            return l[1]
        return None

    #TODO: Some sort of error handling if not correct c instruction
    def instruction_type(instruction):
        if instruction[0] == '@':
            return 'A_INSTRUCTION'
        if instruction[0] == '(':
            return 'L_INSTRUCTION'
        return 'C_INSTRUCTION'

inst='D=D+1;JLE'
print(Parser.dest(inst))
print(Parser.comp(inst))
print(Parser.jump(inst))
inst = '0;JMP'
print(Parser.dest(inst))
print(Parser.comp(inst))
print(Parser.jump(inst))