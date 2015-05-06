# Building Datasets with pydelicious
import pydelicious
import time

# contract: str, int -> dict of (str : dict)
def initUserDict(tag, count = 5):
    user_dict = {}
    # get the top count popular posts
    for p1 in pydelicious.get_popular(tag=tag)[0:count]:
        # find all users who posted this
        # print pydelicious.get_urlposts(p1['url'])
        for p2 in pydelicious.get_urlposts(p1['url']):
            user = p2['user']
            user_dict[user] = {}
    return user_dict

def fillItems(user_dict):
    all_items = {}
    posts = []
    # find links posted by all users
    for user in user_dict:
        for i in range(3):
            try:
                posts = pydelicious.get_userposts(user)
                break
            except:
                print "Failed user: " + user
                time.sleep(4)
        for post in posts:
            url = post['url']
            user_dict[user][url] = 1.0
            all_items[url] = 1
            
    # fill the missing items with 0
    for ratings in user_dict.values():
        for item in all_items:
            if item not in ratings:
                ratings[item] = 0.0
    return user_dict
    