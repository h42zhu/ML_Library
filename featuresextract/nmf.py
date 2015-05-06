from numpy import *
import random



# contract: two matrices of same size -> float

def square_diff(a, b):
    c = a - b
    c = multiply(c, c)
    return sum(c)

def factorize(v, pc = 10, iteration = 50):
    row = shape(v)[0]
    col = shape(v)[1]
    
    # initialize the weight and feature matrix with random variables
    w = matrix([[random.random() for j in range(pc)] for i in range(row)])
    h = matrix([[random.random() for j in range(col)] for i in range(pc)])
    
    # iterate 
    for i in range(iteration):
        wh = w*h
        
        # calc the current square diff
        cost = square_diff(v, wh)
        
        # terminate if fully factorized:
        if cost == 0: break
        
        # update the feature matrix
        hn = (transpose(w)*v)
        hd = (transpose(w)*w*h)
        
        h = matrix(array(h) * array(hn) / array(hd))
        
        # update weight matrix
        wn = v * transpose(h)
        wd = w * h * transpose(h)
        
        w = matrix(array(w) * array(wn) / array(wd))
        
    return w, h
    
a = matrix([[1,2,3], [4,5,6]]) 
b = matrix([[1, 2], [3, 4], [5, 6]]) 
#print a - b
#print square_diff(a, b)
#w, h = factorize(a*b, 4, 100)
#print w*h

