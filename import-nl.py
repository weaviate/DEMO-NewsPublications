#!/usr/bin/env python3
import newspaper, uuid, os, json, sys, time, weaviate, time
from modules.Weaviate import Weaviate
from modules.Weaviate import getWeaviateUrlFromConfigFile

WEAVIATE = Weaviate(sys.argv[1])
CACHEDIR = sys.argv[2]
CLIENT = weaviate.Client(sys.argv[1])

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
# Import the publications without refs except for cities
## 
print('add publications')

WEAVIATE.runREST('/v1/things', {
    'class': 'Publication',
    'id': str(uuid.uuid3(uuid.NAMESPACE_DNS, 'dvhn')),
    'schema': {
        'name': 'Dagblad van het Noorden',
        'headquartersGeoLocation': {
            "latitude": 53.219065, 
            "longitude": 6.568008
        }
    }
}, 0, 'POST')

WEAVIATE.runREST('/v1/things', {
    'class': 'Publication',
    'id': str(uuid.uuid3(uuid.NAMESPACE_DNS, 'nos')),
    'schema': {
        'name': 'NOS',
        'headquartersGeoLocation': {
            "latitude": 52.237869,
            "longitude": 5.174011
        }
    }
}, 0, 'POST')

WEAVIATE.runREST('/v1/things', {
    'class': 'Publication',
    'id': str(uuid.uuid3(uuid.NAMESPACE_DNS, 'nu')),
    'schema': {
        'name': 'nu.nl',
        'headquartersGeoLocation': {
            "latitude": 52.3025,
            "longitude": 4.68889
        }
    }
}, 0, 'POST')

WEAVIATE.runREST('/v1/things', {
    'class': 'Publication',
    'id': str(uuid.uuid3(uuid.NAMESPACE_DNS, 'ad')),
    'schema': {
        'name': 'Algemeen Dagblad',
        'headquartersGeoLocation': {
            "latitude": 51.9218362,
            "longitude": 4.4753684
        }
    }
}, 0, 'POST')

WEAVIATE.runREST('/v1/things', {
    'class': 'Publication',
    'id': str(uuid.uuid3(uuid.NAMESPACE_DNS, 'nrc')),
    'schema': {
        'name': 'NRC',
        'headquartersGeoLocation': {
            "latitude": 52.37403,
            "longitude": 4.88969
        }
    }
}, 0, 'POST')

WEAVIATE.runREST('/v1/things', {
    'class': 'Publication',
    'id': str(uuid.uuid3(uuid.NAMESPACE_DNS, 'telegraaf')),
    'schema': {
        'name': 'De Telegraaf',
        'headquartersGeoLocation': {
            "latitude": 52.3924369,
            "longitude": 4.8326266
        }
    }
}, 0, 'POST')

WEAVIATE.runREST('/v1/things', {
    'class': 'Publication',
    'id': str(uuid.uuid3(uuid.NAMESPACE_DNS, 'fd')),
    'schema': {
        'name': 'Financieel Dagblad',
        'headquartersGeoLocation': {
            "latitude": 52.348873,
            "longitude": 4.916886
        }
    }
}, 0, 'POST')

WEAVIATE.runREST('/v1/things', {
    'class': 'Publication',
    'id': str(uuid.uuid3(uuid.NAMESPACE_DNS, 'volkskrant')),
    'schema': {
        'name': 'De Volkskrant',
        'headquartersGeoLocation': {
            "latitude": 52.0812344,
            "longitude": 4.3150774
        }
    }
}, 0, 'POST')

WEAVIATE.runREST('/v1/things', {
    'class': 'Publication',
    'id': str(uuid.uuid3(uuid.NAMESPACE_DNS, 'trouw')),
    'schema': {
        'name': 'De Trouw',
        'headquartersGeoLocation': {
            "latitude": 52.0812344, 
            "longitude": 4.3150774
        }
    }
}, 0, 'POST')

WEAVIATE.runREST('/v1/things', {
    'class': 'Publication',
    'id': str(uuid.uuid3(uuid.NAMESPACE_DNS, 'rtl')),
    'schema': {
        'name': 'RTL Nieuws',
        'headquartersGeoLocation': {
            "latitude": 52.22333, 
            "longitude": 5.17639
        }
    }
}, 0, 'POST')

