import json

class CodeWriter:


    def __init__(self, output_file):
        self.out = open(output_file, 'w')
        self.segment_table = dict()
        self.unique_label = 0


    #TODO: find a better way to do this. some sort of key value thing?
    def write_arithmetic(self, command):
        asm = '@SP\nAM=M-1\nD=M\n@SP\nAM=M-1\n'
        if command == 'neg':
            asm = '@SP\nAM=M-1\nM=-M\n'
        elif command == 'not':
            asm = '@SP\nAM=M-1\nM=!M\n'

        elif command == 'add':
            asm += 'M=D+M\n'
        elif command == 'sub':
            asm += 'M=M-D\n'

        elif command == 'gt':
            asm += 'D=D-M\n@GTT' + str(self.unique_label) + '\nD;JGT\n@SP\nA=M\nM=0\n@GTE' + str(self.unique_label) + '\n0;JMP\n(GTT' + str(self.unique_label) + ')\n@SP\nA=M\nM=-1\n(GTE' + str(self.unique_label) + ')\n'
        elif command == 'lt':
            asm += 'D=D-M\n@LTT' + str(self.unique_label) + '\nD;JLT\n@SP\nA=M\nM=0\n@LTE' + str(self.unique_label) + '\n0;JMP\n(LTT' + str(self.unique_label) + ')\n@SP\nA=M\nM=-1\n(LTE' + str(self.unique_label) + ')\n'
        elif command == 'eq':
            asm += 'D=D-M\n@ETT' + str(self.unique_label) + '\nD;JEQ\n@SP\nA=M\nM=0\n@ETE' + str(self.unique_label) + '\n0;JMP\n(ETT' + str(self.unique_label) + ')\n@SP\nA=M\nM=-1\n(ETE' + str(self.unique_label) + ')\n'
        
        elif command == 'and':
            asm += 'D=D&M\nD=D+1\n@ANDT' + str(self.unique_label) + '\nD;JEQ\n@SP\nA=M\nM=0\n@ANDE' + str(self.unique_label) + '\n0;JMP\n(ANDT' + str(self.unique_label) + ')\n@SP\nA=M\nM=-1\n(ANDE' + str(self.unique_label) + ')\n'
        elif command == 'or':
            asm += 'D=D|M\nD=D+1\n@ORT' + str(self.unique_label) + '\nD;JEQ\n@SP\nA=M\nM=0\n@ORE' + str(self.unique_label) + '\n0;JMP\n(ORT' + str(self.unique_label) + ')\n@SP\nA=M\nM=-1\n(ORE' + str(self.unique_label) + ')\n'
        
        asm += '@SP\nM=M+1\n'
        self.unique_label += 1
        
        self.out.write(asm)
        

    def write_push_pop(self, command, segment, index):

        base_address = self.segment_table.get(segment)
        if segment == 'static':
            base_address = self.filename + '.' + base_address
        asm = ''
        
        if base_address is not None:
            asm += '@' + base_address + '\nD=M\n'
            asm += '@' + str(index) + '\n'
        
        if command == 'C_PUSH':
            if segment == 'constant':
                asm += '@' + str(index) + '\nD=A\n'
            elif base_address == 'R1' or base_address == 'R2' or base_address == 'R3' or base_address == 'R4':
                pass
            else:
                asm += 'A=D+A\nD=M\n'
            asm += '@SP\nA=M\nM=D\n'

        elif command == 'C_POP':
            asm += 'D=D+A\n@R13\nM=D\n@SP\nM=M-1\nA=M\nD=M\n@R13\nA=M\nM=D\n'

        inc = '@SP\nM=M+1\n'
        asm += inc
        self.out.write(asm)


    def write_label(self, label):
        self.out.write('(' + label + ')\n')


    def write_goto(self, label):
        self.out.write('@' + label + '\n0;JMP\n')


    def write_if(self, label):
        self.out.write('@SP\nA=M\nD=M+1\n@' + label + '\nD;JEQ\n')


    def write_function(self, function_name, n_vars):
        self.write_label(function_name)
        for i in range(int(n_vars)):
            self.write_push_pop('C_PUSH', 'constant', 0)


    def write_call(self, function_name, n_args):
        label = function_name + '$ret.' + str(self.unique_label)
        self.out.write('@' + label + '\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n') # Push return address to the stack
        self.write_push_pop('C_PUSH', 'LCL', 0)
        self.write_push_pop('C_PUSH', 'ARG', 0)
        self.write_push_pop('C_PUSH', 'THIS', 0)
        self.write_push_pop('C_PUSH', 'THAT', 0)
        self.out.write('@SP\nD=M\n@' + str(5 + int(n_args)) + '\nD=D-A\n@ARG\nM=D\n') # Repositioning ARG
        self.out.write('@SP\nD=M\n@LCL\nM=D\n') # Reposition LCL
        self.write_goto(function_name) # Go to label
        self.write_label(label) # Create label for return address
        self.unique_label += 1
        

    def write_return(self): 
        self.out.write('@LCL\nD=M\n@R5\nM=D\n') # endFrame = LCL
        self.out.write('@5\nD=A\n@R5\nD=M-D\nA=A+1\nM=D\n') # retAdd r = *(endFrame - 5)
        self.out.write('@SP\nM=M-1\nA=M\nD=M\n@ARG\nA=M\nM=D\n') # *ARG = pop()
        self.out.write('D=A\n@SP\nM=D+1\n') # SP = ARG + 1
        self.out.write('@R5\nD=M-1\n@THAT\nM=D\n') # THAT = *(endFrame - 1)
        self.out.write('D=D-1\n@THIS\nM=D\n') # THIS = *(endFrame - 2)
        self.out.write('D=D-1\n@ARG\nM=D\n') # ARG = *(endFrame - 3)
        self.out.write('D=D-1\n@LCL\nM=D\n') # LCL = *(endFrame - 4)
        self.out.write('@R5\nA=A+1\nA=M\n0;JMP\n') # goto retAddr



    def close(self):
        self.out.close()


    def config(self, conf_file):
        with open(conf_file, 'r') as file:
            temp = json.load(file)
            for item in temp:
                    self.segment_table[item['segment']] = item['address']

    # Initialize stack pointer and jump to sys.init function.
    def write_bootstrap(self):
        self.out.write('@256\nD=A\n@SP\nM=D\n') 
        self.write_goto('sys.init')

    
    def update_filename(self, directory):
        temp = directory.rsplit('\\')
        self.filename = temp[len(temp)-1].split('.')[0]
        


cw = CodeWriter('opf.asm')
cw.config('configWriter.json')

#cw.write_push_pop('C_POP', 'local', 2)
#print('\n')
#cw.write_push_pop('C_PUSH', 'argument', 5)
#print('\n')
#cw.write_push_pop('C_PUSH', 'constant', 23)
#print('\n')
#cw.write_push_pop('C_PUSH', 'LCL', 0)
#print('\n')
#cw.write_push_pop('C_PUSH', 'pointer', 1)
#print('\n')
#cw.write_call('file.func', 3)
#cw.write_function('file.func', 4)

