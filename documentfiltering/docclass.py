import re
import math
import statsfunc
import sqlite3

# contract: 
# purpose: from a text documents, get a set of alphabetic words, used as a simple feature detector
# 

def getwords(doc, maxlen = 25):
    splitter = re.compile('\\W*')
    # split the words by nonalpha characters
    words = [s.lower() for s in splitter.split(doc) if 3 < len(s) < maxlen ]
    
    # return the unique set
    return set(words)


# classifiers
class classifier:
    # fields: fc, cc, getfeatures, threshholds, connection to Sqlite DB
    def __init__(self, getfeatures, filename = None):
        # counts of feature category combinations
        self.fc = {}
        # counts of documents in each category
        self.cc = {}
        self.getfeatures = getfeatures
        self.connection = None
        self.cur = None
        
    # set up db connection
    def setupdb(self, dbfile):
        try:
            self.connection = sqlite3.connect(dbfile)
            
            self.cur = self.connection.cursor()    
            self.cur.execute('create table if not exists FeatureCatergory(feature, category, count)')
            self.cur.execute('create table if not exists CatergoryCounts(category, count)')
            # data = cur.fetchone()
            # print "SQLite version: %s" % data                
            
        except sqlite3.Error, e:
            print "Error %s:" % e.args[0]
            sys.exit(1)        
        
    # commit all the mem/dictionary data to db
    def recordtodb(self):
        if self.connection is None:
            return
        
        # insert and update the CatergoryCounts table
        for k in self.cc:
            if self.catcount(k) == 0:
                query = 'insert into CatergoryCounts values ("{0}", {1})'.format(k, self.cc[k])
                self.cur.execute(query)
            else:
                count = self.catcount(k) + self.cc[k]
                query = 'update CatergoryCounts set count = {0} where category = "{1}"'.format(count, k)
                self.cur.execute(query)
                
        # insert and update the FeatureCatergory table
        for k in self.fc:
            for k2 in self.fc[k]:
                if self.fcount(k, k2) == 0:
                    query = 'insert into FeatureCatergory values ("{0}", "{1}", {2})'.format(k, k2, self.fc[k][k2])
                    self.cur.execute(query)
                else:
                    count = self.fcount(k, k2) + self.fc[k][k2]
                    query = 'update FeatureCatergory set count = {0} where feature = "{1}" and category = "{2}"'.format(count, k, k2)
                    self.cur.execute(query)
                    
        # commit to db
        self.connection.commit()
        
        # reset the dictionaries
        for k in self.cc:
            self.cc[k] = 0
        for k in self.fc:
            for k2 in self.fc[k]:
                # print k, k2, self.fcount(k, k2)
                self.fc[k][k2] = 0
        
        
    # increase the count of a feature, cat pair
    def incf(self, f, cat):
        self.fc.setdefault(f, {})
        self.fc[f].setdefault(cat, 0)
        self.fc[f][cat] += 1
        
    # increase the count of a category
    def incc(self, cat):
        self.cc.setdefault(cat, 0)
        self.cc[cat] += 1
    
    # return the number of times a feature has appeared in a category
    def fcount(self, f, cat):
        if self.connection is None:
            if f in self.fc and cat in self.fc[f]:
                return float(self.fc[f][cat])
            return 0.0
        
        # return from db
        query = 'select count from FeatureCatergory where feature = "{0}" and category = "{1}"'.format(f, cat)
        result = self.cur.execute(query).fetchone()
        
        if result is None: 
            return 0
        return float(result[0])
    
    # return the number of items in a category
    def catcount(self, cat):
        if self.connection is None:
            if cat in self.cc:
                return float(self.cc[cat])
            return 0.0
        
        # return count from db
        query = 'select count from CatergoryCounts where category = "{0}"'.format(cat)
        # print query
        result = self.cur.execute(query).fetchone()
        if result is None: 
            return 0
        return float(result[0])
    
    # return the total number of items
    def totalcount(self):
        if self.connection is None:
            return sum(self.cc.values())
        
        result = self.cur.execute('select sum(count) from CatergoryCounts').fetchone()
        if result is None:
            return 0
        return result[0]
    
    # return the list of all categories
    def categories(self):
        if self.connection is None:
            return self.cc.keys()
        cat = self.cur.execute('select category from CatergoryCounts')
        return [d[0] for d in cat]    
    
    
    # return the probability that f is in categorty
    def fprob(self, f, cat):
        if self.catcount(cat) == 0:
            return 0
        # the total number of times this feature appeared in this cat / the total number of items in cat
        return self.fcount(f, cat) / self.catcount(cat)
    
    # return the weighted probability for features with little information
    def weightedprob(self, f, cat, probfunc, weight = 1.0, assumeprob = 0.5):
        # current probability
        basicprob = probfunc(f, cat)
        # count the number of times this feature appeared in all cat
        totals = sum([self.fcount(f, c) for c in self.categories()])
        
        # calculate the weighted avg
        return ((weight * assumeprob) + (totals * basicprob)) / (weight + totals)
    
    # important: train method
    # input: an item (a text doc) and a classification
    # uses getfeatures function to break the item into separate features
    # then calls incf to increase the counts for the input classification for every feature
    def train(self, item, cat):
        features = self.getfeatures(item)
        # inc the count for each feature wiht this category
        for f in features:
            self.incf(f, cat)
        
        # inc the count for this category
        self.incc(cat)
        
        
    # train from a sample of data
    def sampletrain(self, fname):
        with open(fname, 'r') as csvfile:
            for line in csvfile:
                row = str.split(line.strip(), ',')
                item, cat = row[0], row[1]
                self.train(item, cat)
                
        if self.connection is not None:
            self.recordtodb()

        
