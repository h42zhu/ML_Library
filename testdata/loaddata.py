# load data in dictionary from csv

data = {}

# contract: str, listof int
def load_data(filename, key_index):
    with open(filename, 'r') as csvfile:
        for line in csvfile:
            row = str.split(line.strip(), ',')
            keys = tuple(row[0:key_index])
            data.setdefault(keys, [])
            data[keys].append(tuple(row[key_index:]))
                        
            
load_data('schedule.csv', 2)
# print data