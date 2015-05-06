
# Returns a transposed dictionary
# Contract: dict of dict -> dict of dict

def transform_dictionary(d):
    result = {}
    for p in d:
        for i in d[p]:
            result.setdefault(i, {})
            result[i][p] = d[p][i] 
    
    return result
    
# print transform_dictionary({'a': {1: 1, 2: 1}, 'b': {2: 1}})


# Mathematical Functions
from math import sqrt
import numpy

# Returns the pearson corr of two vectors
# Contract: list, list -> float

def pearson(x, y):
    assert len(x) == len(y)
    n = len(x)
    assert n > 0
    avg_x =  float(sum(x)) / len(x)
    avg_y =  float(sum(y)) / len(y)
    diffprod = 0
    xdiff2 = 0
    ydiff2 = 0
    for idx in range(n):
        xdiff = x[idx] - avg_x
        ydiff = y[idx] - avg_y
        diffprod += xdiff * ydiff
        xdiff2 += xdiff * xdiff
        ydiff2 += ydiff * ydiff

    return diffprod / sqrt(xdiff2 * ydiff2)

# Returns the Tanimoto score of two vectors
# Contract: list, list -> float

def tanamoto(v1, v2):
    c1, c2, shr = 0, 0 ,0
    assert len(x) == len(y)
    for i in range(len(v1)):
        if v1[i] != 0: c1 = c1 + 1
        if v2[i] != 0: c2 = c2 + 1
        if v1[i] != 0 and v2[i] != 0: shr = shr + 1
        
    return 1.0 - (float(shr)/(c1 + c2 - shr))


# Returns Euclidean Distance
def euclidean(v1, v2):
    a1, a2 = numpy.array(v1).astype('float64'), numpy.array(v2).astype('float64')
    # print a1.dtype, a2.dtype
    # print a1, a2
    return numpy.linalg.norm(a1-a2)

