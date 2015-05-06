import feedparser
import re
import csv

def get_words(html):
    # remove all html tags
    txt = re.compile(r'<[^>]+>').sub('', html)
    
    # split the words by all non-alpha char
    words = re.compile(r'[^A-Z^a-z]+').split(txt)
    
    return [word.lower() for word in words if word != '']


# returns title and dict of word counts for an RSS feed
def get_word_counts(url):
    # parse the feed
    d = feedparser.parse(url)
    wc = {}
    
    # loop through entries
    for e in d.entries:
        if 'summary' in e: summary = e.summary
        else: summary = e.description
        
        # extract a list of words
        words = get_words(e.title + ' ' + summary)
        for word in words:
            wc.setdefault(word, 0)
            wc[word] += 1
    return d.feed.title, wc


def feed_write_to_file(filename, wordcounts, apcounts, title = "Title", fileformat = 'csv'):
     
    with open(filename, 'wb') as outfile:
        outfile.truncate()
        if fileformat == 'csv':
            spamwriter = csv.writer(outfile, delimiter= ',')
            line = [w for w, bc in apcounts.items()]
            spamwriter.writerow(line)
            for blog, wc in wordcounts.items():
                line = [blog] +[wc[w] if w in wc else 0 for w, bc in apcounts.items()]
                spamwriter.writerow(line)
        else:
            outfile.write(title)
            outfile.write('\n')
            for w, bc in apcounts.items():
                outfile.write('\t%s' % w)
            outfile.write('\n')
            for blog, wc in wordcounts.items():
                outfile.write(blog)
                for w, bc in apcounts.items():
                    if w in wc:
                        outfile.write('\t%d' % wc[w])
                    else:
                        outfile.write('\t0')            
                outfile.write('\n')