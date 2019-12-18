#!/usr/bin/env python3
import newspaper, uuid, os, json, sys, time
from modules.Weaviate import Weaviate
from modules.Weaviate import getWeaviateUrlFromConfigFile

WEAVIATE = Weaviate(sys.argv[1])
CACHEDIR = sys.argv[2]

##
# Function to clean up data
##
def processInput(k, v):

    if k == 'Author':
        v = v.replace(' Wsj.Com', '')
        v = v.replace('.', ' ')
        return v
    elif k == 'Summary':
        v = v.replace('\n', ' ')
        return v

    return v

##
# Import the publications without refs
## 
print('add publications')

WEAVIATE.runREST('/v1/things', {
    'class': 'Publication',
    'id': str(uuid.uuid3(uuid.NAMESPACE_DNS, 'ft')),
    'schema': {
        'name': 'Financial Times'
    }
}, 0, 'POST')

WEAVIATE.runREST('/v1/things', {
    'class': 'Publication',
    'id': str(uuid.uuid3(uuid.NAMESPACE_DNS, 'nyt')),
    'schema': {
        'name': 'International New York Times'
    }
}, 0, 'POST')

WEAVIATE.runREST('/v1/things', {
    'class': 'Publication',
    'id': str(uuid.uuid3(uuid.NAMESPACE_DNS, 'guardian')),
    'schema': {
        'name': 'The Guardian International'
    }
}, 0, 'POST')

WEAVIATE.runREST('/v1/things', {
    'class': 'Publication',
    'id': str(uuid.uuid3(uuid.NAMESPACE_DNS, 'wsj')),
    'schema': {
        'name': 'Wallstreet Journal'
    }
}, 0, 'POST')

WEAVIATE.runREST('/v1/things', {
    'class': 'Publication',
    'id': str(uuid.uuid3(uuid.NAMESPACE_DNS, 'cnn')),
    'schema': {
        'name': 'CNN'
    }
}, 0, 'POST')

WEAVIATE.runREST('/v1/things', {
    'class': 'Publication',
    'id': str(uuid.uuid3(uuid.NAMESPACE_DNS, 'fn')),
    'schema': {
        'name': 'Fox News'
    }
}, 0, 'POST')

WEAVIATE.runREST('/v1/things', {
    'class': 'Publication',
    'id': str(uuid.uuid3(uuid.NAMESPACE_DNS, 'econ')),
    'schema': {
        'name': 'The Economist'
    }
}, 0, 'POST')

WEAVIATE.runREST('/v1/things', {
    'class': 'Publication',
    'id': str(uuid.uuid3(uuid.NAMESPACE_DNS, 'newyorker')),
    'schema': {
        'name': 'New Yorker'
    }
}, 0, 'POST')

WEAVIATE.runREST('/v1/things', {
    'class': 'Publication',
    'id': str(uuid.uuid3(uuid.NAMESPACE_DNS, 'wired')),
    'schema': {
        'name': 'Wired'
    }
}, 0, 'POST')

WEAVIATE.runREST('/v1/things', {
    'class': 'Publication',
    'id': str(uuid.uuid3(uuid.NAMESPACE_DNS, 'vogue')),
    'schema': {
        'name': 'Vogue'
    }
}, 0, 'POST')

WEAVIATE.runREST('/v1/things', {
    'class': 'Publication',
    'id': str(uuid.uuid3(uuid.NAMESPACE_DNS, 'gi')),
    'schema': {
        'name': 'Game Informer'
    }
}, 0, 'POST')

##
# Add categories
##
WEAVIATE.runREST('/v1/things', {
    'class': 'Category',
    'id': str(uuid.uuid3(uuid.NAMESPACE_DNS, 'Environmental')),
    'schema': {
        'name': 'Environmental'
    }
}, 0, 'POST')

WEAVIATE.runREST('/v1/things', {
    'class': 'Category',
    'id': str(uuid.uuid3(uuid.NAMESPACE_DNS, 'Recreation')),
    'schema': {
        'name': 'Recreation'
    }
}, 0, 'POST')

WEAVIATE.runREST('/v1/things', {
    'class': 'Category',
    'id': str(uuid.uuid3(uuid.NAMESPACE_DNS, 'Weather')),
    'schema': {
        'name': 'Weather'
    }
}, 0, 'POST')

WEAVIATE.runREST('/v1/things', {
    'class': 'Category',
    'id': str(uuid.uuid3(uuid.NAMESPACE_DNS, 'Technology')),
    'schema': {
        'name': 'Technology'
    }
}, 0, 'POST')

WEAVIATE.runREST('/v1/things', {
    'class': 'Category',
    'id': str(uuid.uuid3(uuid.NAMESPACE_DNS, 'Science')),
    'schema': {
        'name': 'Science'
    }
}, 0, 'POST')

