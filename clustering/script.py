import generatefeedvector

urls = ['http://rss.cbc.ca/lineup/topstories.xml',
       'http://rss.cbc.ca/lineup/world.xml'
       ]

wordcount = {}
apcount = {}
for url in urls:
    title, wc = generatefeedvector.get_word_counts(url)
    wordcount[title] = wc
    for word, count in wc.items():
        apcount.setdefault(word, 0)
        if count > 1:
            apcount[word] += 1
        
generatefeedvector.feed_write_to_file("blogdata.csv", wordcount, apcount, "Test")
