#!/usr/bin/env python3
import newspaper, uuid, os, json, sys, time, weaviate
from modules.Weaviate import Weaviate
from modules.Weaviate import getWeaviateUrlFromConfigFile

WEAVIATE = Weaviate(sys.argv[1])
CACHEDIR = sys.argv[2]
CLIENT = weaviate.Client(WEAVIATE)

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
batch = weaviate.ThingsBatchRequest()
for author, publication in authors.items():
    if len(author.split(' ')) == 2:
        batch.add_thing({
                'name': author,
                'writesFor': [
                    {
                        'beacon': 'weaviate://localhost/things/' + publication
                    }
                ]
            }, 'Author', str(uuid.uuid3(uuid.NAMESPACE_DNS, author)))
    print(i, 'out of', len(authors), 'Authors')
    i += 1
CLIENT.create_things_in_batch(batch)

##
# Import the articles without refs
##
print('add articles')
articles = {}
validator = []
batchThings = weaviate.ThingsBatchRequest()
batchRefs = weaviate.ReferenceBatchRequest()
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

            if articleObj['id'] not in validator:

                validator.append(articleObj['id'])

                # set date
                if obj['pubDate'] != None and obj['pubDate'] != '':
                    articleObj['publicationDate'] = obj['pubDate']

                # add to weaviate
                batchThings.add_thing(articleObj, "Article", str(uuid.uuid3(uuid.NAMESPACE_DNS, obj['title'])))
                batchRefs.add_reference("Publication", obj['publicationId'], "hasArticles", str(uuid.uuid3(uuid.NAMESPACE_DNS, obj['title'])))

                # update author to include this article
                for author in obj['authors']:
                    # check if relation should be through author or publication
                    if len(processInput('Author', author).split(' ')) == 2:
                        batchRefs.add_reference("Author", str(uuid.uuid3(uuid.NAMESPACE_DNS, processInput('Author', author))), "wroteArticles", str(uuid.uuid3(uuid.NAMESPACE_DNS, obj['title'])))
                    
                print('Added: ' + obj['title'])

CLIENT.create_things_in_batch(batchThings)
CLIENT.add_references_in_batch(batchRefs)