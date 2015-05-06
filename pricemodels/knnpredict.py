import os, sys
lib_path = os.path.abspath(os.path.join('..', 'recommendation'))
sys.path.append(lib_path)
lib_path = os.path.abspath(os.path.join('..', 'genetic'))
sys.path.append(lib_path)

# class for hierachical clustering algorithm
# each cluster contains data about its location
# every iteration, the best pair of clusters is merged into a single cluster (measure = corr)
from pylab import *
import random
import utilityfunc
import csv
import math
import optimization

# get a list of distances between vec and every other vec in data
def get_distance_list(data, vec):
    distances = []
    for i in range(len(data)):
        vec2 = data[i]['input']
        # print vec2, vec
        distances.append((utilityfunc.euclidean(vec, vec2), i))
    distances.sort()
    return distances
        
        
# get estimate based on k nearest neighbors
# uses normal simple arithmatic averaging
def knn_estimate(data, vec, k = 4):
    dlist = get_distance_list(data, vec)
    avg = 0.0
    
    for i in range(k):
        # find index in dataset
        indx = dlist[i][1]
        avg = avg + data[indx]['result']
    return avg / k

# weight function: 1 / distance + eps
def inverseweight(dist, num = 1.0, eps = 0.1):
    return num / (dist + eps)

# weight function: substract the dist from a constant
def substractweight(dist, const = 1.0):
    if const - dist < 0: return 0
    return const - dist

# weight function: gaussian distribution
def gaussianweight(dist, sig = 10.0):
    return math.e**(-dist**2 / (2*sig**2))


# weighted KKN, using one of the weight functions

def weightedkkn(data, vec, k = 5, weightf = gaussianweight):
    dlist = get_distance_list(data, vec)
    # print dlist
    avg = 0.0
    totalweight = 0.0
    
    for i in range(k):
        # find index in dataset
        dist = dlist[i][0]
        # print dist
        indx = dlist[i][1]
        weight = weightf(dist)
        totalweight = totalweight + weight
        avg = avg + weight*float(data[indx]['result']) 
        
    return avg / totalweight


# cross validation
def dividedata(data, test = 0.05):
    trainset = []
    testset = []
    for row in data:
        if random.random() < test:
            testset.append(row)
        else:
            trainset.append(row)
            
    return trainset, testset

def errorscore(algf, trainset, testset):
    error = 0.0
    for row in testset:
        guess = algf(trainset, row['input'])
        error = error + (float(row['result']) - guess)**2
    return error/(len(testset)+1)

def crossvalidate(algf, data, trials = 100, test = 0.05):
    error = 0.0
    for _ in range(trials):
        trainset, testset = dividedata(data, test)
        error = error + errorscore(algf, trainset, testset)
    return error / trials


def datasetcsv(filename, header = True):
    data = []
    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile)
        if header: next(reader, None)
        for line in reader:
            # print line
            if len(line) > 1:
                data.append({'input': line[:len(line)-1], 'result': line[len(line) - 1]})
    return data


# rescale the dataset
def rescale(data, scale):
    scaleddata = []
    for row in data:
        # assert len(row['input']) == len(scale)
        scaled = [scale[i] * float(row['input'][i]) for i in range(len(scale))]
        scaleddata.append({'input': scaled, 'result': row['result']})
    return scaleddata

# create the cost function for optimizing which weights/scaling to give to input data fields
def createcostfunction(algf, data):
    def costf(scale):
        sdata = rescale(data, scale)
        return crossvalidate(algf, sdata, trials = 10)
    return costf



def probguess(data, vec1, low, high, k = 5, weighf = gaussianweight):
    dlist = get_distance_list(data, vec1)
    nweight, tweight = 0.0, 0.0
    
    for i in range(k):
        distance = dlist[i][0]
        index = dlist[i][1]
        weight = weighf(distance)
        v = data[index]['result']
        
        # check if point in range
        if low <= v <= high:
            nweight += weight
        tweight += weight
        
        if tweight == 0:
            return 0
        
    # the prob is the weights in range / total weights
    return nweight / tweight
    

def cumulativegraph(data, vec1, high,  k = 5, weightf = gaussianweight):
    t1 = arange(0.0, high, 0.1)
    cprob = array([probguess(data, vec1, 0, v, k, weightf) for v in t1])
    plot(t1, cprob)
    show()

# script for testing
weighteddomain = [(0, 100)]*3
data = datasetcsv('winesampledata.csv')
costf = createcostfunction(weightedkkn, data)
#print data
#print weightedkkn(data, (99.0, 5.0))
print crossvalidate(weightedkkn, data)
print optimization.annealing_optimize(weighteddomain, costf, step = 2)
# cumulativegraph(data, (1, 1, 1), 6)