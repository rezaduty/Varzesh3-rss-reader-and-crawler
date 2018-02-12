# -*- coding: utf-8 -*-
# things.py

# Let's get this party started!
import falcon
import feedparser
import jalali
import persian
import requests
from bs4 import BeautifulSoup
from newspaper import Article

result = ""


def get_top_img_and_description(url):
    article = Article(url)
    article.download()
    article.html
    article.parse()

    r = requests.get(url)
    r.encoding = "utf-8"

    data = r.text
    soup = BeautifulSoup(data, 'html.parser')

    div = soup.find('body')
    ps = div.find_all('p')
    a = ""
    for p in ps:
        a = a + p.text
        print (a)

    print (article.top_image)

# Falcon follows the REST architectural style, meaning (among
# other things) that you think in terms of resources and state
# transitions, which map to HTTP verbs.
# Function to fetch the rss feed and return the parsed RSS


def parseRSS(rss_url):
    return feedparser.parse(rss_url)

# Function grabs the rss feed headlines (titles) and returns them as a list


def getHeadlines(rss_url):
    headlines = []

    feed = parseRSS(rss_url)
    headlines.append("[")
    i = 0
    length_key = len(feed['items'])  # length of the list stored at `'key'` ...

    #print length_key

    for newsitem in feed['items']:
        #print newsitem
        i = i+1
        article = Article(newsitem['link'])
        article.download()
        article.html
        article.parse()
            
        if i == length_key:

            headlines.append('{"title": "'+newsitem['title']+'",')
            headlines.append('"description": "'+newsitem['description']+'",')
            headlines.append('"image": "'+article.top_image+'",')
            headlines.append('"link": "'+newsitem['link']+'"}')

        else:
            headlines.append('{"title": "'+newsitem['title']+'",')
            headlines.append('"description": "'+newsitem['description']+'",')
            headlines.append('"image": "'+article.top_image+'",')
            headlines.append('"link": "'+newsitem['link']+'"},')

    headlines.append("]")

    return headlines


# A list to hold all headlines
allheadlines = []

# List of RSS feeds that we will fetch and combine
newsurls = {
    'Sport':           'http://www.varzesh3.com/rss/all'
}

# Iterate over the feed urls
for key, url in newsurls.items():
    # Call getHeadlines() and combine the returned headlines with allheadlines
    allheadlines.extend(getHeadlines(url))


# Iterate over the allheadlines list and print each headline
for hl in allheadlines:
    result = result + hl + "\n"
    #print result


class ThingsResource(object):
    def on_get(self, req, resp):
        """Handles GET requests"""
        resp.status = falcon.HTTP_200  # This is the default status

        r = requests.post("https://api.myjson.com/bins", data=result)
        print(r.status_code, r.reason)
        resp.body = (result)


# falcon.API instances are callable WSGI apps
app = falcon.API()

# Resources are represented by long-lived class instances
things = ThingsResource()

# things will handle all requests to the '/things' URL path
app.add_route('/feed', things)
