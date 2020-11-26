import uuid, json

publications = [
    {
        'class': 'Publication',
        'id': str(uuid.uuid3(uuid.NAMESPACE_DNS, 'ft')),
        'schema': {
            'name': 'Financial Times',
            'headquartersGeoLocation': {
                "latitude": 51.5127391, 
                "longitude": -0.0962234
            }
        }
    },
    {
        'class': 'Publication',
        'id': str(uuid.uuid3(uuid.NAMESPACE_DNS, 'nyt')),
        'schema': {
            'name': 'International New York Times',
            'headquartersGeoLocation': {
                "latitude": 51.5127391,
                "longitude": -0.0962234
            }
        }
    },
    {
        'class': 'Publication',
        'id': str(uuid.uuid3(uuid.NAMESPACE_DNS, 'nyt-small')),
        'schema': {
            'name': 'New York Times',
            'headquartersGeoLocation': {
                "latitude": 48.8929012,
                "longitude": 2.2480131
            }
        }
    },
    {
        'class': 'Publication',
        'id': str(uuid.uuid3(uuid.NAMESPACE_DNS, 'nyt-company')),
        'schema': {
            'name': 'The New York Times Company',
            'headquartersGeoLocation': {
                "latitude": 48.8929012,
                "longitude": 2.2480131
            }
        }
    },
    {
        'class': 'Publication',
        'id': str(uuid.uuid3(uuid.NAMESPACE_DNS, 'guardian')),
        'schema': {
            'name': 'The Guardian',
            'headquartersGeoLocation': {
                "latitude": 51.5349539,
                "longitude": -0.1216748
            }
        }
    },
    {
        'class': 'Publication',
        'id': str(uuid.uuid3(uuid.NAMESPACE_DNS, 'wsj')),
        'schema': {
            'name': 'Wall Street Journal',
            'headquartersGeoLocation': {
                "latitude": 40.7574323,
                "longitude": -73.9827028
            }
        }
    },
    {
        'class': 'Publication',
        'id': str(uuid.uuid3(uuid.NAMESPACE_DNS, 'cnn')),
        'schema': {
            'name': 'CNN',
            'headquartersGeoLocation': {
                "latitude": 33.757934,
                "longitude": 84.394811
            }
        }
    },
    {
        'class': 'Publication',
        'id': str(uuid.uuid3(uuid.NAMESPACE_DNS, 'fn')),
        'schema': {
            'name': 'Fox News',
            'headquartersGeoLocation': {
                "latitude": 40.758678,
                "longitude": -73.9824059
            }
        }
    },
    {
        'class': 'Publication',
        'id': str(uuid.uuid3(uuid.NAMESPACE_DNS, 'econ')),
        'schema': {
            'name': 'The Economist',
            'headquartersGeoLocation': {
                "latitude": 51.5046127, 
                "longitude": -0.0236484
            }
        }
    },
    {
        'class': 'Publication',
        'id': str(uuid.uuid3(uuid.NAMESPACE_DNS, 'newyorker')),
        'schema': {
            'name': 'New Yorker',
            'headquartersGeoLocation': {
                "latitude": 40.7127431, 
                "longitude": -74.0133795
            }
        }
    },
    {
        'class': 'Publication',
        'id': str(uuid.uuid3(uuid.NAMESPACE_DNS, 'wired')),
        'schema': {
            'name': 'Wired',
            'headquartersGeoLocation': {
                "latitude": 37.7808297,
                "longitude": -122.3958169
            }
        }
    },
    {
        'class': 'Publication',
        'id': str(uuid.uuid3(uuid.NAMESPACE_DNS, 'vogue')),
        'schema': {
            'name': 'Vogue',
            'headquartersGeoLocation': {
                "latitude": 40.751537, 
                "longitude": -73.986259
            }
        }
    },
    {
        'class': 'Publication',
        'id': str(uuid.uuid3(uuid.NAMESPACE_DNS, 'gi')),
        'schema': {
            'name': 'Game Informer',
            'headquartersGeoLocation': {
                "latitude": 44.9901912,
                "longitude": -93.2753822}
        }
    }
]