WEAVIATE.runREST('/v1/things', {
    'class': 'Category',
    'id': str(uuid.uuid3(uuid.NAMESPACE_DNS, 'Sports')),
    'schema': {
        'name': 'Sports'
    }
}, 0, 'POST')

WEAVIATE.runREST('/v1/things', {
    'class': 'Category',
    'id': str(uuid.uuid3(uuid.NAMESPACE_DNS, 'Religion')),
    'schema': {
        'name': 'Religion'
    }
}, 0, 'POST')

WEAVIATE.runREST('/v1/things', {
    'class': 'Category',
    'id': str(uuid.uuid3(uuid.NAMESPACE_DNS, 'Politics')),
    'schema': {
        'name': 'Politics'
    }
}, 0, 'POST')

WEAVIATE.runREST('/v1/things', {
    'class': 'Category',
    'id': str(uuid.uuid3(uuid.NAMESPACE_DNS, 'Media')),
    'schema': {
        'name': 'Media'
    }
}, 0, 'POST')

WEAVIATE.runREST('/v1/things', {
    'class': 'Category',
    'id': str(uuid.uuid3(uuid.NAMESPACE_DNS, 'Government')),
    'schema': {
        'name': 'Government'
    }
}, 0, 'POST')

##
# Import the authors without refs
##
print('add authors')

authors = {}
for filename in os.listdir(CACHEDIR):
    if filename.endswith(".json"):
        with open(CACHEDIR + '/' + filename) as f:
            obj = json.load(f)
            for author in obj['authors']:
                authors[processInput('Author', author)] = obj['publicationId']

# add to weaviate
i = 1
for author, publication in authors.items():
    if len(author.split(' ')) == 2:
        WEAVIATE.runREST('/v1/things', {
            'class': 'Author',
            'id': str(uuid.uuid3(uuid.NAMESPACE_DNS, author)),
            'schema': {
                'name': author,
                'writesFor': [
                    {
                        'beacon': 'weaviate://localhost/things/' + publication
                    }
                ]
            }
        }, 0, 'POST')
    print(i, 'out of', len(authors), 'Authors')
    i += 1

##
# Import the articles without refs
##
print('add articles')
articles = {}
validator = []
for filename in os.listdir(CACHEDIR):
    if filename.endswith(".json"):
        with open(CACHEDIR + '/' + filename) as f:
            obj = json.load(f)
            authors = []
            for author in obj['authors']:
                # check if relation should be through author or publication
                if len(processInput('Author', author).split(' ')) == 2:
                    authors.append({
                        'beacon': 'weaviate://localhost/things/' + str(uuid.uuid3(uuid.NAMESPACE_DNS, processInput('Author', author)))
                    })
                else:
                    authors.append({
                        'beacon': 'weaviate://localhost/things/' + obj['publicationId']
                    })

            wordCount = 0
            for paragraph in obj['paragraphs']:
                wordCount += len(paragraph.split(' '))

            articleObj = {
                'class': 'Article',
                'id': str(uuid.uuid3(uuid.NAMESPACE_DNS, obj['title'])),
                'schema': {
                    'title': obj['title'],
                    'summary': processInput('Summary', obj['summary']),
                    'hasAuthors': authors,
                    'wordCount': wordCount,
                    'url': obj['url'],
                    'inPublication': [
                        {
                            'beacon': 'weaviate://localhost/things/' + obj['publicationId']
                        }
                    ]
                }
            }

            if articleObj['id'] not in validator:

                validator.append(articleObj['id'])

                # set date
                if obj['pubDate'] != None and obj['pubDate'] != '':
                    articleObj['publicationDate'] = obj['pubDate']

                # add to weaviate
                WEAVIATE.runREST('/v1/things', articleObj, 0, 'POST')

                # update publication to include this article
                WEAVIATE.runREST('/v1/things/'+obj['publicationId']+'/references/hasArticles', {
                    'beacon': 'weaviate://localhost/things/' + str(uuid.uuid3(uuid.NAMESPACE_DNS, obj['title']))
                }, 0, 'POST')

                # update author to include this article
                for author in obj['authors']:
                    # check if relation should be through author or publication
                    if len(processInput('Author', author).split(' ')) == 2:
                        WEAVIATE.runREST('/v1/things/'+str(uuid.uuid3(uuid.NAMESPACE_DNS, processInput('Author', author)))+'/references/wroteArticles', {
                            'beacon': 'weaviate://localhost/things/' + str(uuid.uuid3(uuid.NAMESPACE_DNS, obj['title']))
                        }, 0, 'POST')
                    
                print('Added: ' + obj['title'])
