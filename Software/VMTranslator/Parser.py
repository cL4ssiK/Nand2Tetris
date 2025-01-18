import json

class Parser:

    def __init__(self, source, config):
        self.file = open(source, 'r')
        self.current_instruction = None
        self.command_table = dict()
        
        with open(config, 'r') as file:
            temp = json.load(file)
            for type in temp:
                    for item in temp[type]:
                        self.command_table[item] = type
            


    def has_more_lines(self):
        cp = self.file.tell()
        next =  self.file.readline()
        self.file.seek(cp)
        
        if not next:
            self.file.close()
            return False
        
        return True

    def advance(self):
        self.current_instruction = self.file.readline()

    def command_type(self):
        s=self.current_instruction.split()[0]
        return self.command_table.get(s)

    def arg1(self):
        temp = self.current_instruction.split()
        if len(temp) > 1:
            return temp[1]
        return self.current_instruction.split()[0]

    def arg2(self):
        temp = self.current_instruction.split()
        if len(temp) > 2:
            return temp[2]
        return None

    def close(self):
        self.file.close()

#p = Parser('test.vm', 'config.json')
#while(p.has_more_lines()):
#    p.advance()
#    print(p.command_type())
#    print(p.arg1())
#    print(p.arg2())
#    print('----------------')
#    
#p.close()