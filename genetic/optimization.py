# import time
import random
import math


def annealing_optimize(domain, costf, T = 100000.0, cool = 0.95, step = 1):
    # initialize values randomly
    vec = [float(random.randint(domain[i][0], domain[i][1])) for i in range(len(domain))]
    
    while T > 0.1:
        # choose one of the indices
        i = random.randint(0, len(domain) - 1)
        
        # choose a direction to change it
        direc = random.randint(-step, step)
        vec_new = vec[:]
        vec_new[i] += direc
        
        # boundaries
        if vec_new[i] < domain[i][0]: vec_new[i] = domain[i][0]
        elif vec_new > domain[i][1]: vec_new[i] = domain[i][1]
        
        # current cost and new cost
        ea = costf(vec)
        eb = costf(vec_new)
        
        p = math.e ** ((ea - eb) / T)
        
        # check if the new iteration is better or if it makes the probability cutoff
        if (eb < ea or random.random < p):
            vec = vec_new
            
        # decrease the temp / freedom
        T = T * cool
        
    return vec



def genetic_optimize(domain, costf, popsize = 50, step = 1, mut_prod = 0.2, elite = 0.2, max_iter = 100):
    # mutation
    """
    :param domain:
    :param costf:
    :param popsize:
    :param step:
    :param mut_prod:
    :param elite:
    :param max_iter:
    :return:
    """

    def mutate(vec):
        vec2 = vec
        i = random.randint(0, len(domain) - 1)
        if random.random() < 0.5 and vec[i] > domain[i][0]:
            vec2[i] = vec2[i] - step
            return vec2
        elif vec[i] < domain[i][1]:
            vec2[i] = vec2[i] + step
            return vec2
        
    # crossover
    def crossover(r1, r2):
        i = random.randint(0, len(domain) - 2)
        return r1[0:i] + r2[i:]
    
    # build the initial pop
    pop = []
    for _ in range(popsize):
        vec = [random.randint(domain[i][0], domain[i][1]) for i in range(len(domain))]
        pop.append(vec)
        
    # winner size
    topelite = int(elite*popsize)
    
    # main loop
    for i in range(max_iter):
        scores = [(costf(v), v) for v in pop]
        scores.sort()
        ranked = [v for(s, v) in scores]
        
        # start with the winners
        pop_winner = ranked[0:topelite]
        
        # add mutated form of winners
        while len(pop_winner) < popsize:
            if random.random() < mut_prod:
                # mutation
                c = random.randint(0, topelite)
                pop_winner.append(mutate(ranked[c]))
            else:
                # crossover
                c1, c2 = random.randint(0, topelite), random.randint(0, topelite)
                pop_winner.append(crossover(ranked[c1], ranked[c2]))
        
            # print scores[0][1]
        return scores[0][1]


