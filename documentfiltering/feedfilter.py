import feedparser
import re

# input: filename (of URLs of a blog feed)
# prints out the classification

def classify_feed(feed, classifier):
    f = feedparser.parse(feed)
    for entry in f['entries']:
        print 
        print '------'
        # print the contents
        print 'Title: ' + entry['title'].encode('utf-8')
        # print 'Publisher: ' + entry['publisher'].encode('utf-8')
        print
        print 'Summary: ' + entry['summary'].encode('utf-8')
        
        fulltext = '{0}{1}'.format(entry['title'].encode('utf-8', 'ignore'), entry['summary'].encode('utf-8', 'ignore'))
        
        print 'Guess: ' + str(classifier.classify(fulltext))
        
        # ask for the user to specify the correct cat
        cl = raw_input('Enter Category: ')
        classifier.train(fulltext, cl)
        classifier.recordtodb()
        
        
import docclass
cl = docclass.fisherclassifier(docclass.getwords)
cl.setupdb('python_feed.db')
classify_feed('http://rss.cbc.ca/lineup/topstories.xml', cl)