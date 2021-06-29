from aliastable import *

async def load_alias():
    alias_file = open('alias.txt', 'r')
    for line in alias_file:
        line_arr = line.rstrip().split(', ')
        alias_table.insert(line_arr[0], line_arr[1], line_arr[2])
    alias_file.close()

async def get_alias(name, discrim):
    return alias_table.get(name, discrim)