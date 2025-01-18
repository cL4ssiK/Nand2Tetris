import json

class Code:

    def __init__(self, tables):
        self.binary_table = [dict(), dict(), dict()]
        
        # Initialize pre defined instructions from .json file
        if tables != None:
            
            with open(tables, "r") as file:
                data = json.load(file)
                
                for table, tab in zip(data, self.binary_table):
                    for item in data[table]:
                        tab[item['instruction']] = item['binary']


    def dest(self, ddd):
        return self.binary_table[0].get(ddd)

    def comp(self, acccccc):
        return self.binary_table[1].get(acccccc)

    def jump(self, jjj):
        return self.binary_table[2].get(jjj)


#c = Code('instructions.json')
#print(c.dest('A'))
#print(c.comp('D|A'))
#print(c.jump('JEQ'))