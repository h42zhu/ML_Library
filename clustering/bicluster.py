import os, sys
lib_path = os.path.abspath(os.path.join('..', 'recommendation'))
sys.path.append(lib_path)

# class for hierachical clustering algorithm
# each cluster contains data about its location
# every iteration, the best pair of clusters is merged into a single cluster (measure = corr)
import random
import utilityfunc


class bicluster:
    def __init__(self, vec, left = None, right = None, distance = 0.0, id = None):
        self.left = left
        self.right = right
        self.vec = vec
        self.id = id
        self.distance = distance
        
# contract: 2D matrix, func, int, int -> 2D matrix
def kclusters(rows, distance = utilityfunc.pearson, k = 4, iterations = 100):
    # Determine the max and min in each row
    ranges = [(min([row[i] for row in rows]), max([row[i] for row in rows])) for i in range(len(rows[0]))]
    
    # create k randomly placed centroids
    clusters = [[random.random()*(ranges[i][1] - ranges[i][0]) + ranges[i][0]
                 for i in range(len(rows[0]))] for _ in range(k)]
    last_matches = None
    for t in range(iterations):
        best_matches = [[]] * k
        
        # find which centroid is the closest to each row
        for j in range(len(rows)):
            row = rows[j]
            best_match = 0
            for i in range(k):
                d = distance(clusters[i], row)
                if d < distance(clusters[best_match], row): bestmatch = i
            best_matches[best_match].append(j)
        
        # if the results are the same as last time, break
        if best_matches == last_matches: break
        last_matches = best_matches
    
        # move the centroids to the avg of their members
        for i in range(k):
            avgs = [0.0] * len(rows[0])
            if len(best_matches[i]) > 0:
                for rowid in best_matches[i]:
                    for m in range(len(rows[rowid])):
                        avgs[m] += rows[rowid][m]
                for j in range(len(avgs)):
                    avg[j] /= len(best_matches[i])
                clusters[i] = avgs
                
    return best_matches