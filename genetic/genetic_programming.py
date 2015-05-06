from random import random, randint, choice
from copy import deepcopy
from math import log

class fwrapper:
    def __init__(self, function, childcount, name):
        self.function = function
        self.childcount = childcount
        self.name = name
        
class node:
    def __init__(self, fw, children):
        self.function = fw.function
        self.name = fw.name
        self.children = children
        
    def evaluate(self, inp):
        results = [n.evaluate(inp) for n in self.children]
        return self.function(results)
    
    def display(self, indent = 0):
        print (" "*indent) + self.name
        for c in self.children:
            c.display(indent + 1)
    
class paramnode:
    def __init__(self, idx):
        self.idx = idx
        
    def evaluate(self, inp):
        return inp[self.idx]
    
    def display(self, indent = 0):
        print "{0}{1}".format(" "*indent, self.idx)
    
class constnode:
    def __init__(self, v):
        self.v = v
        
    def evaluate(self, inp):
        return self.v
    
    def display(self, indent = 0):
        print "{0}{1}".format(" "*indent, self.v)
    
    

    
    
# creating some math functions
def iffunc(l):
    if l[0] > 0: return l[1]
    else: return l[2]
    
def isgreater(l):
    if l[0] > l[1]: return 1
    else: return 0
    


# random tree
def make_random_tree(pc, flist, maxdepth = 4, fpr = 0.5, ppr = 0.6):
    if random() < fpr and maxdepth > 0:
        f = choice(flist)
        children = [make_random_tree(pc, flist, maxdepth - 1, fpr, ppr) for i in range(f.childcount)]
        return node(f, children)
    elif random() < ppr:
        return paramnode(randint(0, pc -1))
    else:
        return constnode(randint(0, 10))


def example_tree():
    return node(ifw, [
    node(gtw, [paramnode(0), constnode(3)]),
    node(addw, [paramnode(1), constnode(5)]),
    node(subw, [paramnode(1), constnode(2)])])

#ext = example_tree()
#print ext.evaluate([2,3])
#print ext.evaluate([5,3])
#ext.display()


def hiddenfunction(x, y):
    return x**2 + 2*y + 3*x + 5

def buildhiddenset(func, size = 100):
    rows = []
    for i in range(size):
        x = randint(0, 50)
        y = randint(0, 50)
        rows.append([x, y, func(x, y)])
    return rows

def scorefunction(tree, s):
    dif = 0
    for data in s:
        v = tree.evaluate([data[0], data[1]])
        dif = dif + abs(v-data[2])
    return dif 



# mutation of the tree
def mutate(t, pc, flist, prob = 0.1):
    if random() < prob:
        return make_random_tree(pc, flist)
    else:
        result = deepcopy(t)
        if isinstance(t, node):
            result.children = [mutate(c, pc, flist) for c in t.children]
        return result
    
# building the environment for evolution
def evolve(pc, popsize, flist, rankfunction, max_gen = 500, mutation_rate = 0.1, pexp = 0.7, pnew = 0.05):
    # return a random number, tending towards lower numbers
    def selectindex():
        return int(log(random())/log(pexp))
    
    # create a random initial population
    population = [make_random_tree(pc, flist) for _ in range(popsize)]
    
    for i in range(max_gen):
        scores = rankfunction(population)
        if scores[0][0] == 0: 
            break
        
        # select the top 2
        newpop = [scores[0][1], scores[1][1]]
        
        # build the next generation
        while len(newpop) < popsize:
            if random() > pnew:
                # mutate(t, pc, flist, prob = 0.5)
                newpop.append(mutate(scores[selectindex()][1], pc, flist, prob = mutation_rate))
                
            else:
                # add a random new node to the population
                newpop.append(make_random_tree(pc, flist))
            
        population = newpop
        
    scores[0][1].display
    return scores[0][1]

# return a rank function with a given dataset and score_function
def get_rank_function(dataset, scorefunc):
    def rankfunction(population):
        scores = [(scorefunc(t, dataset), t) for t in population]
        scores.sort()
        return scores
    return rankfunction
    
addw = fwrapper(lambda l: l[0] + l[1], 2, 'add')
subw = fwrapper(lambda l: l[0] - l[1], 2, 'subtract')
mulw = fwrapper(lambda l: l[0] * l[1], 2, 'multiply')

ifw = fwrapper(iffunc, 3, 'if')
gtw = fwrapper(isgreater, 2, 'isgreater')
flist = [addw, subw, mulw, ifw, gtw]

hset = buildhiddenset(hiddenfunction, 10)


# randtree1 = make_random_tree(3, flist)
# randtree1.display()
# print randtree1.evaluate([])
#print scorefunction(randtree1, hset)
#randtree2 = mutate(randtree1, 3, flist)
#randtree2.display()
#print scorefunction(randtree2, hset)

# script for testing the genetic programming
rf = get_rank_function(hset, scorefunction)

# evolve(pc, popsize, flist, rankfunction, max_gen = 500, mutation_rate = 0.1, pexp = 0.7, pnew = 0.05)
# sol = evolve(2, 500, flist, rf)