categories = [
    {
        'class': 'Category',
        'id': str(uuid.uuid3(uuid.NAMESPACE_DNS, 'Art')),
        'schema': {
            'name': 'Art'
        }
    }
    ,{
        'class': 'Category',
        'id': str(uuid.uuid3(uuid.NAMESPACE_DNS, 'Music')),
        'schema': {
            'name': 'Music'
        }
    }
    ,{
        'class': 'Category',
        'id': str(uuid.uuid3(uuid.NAMESPACE_DNS, 'Movies')),
        'schema': {
            'name': 'Movies'
        }
    }
    ,{
        'class': 'Category',
        'id': str(uuid.uuid3(uuid.NAMESPACE_DNS, 'Environmental')),
        'schema': {
            'name': 'Environmental'
        }
    }
    ,{
        'class': 'Category',
        'id': str(uuid.uuid3(uuid.NAMESPACE_DNS, 'Recreation')),
        'schema': {
            'name': 'Recreation'
        }
    }
    ,{
        'class': 'Category',
        'id': str(uuid.uuid3(uuid.NAMESPACE_DNS, 'Weather')),
        'schema': {
            'name': 'Weather'
        }
    }
    ,{
        'class': 'Category',
        'id': str(uuid.uuid3(uuid.NAMESPACE_DNS, 'Technology')),
        'schema': {
            'name': 'Technology'
        }
    }
    ,{
        'class': 'Category',
        'id': str(uuid.uuid3(uuid.NAMESPACE_DNS, 'Science')),
        'schema': {
            'name': 'Science'
        }
    }
    ,{
        'class': 'Category',
        'id': str(uuid.uuid3(uuid.NAMESPACE_DNS, 'Sports')),
        'schema': {
            'name': 'Sports'
        }
    }
    ,{
        'class': 'Category',
        'id': str(uuid.uuid3(uuid.NAMESPACE_DNS, 'Religion')),
        'schema': {
            'name': 'Religion'
        }
    }
    ,{
        'class': 'Category',
        'id': str(uuid.uuid3(uuid.NAMESPACE_DNS, 'Politics')),
        'schema': {
            'name': 'Politics'
        }
    }
    ,{
        'class': 'Category',
        'id': str(uuid.uuid3(uuid.NAMESPACE_DNS, 'Media')),
        'schema': {
            'name': 'Media'
        }
    }
    ,{
        'class': 'Category',
        'id': str(uuid.uuid3(uuid.NAMESPACE_DNS, 'Government')),
        'schema': {
            'name': 'Government'
        }
    }
    ,{
        'class': 'Category',
        'id': str(uuid.uuid3(uuid.NAMESPACE_DNS, 'Business')),
        'schema': {
            'name': 'Business'
        }
    }
]
    
