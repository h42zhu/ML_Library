import feedparser, csv
import re
import os, sys
import nmf
import numpy

lib_path = os.path.abspath(os.path.join('..', 'documentfiltering'))
sys.path.append(lib_path)

from docclass import getwords

feedlist = [
    'http://today.reuters.com/rss/topNews',
    'http://www.nytimes.com/services/xml/rss/nyt/HomePage.xml',
    'http://google.com/?output=rss'
]

def stripHTML(h):
    p = ''
    s = 0
    for c in h:
        if c=='<': s = 1
        elif c=='>':
            s = 0
            p = p + ' '
        elif s == 0: p = p + c
    return p

def get_article_words_count(feedlist):
    allwords = {}
    articlewords = []
    articletitles = set()
    ec = 0
    # loop over every feed
    
    for feed in feedlist:
        f = feedparser.parse(feed)
        for e in f.entries:
            # ignore identical articles
            if e.title in articletitles: continue
            
            # extract the words
            txt = e.title.encode('utf-8') + stripHTML(e.description.encode('utf-8'))
            words = getwords(txt)
            articlewords.append({})
            articletitles.add(e.title)
            
            # inc counts of all words in an article in allwords, articlewords
            for word in words:
                allwords.setdefault(word, 0)
                allwords[word] += 1
                articlewords[ec].setdefault(word, 0)
                articlewords[ec][word] += 1
            ec = ec + 1
            
    return allwords, articlewords, list(articletitles)

def make_matrix(allw, articlew):
    wordvec = []
    
    # only take those words that are common but not too common
    # print allw.items()
    for w, c in allw.items():
        if c > 2 and c < len(articlew) * 0.6:
            wordvec.append(w)
            
        # create the word matrix
    l1 = [[(word in f and f[word] or 0) for word in wordvec] for f in articlew]
    return l1, wordvec


def show_features(w, h, titles, wordvec, out = 'features.csv'):
    with open(out, 'wb') as csvfile:
        csvfile.truncate()
        spamwriter = csv.writer(csvfile, delimiter= ',') 
        
        row, col = numpy.shape(h)
        pattern_names = []
        top_patterns = [[] for _ in range(len(titles))]
        
        # loop over features
        for i in range(row):
            slist = []
            # create a list of words and their weights
            for j in range(col):
                slist.append((h[i, j], wordvec[j]))
            slist.sort(reverse = True)
            
            # print the first 5 elems
            if len(slist) > 5:
                n = [str(s[1]) for s in slist[0:5]]
            else:
                n = [str(s[1]) for s in slist]
            
            spamwriter.writerow(n)
            pattern_names.append(n)
            
            # create a list of articles for this feature
            flist = []
            for j in range(len(titles)):
                # add the artile with its weight
                flist.append((w[j, i], i, titles[j]))
                top_patterns[j].append((w[j, i], i, titles[j]))
                
            # sort reverse
            flist.sort(reverse = True)
            
            # show top 3 articles:
            for f in flist[0:3]:
                spamwriter.writerow(list(f))
                
    return top_patterns, pattern_names


def show_articles(titles, pattern_names, pattern_names, out = 'articles.csv'):
    pass



allw,artw,artt = get_article_words_count(feedlist)
wordmatrix, wordvec = make_matrix(allw, artw)
print wordmatrix, wordvec
v = numpy.matrix(wordmatrix)
weights, feat = nmf.factorize(v, pc = 20, iteration= 50)
print weights, feat

topp, pn = show_features(weights, feat, artt, wordvec)
