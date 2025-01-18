import json

class SymbolTable:

    def __init__(self, pre_defined_symbols=None):
        self.symbol_table = dict()
        
        # Initialize pre defined symbols from .json file
        if pre_defined_symbols != None:
            
            with open(pre_defined_symbols, "r") as file:
                data = json.load(file)

                for item in data:
                    self.symbol_table[item['symbol']] = item['value']

    def add_entry(self, symbol, address):
        self.symbol_table[symbol] = address

    def contains(self, symbol):
        if self.get_address(symbol) is None:
            return False
        return True

    def get_address(self, symbol):
        return self.symbol_table.get(symbol)

#s = SymbolTable("symbols.json")
#print(s.get_address('SCREEN'))
#print(s.contains('KBD'))
#print(s.contains('MOI'))
#s.add_entry('MOI', 16)
#print(s.contains('MOI'))
#print(s.get_address('MOI'))