publications_nl = [
    {
        'class': 'Publication',
        'id': str(uuid.uuid3(uuid.NAMESPACE_DNS, 'dvhn')),
        'schema': {
            'name': 'Dagblad van het Noorden',
            'headquartersGeoLocation': {
                "latitude": 53.219065, 
                "longitude": 6.568008
            }
        }
    }
    ,{
        'class': 'Publication',
        'id': str(uuid.uuid3(uuid.NAMESPACE_DNS, 'nos')),
        'schema': {
            'name': 'NOS',
            'headquartersGeoLocation': {
                "latitude": 52.237869,
                "longitude": 5.174011
            }
        }
    }
    ,{
        'class': 'Publication',
        'id': str(uuid.uuid3(uuid.NAMESPACE_DNS, 'nu')),
        'schema': {
            'name': 'nu.nl',
            'headquartersGeoLocation': {
                "latitude": 52.3025,
                "longitude": 4.68889
            }
        }
    }
    ,{
        'class': 'Publication',
        'id': str(uuid.uuid3(uuid.NAMESPACE_DNS, 'ad')),
        'schema': {
            'name': 'Algemeen Dagblad',
            'headquartersGeoLocation': {
                "latitude": 51.9218362,
                "longitude": 4.4753684
            }
        }
    }
    ,{
        'class': 'Publication',
        'id': str(uuid.uuid3(uuid.NAMESPACE_DNS, 'nrc')),
        'schema': {
            'name': 'NRC',
            'headquartersGeoLocation': {
                "latitude": 52.37403,
                "longitude": 4.88969
            }
        }
    }
    ,{
        'class': 'Publication',
        'id': str(uuid.uuid3(uuid.NAMESPACE_DNS, 'telegraaf')),
        'schema': {
            'name': 'De Telegraaf',
            'headquartersGeoLocation': {
                "latitude": 52.3924369,
                "longitude": 4.8326266
            }
        }
    }
    ,{
        'class': 'Publication',
        'id': str(uuid.uuid3(uuid.NAMESPACE_DNS, 'fd')),
        'schema': {
            'name': 'Financieel Dagblad',
            'headquartersGeoLocation': {
                "latitude": 52.348873,
                "longitude": 4.916886
            }
        }
    }
    ,{
        'class': 'Publication',
        'id': str(uuid.uuid3(uuid.NAMESPACE_DNS, 'volkskrant')),
        'schema': {
            'name': 'De Volkskrant',
            'headquartersGeoLocation': {
                "latitude": 52.0812344,
                "longitude": 4.3150774
            }
        }
    }
    ,{
        'class': 'Publication',
        'id': str(uuid.uuid3(uuid.NAMESPACE_DNS, 'trouw')),
        'schema': {
            'name': 'De Trouw',
            'headquartersGeoLocation': {
                "latitude": 52.0812344, 
                "longitude": 4.3150774
            }
        }
    }
    ,{
        'class': 'Publication',
        'id': str(uuid.uuid3(uuid.NAMESPACE_DNS, 'rtl')),
        'schema': {
            'name': 'RTL Nieuws',
            'headquartersGeoLocation': {
                "latitude": 52.22333, 
                "longitude": 5.17639
            }
        }
    }
    ,{
        'class': 'Publication',
        'id': str(uuid.uuid3(uuid.NAMESPACE_DNS, 'elsevier')),
        'schema': {
            'name': 'Elsevier',
            'headquartersGeoLocation': {
                "latitude": 52.3933107,
                "longitude": 4.8371682
            }
        }
    }
    ,{
        'class': 'Publication',
        'id': str(uuid.uuid3(uuid.NAMESPACE_DNS, 'parool')),
        'schema': {
            'name': 'Het Parool',
            'headquartersGeoLocation': {
                "latitude": 52.0812344, 
                "longitude": 4.3150774
            }
        }
    }
    ,{
        'class': 'Publication',
        'id': str(uuid.uuid3(uuid.NAMESPACE_DNS, 'gelderlander')),
        'schema': {
            'name': 'De Gelderlander',
            'headquartersGeoLocation': {
                "latitude": 51.8474946,
                "longitude": 5.8637771}
        }
    }
    ,{
        'class': 'Publication',
        'id': str(uuid.uuid3(uuid.NAMESPACE_DNS, 'tweakers')),
        'schema': {
            'name': 'Tweakers',
            'headquartersGeoLocation': {
                "latitude": 52.35481643676758,
                "longitude": 4.876302242279053}
        }
    }
    ,{
        'class': 'Publication',
        'id': str(uuid.uuid3(uuid.NAMESPACE_DNS, 'metro')),
        'schema': {
            'name': 'Metro',
            'headquartersGeoLocation': {
                "latitude": 52.3924369,
                "longitude": 4.8326266}
        }
    }
]
for cat in categories:
    with open(f'./cache/categories/{cat["id"]}.json', 'w') as f:
        json.dump(cat, f)
        
for pub in publications:
    with open(f'./cache/publications/{pub["id"]}.json', 'w') as f:
        json.dump(pub, f)

for pub_nl in publications_nl:
    with open(f'./cache-nl/publications/{pub_nl["id"]}.json', 'w') as f:
        json.dump(pub_nl, f)