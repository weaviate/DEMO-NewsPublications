#!/usr/bin/env python3
import newspaper, uuid, os, json, sys, nltk

NEWSPAPERS = {
    'ft': 'https://www.ft.com',
    'nyt': 'https://www.theguardian.com/international',
    'guardian': 'https://www.nytimes.com',
    'wsj': 'https://www.wsj.com',
    'cnn': 'https://edition.cnn.com/',
    'fn': 'https://www.foxnews.com/',
    'econ': 'https://www.economist.com/',
    'newyorker': 'https://www.newyorker.com/',
    'wired': 'https://www.wired.com/',
    'vogue': 'https://www.vogue.com/',
    'gi': 'https://www.gameinformer.com/'
}

def isInCache(uuid):
    if os.path.isfile('./cache/' + str(uuid) + '.json'):
        return True
    return False

def saveToCache(obj):
    f = open('./cache/' + obj['id'] + '.json', 'x')
    f.write(json.dumps(obj))
    f.close()
    if os.path.getsize('./cache/' + obj['id'] + '.json') < 2000:
        os.remove('./cache/' + obj['id'] + '.json')

def dateToIso(i):

    isoDate = None

    try:
        isoDate = article.publish_date.isoformat()
    except:
        return isoDate

# download nltk english 
nltk.download()

# which newspaper to load?
if sys.argv[1] not in NEWSPAPERS:
    print("ERROR, CHOOSE A NEWSPAPER")
    print(NEWSPAPERS)
    exit(1)

# build the actual newspaper
for articleRaw in newspaper.build(NEWSPAPERS[sys.argv[1]], memoize_articles=False).articles:

    articleUuid = uuid.uuid3(uuid.NAMESPACE_DNS, articleRaw.url)

    if isInCache(articleUuid) == False:
    
        try:

            article = newspaper.Article(articleRaw.url)
            article.download()
            article.parse()
            article.nlp()

            if (article.meta_lang == 'en' or article.meta_lang == None) and \
                article.title != '' and \
                article.title != None and \
                article.summary != '' and \
                article.summary != None:

                # create the cache obj
                cacheObject = {
                    'id': str(articleUuid),
                    'title': article.title,
                    'url': article.url,
                    'summary': article.summary,
                    'paragraphs': article.text.split("\n\n"),
                    'authors': article.authors,
                    'keywords': article.keywords,
                    'pubDate': dateToIso(article),
                    'publicationId': str(uuid.uuid3(uuid.NAMESPACE_DNS, sys.argv[1]))
                }

                # save to the cache
                saveToCache(cacheObject)

                print("downloaded: " + article.title)
        except Exception as e:
            print("something went wrong:", str(e))
    else:
        print('collected from cache')


