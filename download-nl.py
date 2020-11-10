#!/usr/bin/env python3
import newspaper, uuid, os, json, sys, nltk

NEWSPAPERS = {
    'dvhn': 'https://www.dvhn.nl/',
    'nos': 'https://nos.nl/',
    'nu': 'https://nu.nl/',
    'ad': 'https://ad.nl/',
    'nrc': 'https://nrc.nl/',
    'telegraaf': 'https://www.telegraaf.nl/',
    'fd': 'https://fd.nl/',
    'volkskrant': 'https://volkskrant.nl/',
    'trouw': 'https://trouw.nl/',
    'rtl': 'https://www.rtlnieuws.nl/',
    'elsevier': 'https://www.ewmagazine.nl/',
    'parool': 'https://www.parool.nl/',
    'gelderlander': 'https://www.gelderlander.nl/',
    'tweakers': 'https://tweakers.net/nieuws/',
    'metro': 'https://www.metronieuws.nl/'
}

def isInCache(uuid):
    if os.path.isfile('./cache-nl/' + str(uuid) + '.json'):
        return True
    return False

def saveToCache(obj):
    f = open('./cache-nl/' + obj['id'] + '.json', 'x')
    f.write(json.dumps(obj))
    f.close()
    if os.path.getsize('./cache-nl/' + obj['id'] + '.json') < 2000:
        os.remove('./cache-nl/' + obj['id'] + '.json')

def dateToIso(i):

    isoDate = None

    try:
        isoDate = i.publish_date.isoformat()
    except:
        pass

    try:
        isoDate = i.pubdate.isoformat()
    except:
        pass
    
    return isoDate

# download nltk english 
# nltk.download()

# which newspaper to load?
if sys.argv[1] not in NEWSPAPERS:
    print("ERROR, CHOOSE A NEWSPAPER")
    print(NEWSPAPERS)
    exit(1)

# build the actual newspaper
for articleRaw in newspaper.build(NEWSPAPERS[sys.argv[1]], memoize_articles=False, language='nl').articles:

    articleUuid = uuid.uuid3(uuid.NAMESPACE_DNS, articleRaw.url)

    if isInCache(articleUuid) == False:
    
        try:

            article = newspaper.Article(articleRaw.url)
            article.download()
            article.parse()
            article.nlp()

            if (article.meta_lang == 'nl' or article.meta_lang == None) and \
                article.title != '' and \
                article.title != None and \
                article.summary != '' and \
                article.summary != None:

                if 'Puzzel' in article.title:
                    continue

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