WEAVIATE.runREST('/v1/things', {
    'class': 'Publication',
    'id': str(uuid.uuid3(uuid.NAMESPACE_DNS, 'elsevier')),
    'schema': {
        'name': 'Elsevier',
        'headquartersGeoLocation': {
            "latitude": 52.3933107,
            "longitude": 4.8371682
        }
    }
}, 0, 'POST')

WEAVIATE.runREST('/v1/things', {
    'class': 'Publication',
    'id': str(uuid.uuid3(uuid.NAMESPACE_DNS, 'parool')),
    'schema': {
        'name': 'Het Parool',
        'headquartersGeoLocation': {
            "latitude": 52.0812344, 
            "longitude": 4.3150774
        }
    }
}, 0, 'POST')

WEAVIATE.runREST('/v1/things', {
    'class': 'Publication',
    'id': str(uuid.uuid3(uuid.NAMESPACE_DNS, 'gelderlander')),
    'schema': {
        'name': 'De Gelderlander',
        'headquartersGeoLocation': {
            "latitude": 51.8474946,
            "longitude": 5.8637771}
    }
}, 0, 'POST')

WEAVIATE.runREST('/v1/things', {
    'class': 'Publication',
    'id': str(uuid.uuid3(uuid.NAMESPACE_DNS, 'tweakers')),
    'schema': {
        'name': 'Tweakers',
        'headquartersGeoLocation': {
            "latitude": 52.35481643676758,
            "longitude": 4.876302242279053}
    }
}, 0, 'POST')

WEAVIATE.runREST('/v1/things', {
    'class': 'Publication',
    'id': str(uuid.uuid3(uuid.NAMESPACE_DNS, 'metro')),
    'schema': {
        'name': 'Metro',
        'headquartersGeoLocation': {
            "latitude": 52.3924369,
            "longitude": 4.8326266}
    }
}, 0, 'POST')

##
# Add categories
##
# WEAVIATE.runREST('/v1/things', {
#     'class': 'Category',
#     'id': str(uuid.uuid3(uuid.NAMESPACE_DNS, 'Art')),
#     'schema': {
#         'name': 'Art'
#     }
# }, 0, 'POST')

# WEAVIATE.runREST('/v1/things', {
#     'class': 'Category',
#     'id': str(uuid.uuid3(uuid.NAMESPACE_DNS, 'Music')),
#     'schema': {
#         'name': 'Music'
#     }
# }, 0, 'POST')

# WEAVIATE.runREST('/v1/things', {
#     'class': 'Category',
#     'id': str(uuid.uuid3(uuid.NAMESPACE_DNS, 'Movies')),
#     'schema': {
#         'name': 'Movies'
#     }
# }, 0, 'POST')

# WEAVIATE.runREST('/v1/things', {
#     'class': 'Category',
#     'id': str(uuid.uuid3(uuid.NAMESPACE_DNS, 'Environmental')),
#     'schema': {
#         'name': 'Environmental'
#     }
# }, 0, 'POST')

# WEAVIATE.runREST('/v1/things', {
#     'class': 'Category',
#     'id': str(uuid.uuid3(uuid.NAMESPACE_DNS, 'Recreation')),
#     'schema': {
#         'name': 'Recreation'
#     }
# }, 0, 'POST')

# WEAVIATE.runREST('/v1/things', {
#     'class': 'Category',
#     'id': str(uuid.uuid3(uuid.NAMESPACE_DNS, 'Weather')),
#     'schema': {
#         'name': 'Weather'
#     }
# }, 0, 'POST')

# WEAVIATE.runREST('/v1/things', {
#     'class': 'Category',
#     'id': str(uuid.uuid3(uuid.NAMESPACE_DNS, 'Technology')),
#     'schema': {
#         'name': 'Technology'
#     }
# }, 0, 'POST')

# WEAVIATE.runREST('/v1/things', {
#     'class': 'Category',
#     'id': str(uuid.uuid3(uuid.NAMESPACE_DNS, 'Science')),
#     'schema': {
#         'name': 'Science'
#     }
# }, 0, 'POST')

