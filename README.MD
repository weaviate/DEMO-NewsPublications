# Newspapers and Magazine // Weaviate

This demo shows how Weaviate can be used to explore magazines and newspapers.

_ARTICLES ARE USED FOR DEMO PURPOSES ONLY!_

_IF YOU WANT TO USE THIS DEMO, JUST RUN THE DOCKER FROM THE DOCS https://www.semi.technology/developers/weaviate/current/getting-started/example-datasets.html#news-publications_

## Installation (for collecting data) (ENGLISH and DUTCH)

Make sure to have Python3 and pip3 installed.

Only if you want to start with a fresh dataset (the cache folder is populated);

1. `$ rm ./cache-en/*.json` for English dataset and `$ rm ./cache-nl/*.json` for Dutch dataset
2. `$ python3 download.py <nl | en>  <'newspaper' | -a>`. The `-a` option is for all newspapers implemented. Below is the list of the available newspapers.

List of available newspapers.
1. English:
    - 'ft': 'https://www.ft.com'
    - 'nyt': 'https://www.theguardian.com/international'
    - 'guardian': 'https://www.nytimes.com'
    - 'wsj': 'https://www.wsj.com'
    - 'cnn': 'https://edition.cnn.com/'
    - 'fn': 'https://www.foxnews.com/'
    - 'econ': 'https://www.economist.com/'
    - 'newyorker': 'https://www.newyorker.com/'
    - 'wired': 'https://www.wired.com/'
    - 'vogue': 'https://www.vogue.com/'
    - 'gi': 'https://www.gameinformer.com/'
2. Dutch:
    - 'dvhn': 'https://www.dvhn.nl/'
    - 'nos': 'https://nos.nl/'
    - 'nu': 'https://nu.nl/'
    - 'ad': 'https://ad.nl/'
    - 'nrc': 'https://nrc.nl/'
    - 'telegraaf': 'https://www.telegraaf.nl/'
    - 'fd': 'https://fd.nl/'
    - 'volkskrant': 'https://volkskrant.nl/'
    - 'trouw': 'https://trouw.nl/'
    - 'rtl': 'https://www.rtlnieuws.nl/'
    - 'elsevier': 'https://www.ewmagazine.nl/'
    - 'parool': 'https://www.parool.nl/'
    - 'gelderlander': 'https://www.gelderlander.nl/'
    - 'tweakers': 'https://tweakers.net/nieuws/'
    - 'metro': 'https://www.metronieuws.nl/'

## Execute the import WITHOUT Docker

1. `$ pip3 install -r requirements.txt`
2. `$ python3 import.py <WEAVIATE_URL> <CACHE_DIR> [BATCH_SIZE]`
    - e.g.: `$ python3 import.py http://localhost:8080 cache-en 10`

## Execute the import WITH Docker (Weaviate with Docker Compose) 

0. Make sure you have Weaviate running (See [Install Weaviate with Docker Compose](https://www.semi.technology/developers/weaviate/current/getting-started/installation.html#docker-compose "Docker Compose")).
1. `$ export WEAVIATE_ID=$(echo ${PWD##*/}_weaviate_1 | tr "[:upper:]" "[:lower:]")`
2. `$ export WEAVIATE_ORIGIN="http://$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $WEAVIATE_ID):8080"`
3. `$ export WEAVIATE_NETWORK=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.NetworkID}}{{end}}' $WEAVIATE_ID)`
4. `$ docker run -i --network=$WEAVIATE_NETWORK -e weaviate_host=$WEAVIATE_ORIGIN -e cache_dir=<YOUR_CACHE_DIR> -e batch_size=<_YOUR_BATCH_SIZE> semitechnologies/weaviate-demo-newspublications:latest`

```
# in the same directory as the docker-compose.yaml
$ export WEAVIATE_ID=$(echo ${PWD##*/}_weaviate_1 | tr "[:upper:]" "[:lower:]")
$ export WEAVIATE_ORIGIN="http://$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $WEAVIATE_ID):8080"
$ export WEAVIATE_NETWORK=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.NetworkID}}{{end}}' $WEAVIATE_ID)
$ docker run -i --network=$WEAVIATE_NETWORK -e weaviate_host=$WEAVIATE_ORIGIN -e cache_dir=cache-nl -e batch_size=12 semitechnologies/weaviate-demo-newspublications
```

## Execute the import WITH Docker (Weaviate on external host or local WITHOUT Docker Compose) 

0. Make sure you have Weaviate running .
1. `$ eexport WEAVIATE_ORIGIN=WEAVIATE_ORIGIN`
4. `$ docker run -i -e weaviate_host=$WEAVIATE_ORIGIN -e cache_dir=<YOUR_CACHE_DIR> -e batch_size=<_YOUR_BATCH_SIZE> semitechnologies/weaviate-demo-newspublications:latest`

## Create Docker

1. `$ docker build . --tag="semitechnologies/weaviate-demo-newspublications:latest" --no-cache`
2. `$ docker push semitechnologies/weaviate-demo-newspublications:latest`

Default values for the envirionmental variables:
- **weaviate_host=http://localhost:8080**
- **cache_dir=cache-en**
- **batch_size=200**