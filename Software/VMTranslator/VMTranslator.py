import sys
import os
from Parser import Parser
from CodeWriter import CodeWriter


class VMTranslator:

    def __init__(self, folder_name):
        # Create object to write code to output file.
        output_file_name = folder_name.split('.')[0] + '.asm'
        self.cw = CodeWriter(output_file_name)
        self.cw.config('configWriter.json')


    def translate_file(self, file_name):
        parser = Parser(file_name, 'config.json')

        while parser.has_more_lines():
            parser.advance()

            # Remove empty lines and comments
            if parser.current_instruction == '':
                continue
            
            type = parser.command_type()
            command = parser.arg1()
            addr = parser.arg2()

            if type == 'C_ARITHMETIC':
                self.cw.write_arithmetic(command)

            elif type == 'C_PUSH' or type == 'C_POP':
                self.cw.write_push_pop(type, command, addr)

            elif type == 'C_LABEL':
                self.cw.write_label(command)

            elif type == 'C_GOTO':
                self.cw.write_goto(command)

            elif type == 'C_IF':
                self.cw.write_if(command)

            elif type == 'C_FUNCTION':
                self.cw.write_function(command, addr)

            elif type == 'C_CALL':
                self.cw.write_call(command, addr)

            elif type == 'C_RETURN':
                self.cw.write_return()    

        parser.close()

    def translate_folder(self, folder_name):
        for filename in os.listdir(folder_name):
            file_path = os.path.join(folder_name, filename)

            # Take out folders inside folders.
            if not os.path.isfile(file_path):
                continue
            # Take out every file that is not labeled .vm
            if filename.split('.')[1] != 'vm':
                continue

            self.translate_file(file_path)



#TODO: Muokkaa codewriterin aritmeettisia lauseita siten että esim lt toimii x lt y kun nyt toimii y lt x. Eli ylempänä stackissa oleva viimeisenä.
#TODO: Make this able to handle multi file translations. 
def main():
    
    #args = sys.argv
    args = ['testFolderTranslation']
    if len(args) != 1:
        print("Invalid amount of arguments!")
        sys.exit(1)
    
    folder_name = args[0]
    directory_path = os.path.join(os.getcwd(), folder_name)

    if not (os.path.isdir(directory_path) or os.path.isfile(directory_path)):
        print(f"Error: {directory_path} is not a valid folder.")
        sys.exit(1)

    vmt = VMTranslator(folder_name)

    if os.path.isdir(directory_path):
        vmt.translate_folder(folder_name)
    else:
        vmt.translate_file(folder_name)
        
    vmt.cw.close()

        

if __name__ == "__main__":
    main()