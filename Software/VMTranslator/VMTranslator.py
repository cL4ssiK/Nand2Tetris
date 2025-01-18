import sys
from Parser import Parser
from CodeWriter import CodeWriter


#TODO: Muokkaa codewriterin aritmeettisia lauseita siten että esim lt toimii x lt y kun nyt toimii y lt x. Eli ylempänä stackissa oleva viimeisenä.
def main():
    
    #args = sys.argv
    args = ['test.vm']
    if len(args) != 1:
        print("Invalid amount of arguments!")
        return
    
    parser = Parser(args[0], 'config.json')
    opf = args[0].split('.')[0] + '.asm'
    cw = CodeWriter(opf)
    cw.config('configWriter.json')

    while parser.has_more_lines():
        parser.advance()
        if parser.current_instruction[0] == '/':
            continue
        type = parser.command_type()
        command = parser.arg1()
        addr = parser.arg2()
        if type == 'C_ARITHMETIC':
            cw.write_arithmetic(command)
        elif type == 'C_PUSH' or type == 'C_POP':
            cw.write_push_pop(type, command, addr)
        elif type == 'C_LABEL':
            cw.write_label(command)
        elif type == 'C_GOTO':
            cw.write_goto(command)
        elif type == 'C_IF':
            cw.write_if(command)
        elif type == 'C_FUNCTION':
            cw.write_function(command, addr)
        elif type == 'C_CALL':
            cw.write_call(command, addr)
        elif type == 'C_RETURN':
            cw.write_return()    
        
    cw.close()
    parser.close()

if __name__ == "__main__":
    main()