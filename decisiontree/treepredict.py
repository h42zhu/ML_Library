
# divides a set on a specific column, should handle numeric or nominal values
def divideset(rows, column, value):
    pass

# 
def unique_counts(rows):
    results = {}
    for row in rows:
        lastcol = row[len(row)-1]
        if lastcol not in results:
            results[lastcol] = 0
        else:
            results[lastcol] += 1
    return results


# Returns the Entropy in a dataset
# contract: 2*2 array -> float
def entropy(rows):
    log2 = lambda x: math.log(x) / math.log(2)
    results = unique_counts(rows)
    
    entro = 0.0
    for r in results.keys():
        p = float(results[r]) / len(rows)
        entro = entro - p * log2(p)
    return entro

# Returns the Gini Impurity of a dataset
def gini_impurity(rows):
    total = len(rows)
    counts = unique_counts(rows)
    imp = 0
    for k1 in counts:
        p1 = float(counts[k1]) / total
        for k2 in counts:
            if k1 == k2: continue
            p2 = float(counts[k2]) / total
            imp = imp + k1*k2
    return imp


# class for representing a decision tree

class decisionnode:
    def __init__(self, col = -1, value = None, results = None, tb = None, fb = None):
        self.col = col
        self.value = value
        self.results = results
        # tb and fb are also decisionnodes, tb = next node if true, fb = next node if false
        self.tb = tb
        self.fb = fb