class naivebayes(classifier):
    def __init__(self, getfeatures):
        classifier.__init__(self, getfeatures)
        self.threshholds = {}
        
    # set method for threshhold
    def set_threshhold(self, cat, t):
        self.threshholds[cat] = t
        
    # get method for threshhold, return 1.0 if not found
    def get_threshhold(self, cat):
        if cat not in self.threshholds: return 1.0
        return self.threshholds[cat]

    def docprob(self, item, cat):
        features = self.getfeatures(item)
        
        # mult the probs of all features together
        p = 1
        for f in features: p *= self.weightedprob(f, cat, self.fprob)
        
        return p


    def prob(self, item, cat):
        catprob = self.catcount(cat) / self.totalcount()
        docprob = self.docprob(item, cat)
        return catprob * docprob

    # classify if a document is which cat
    def classify(self, item, default = None):
        probs = {}
        # find the cat with the highest prob
        max_prob = 0.0
        for cat in self.categories():
            probs[cat] = self.prob(item, cat)
            if probs[cat] > max_prob:
                max_prob = probs[cat]
                best = cat
        
        # make sure the prob exceeds threshhold * next best
        for cat in probs:
            if cat == best: continue
            if probs[cat] * self.get_threshhold(best) > probs[best]: return default
        
        return best

class fisherclassifier(classifier):
    def __init__(self, getfeatures):
        classifier.__init__(self, getfeatures)
        self.threshholds = {}
        
    # set method for threshhold
    def set_threshhold(self, cat, t):
        self.threshholds[cat] = t
        
    # get method for threshhold, return 1.0 if not found
    def get_threshhold(self, cat):
        if cat not in self.threshholds: return 0.0
        return self.threshholds[cat]
        
    def cprob(self, f, cat):
        # the frequency of this feature in this cat
        clf = self.fprob(f, cat)
        if clf < 0.00001: return 0.0
        
        # the frequency of this feature in all cat
        freqsum = sum([self.fprob(f, c) for c in self.categories()])

        # the prob is the freq in this cat / overall freq
        return clf / freqsum
    
    # mult (all probs over each feature in the doc) | ln | mult -2
    # to get result of the Fisher Method
    def fisherprob(self, item, cat):
        p = 1.0
        features = self.getfeatures(item)
        for f in features:
            p *= (self.weightedprob(f, cat, self.cprob))
            
        fscore = -2 * math.log(p)
        
        # use the inverse X Square CDF to get a probability
        return statsfunc.inverse_chi2(fscore, len(features) * 2)
    
    # classify based on fisherprob and the threshholds
    def classify(self, item, default = None):
        best = default
        m = 0.0
        for c in self.categories():
            p = self.fisherprob(item, c)
            # make sure it passes threshhold
            if p > self.get_threshhold(c) and p > m:
                best = c
                m = p
        return best

#cl = fisherclassifier(getwords)
#cl.setupdb('docclass_v1.db')
#cl.sampletrain('sampledata.csv')
#cl.recordtodb()
#print cl.classify('quick money')