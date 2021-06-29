
class AliasTable:
    def __init__(self):
        self.table = {}
    def insert(self, name, discrim, alias):
        self.table[name] = (discrim, alias)
    def get(self, name, discrim):
        if self.table[name] and self.table[name][0] == discrim:
            return self.table[name][1].rstrip()
        else:
            raise KeyError

alias_table = AliasTable()
