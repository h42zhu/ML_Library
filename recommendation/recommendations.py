import math
import utilityfunc
# Euclidean Distance & Correlation for Similarity Scores

# Returns a distance based similarity scores for person1 and person2
# Contract: (dict of str: (dict of (str: float))) , str, str, str -> float
def similarity_score(prefs, person1, person2, method = "Euclidean"):
    si = {item: 1 for item in prefs[person1] if item in prefs[person2]}
    
    n = len(si)
    
    if n == 0: return 0
            
    if method == "Euclidean":

        # Euclidean distance formulate
        sum_squares = sum([math.pow(prefs[person1][item] - prefs[person2][item], 2)
                           for item in prefs[person1] if item in prefs[person2]])
        
        return float(1)/(1 + sum_squares)
    
    else:
        # Peason correlation coefficient for p1 and p2
        # Add up prefs
        sum1 = sum([prefs[person1][it] for it in si])
        sum2 = sum([prefs[person2][it] for it in si])
        
        # Sum up the squares
        sum1SQ = sum([math.pow(prefs[person1][it], 2) for it in si])
        sum2SQ = sum([math.pow(prefs[person2][it], 2) for it in si])
        
        # Sum up the prod
        pSum = sum([prefs[person1][it]*prefs[person2][it] for it in si])
        
        num = pSum - (sum1 * sum2 / float(n))
        den = math.sqrt((sum1SQ - sum1**2)/n * (sum2SQ - sum2**2)/n)
        
        return num / den
    
    
    

    
# Returns the best matches for person from the prefs
# Contract: dict, str, int, func -> listof (float, str)

def top_matches(prefs, person, n = 5, similarity = similarity_score, method = "Euclidean"):
    scores = [(similarity(prefs, person, other, method), other) for other in prefs if other != person]
    scores.sort(reverse=True)
    if len(scores) <= n:
        n = len(scores) - 1
    
    return scores[0:n]


# Returns the similarity weighted average of rankings
# Contract: dict, str, func -> listof (float, str)
def get_recommendatios(prefs, person, similarity = similarity_score, method = "Euclidean"):
    totals = {}
    sim_sums = {}
    
    for other in prefs:
        if other == person: continue
        sim = similarity(prefs, person, other, method)
        
        # ignore scores of 0 or lower
        if sim <= 0: continue
        for item in prefs[other]:
            # check for movie the person hasn't seen yet
            if item not in prefs[person] or prefs[person][item] == 0:
                totals.setdefault(item, 0)
                totals[item] = totals[item] + prefs[other][item]*sim
                
                sim_sums.setdefault(item, 0)
                sim_sums[item] = sim_sums[item] + sim
                
    # create normalized list
    rankings = [(total/sim_sums[item], item) for item, total in totals.items()]
    
    rankings.sort(reverse=True)
    return rankings

# Item comparison dataset
def calculate_similar_items(prefs, n=10):
    # create a dict of items (showing which other items they are most similar to
    result = {}
    
    # invert the prefs matrix
    item_prefs = utilityfunc.transform_dictionary(prefs)
    
    for item in item_prefs:
        # find the most similar item
        scores = top_matches(item_prefs, item, n=n)
        result[item] = scores
    return result