# WEAVIATE.runREST('/v1/things', {
#     'class': 'Category',
#     'id': str(uuid.uuid3(uuid.NAMESPACE_DNS, 'Sports')),
#     'schema': {
#         'name': 'Sports'
#     }
# }, 0, 'POST')

# WEAVIATE.runREST('/v1/things', {
#     'class': 'Category',
#     'id': str(uuid.uuid3(uuid.NAMESPACE_DNS, 'Religion')),
#     'schema': {
#         'name': 'Religion'
#     }
# }, 0, 'POST')

# WEAVIATE.runREST('/v1/things', {
#     'class': 'Category',
#     'id': str(uuid.uuid3(uuid.NAMESPACE_DNS, 'Politics')),
#     'schema': {
#         'name': 'Politics'
#     }
# }, 0, 'POST')

# WEAVIATE.runREST('/v1/things', {
#     'class': 'Category',
#     'id': str(uuid.uuid3(uuid.NAMESPACE_DNS, 'Media')),
#     'schema': {
#         'name': 'Media'
#     }
# }, 0, 'POST')

# WEAVIATE.runREST('/v1/things', {
#     'class': 'Category',
#     'id': str(uuid.uuid3(uuid.NAMESPACE_DNS, 'Government')),
#     'schema': {
#         'name': 'Government'
#     }
# }, 0, 'POST')

# WEAVIATE.runREST('/v1/things', {
#     'class': 'Category',
#     'id': str(uuid.uuid3(uuid.NAMESPACE_DNS, 'Business')),
#     'schema': {
#         'name': 'Business'
#     }
# }, 0, 'POST')

# sleep for slower machines
time.sleep(4)

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

    # empty author object
    authorObj = {}

    if len(author.split(' ')) == 2:

        # author obj
        authorObj = {
            'name': author,
            'writesFor': [
                {
                    'beacon': 'weaviate://localhost/things/' + publication
                }
            ]
        }

        # add every 200
        if (i % 199) == 0:
            CLIENT.batch.create_things(batch)
            batch = weaviate.ThingsBatchRequest()

        batch.add_thing(authorObj, 'Author', str(uuid.uuid3(uuid.NAMESPACE_DNS, author)))
        
    i += 1

CLIENT.batch.create_things(batch)

# sleep for slower machines
time.sleep(4)

##
# Import the articles without refs
##
print('add articles')
i = 1
articles = {}
validator = []
batchThings = weaviate.ThingsBatchRequest()
batchRefs = weaviate.ReferenceBatchRequest()
for filename in os.listdir(CACHEDIR):
    if filename.endswith(".json"):
        with open(CACHEDIR + '/' + filename) as f:

            # add every 200
            if (i % 199) == 0:
                CLIENT.batch.create_things(batchThings)
                batchThings = weaviate.ThingsBatchRequest()
                CLIENT.batch.add_references(batchRefs)
                batchRefs = weaviate.ReferenceBatchRequest()

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

            articleId = str(uuid.uuid3(uuid.NAMESPACE_DNS, obj['title']))
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

            if articleId not in validator:

                validator.append(articleId)

                # set date

                if obj['pubDate'] != None and obj['pubDate'] != '':
                    articleObj['publicationDate'] = obj['pubDate']

                # add to weaviate
                batchThings.add_thing(articleObj, "Article", articleId)
                batchRefs.add_reference(obj['publicationId'], "Publication", "hasArticles", articleId)

                # update author to include this article
                for author in obj['authors']:
                    # check if relation should be through author or publication
                    if len(processInput('Author', author).split(' ')) == 2:
                        batchRefs.add_reference(str(uuid.uuid3(uuid.NAMESPACE_DNS, processInput('Author', author))), "Author", "wroteArticles", str(uuid.uuid3(uuid.NAMESPACE_DNS, obj['title'])))
        i += 1

# sleep for slower machines
time.sleep(4)

CLIENT.batch.create_things(batchThings)

# sleep for slower machines
time.sleep(4)

CLIENT.batch.add_references(batchRefs)
