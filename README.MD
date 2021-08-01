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

## Running with GPU and compose (Debian)

```sh
# STEP 1
$ sudo apt install && \
sudo apt update && \
sudo apt install gcc make && \
BASE_URL=https://us.download.nvidia.com/tesla && \
DRIVER_VERSION=470.57.02 && \
curl -fSsl -O $BASE_URL/$DRIVER_VERSION/NVIDIA-Linux-x86_64-$DRIVER_VERSION.run && \
sudo sh NVIDIA-Linux-x86_64-$DRIVER_VERSION.run
```

```sh
# STEP 2 (installs both docker-compose and nvidia support for Docker)
$ sudo apt-get update && \
sudo apt-get -qq -y install \
    apt-transport-https \
    ca-certificates \
    curl \
    git \
    jq \
    software-properties-common && \
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add - && \
sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable" && \
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add - && \
distribution=$(. /etc/os-release;echo $ID$VERSION_ID) && \
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list && \
sudo apt-get update && \
sudo apt-get -qq -y install nvidia-container-runtime nvidia-docker2 docker-ce && \
sudo curl -L https://github.com/docker/compose/releases/download/1.29.2/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose && \
sudo chmod +x /usr/local/bin/docker-compose && \
sudo usermod -aG docker $USER && \
sudo docker run --rm --gpus all nvidia/cuda:11.0-base nvidia-smi && \
sudo sysctl -w vm.max_map_count=262144 && \
exit
```

You can validate if the GPUs are supported by running:

``` sh
$ docker run --rm --gpus all nvidia/cuda:11.0-base nvidia-smi
```
