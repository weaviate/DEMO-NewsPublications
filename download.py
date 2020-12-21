#!/usr/bin/env python3
import uuid as uuid_lib
import os
import json
import sys
from typing import Optional
import newspaper as news
from rfc3339 import rfc3339

NEWSPAPERS = {}
NEWSPAPERS['en'] = {
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

NEWSPAPERS['nl'] = {
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


def is_in_cache(
        uuid: str,
        cache_path: str
    ) -> bool:
    """
    Check if file in cache directory.

    Parameters
    ----------
    uuid : str
        Uuid of the file to check.
    cache_path : str
        Dirctory where to check fo the file.

    Returns
    -------
    bool
        True if file is in the directory, False otherwise.
    """

    if os.path.isfile(cache_path + str(uuid) + '.json'):
        return True
    return False

def save_to_cache(
        obj: dict,
        cache_path: str
    ) -> None:
    """
    Save newspaper object in a cache directory.

    Parameters
    ----------
    obj : dict
        Newspaper object as a dict.
    cache_path : str
        Path where to save the newspaper.
    """

    with open(cache_path + obj['id'] + '.json', 'x') as file_:
        file_.write(json.dumps(obj))
    if os.path.getsize(cache_path + obj['id'] + '.json') < 2000: # TODO: WHY 2000?
        os.remove(cache_path + obj['id'] + '.json')

def date_to_iso(
        article: news.Article
    ) -> Optional[str]:
    """
    Get article's data as a RFC3339 format string.

    Parameters
    ----------
    article : newspaper.Article
        Article for wich to get the data.

    Returns
    -------
    str
        RFC3339 formated data of ther article.
    """

    try:
        rfc3339_date = rfc3339(
            timestamp=article.publish_date,
            utc=True,
            use_system_timezone=False
        )
        return rfc3339_date
    except:
        return None


def build_actual_newspaper(
        lang: str,
        newspaper: str,
        cache_path: str
    ) -> None:
    """
    Download and save newspaper articles as weaviate schemas.

    Parameters
    ----------
    lang : str
        Language of the newspaper.
    newspaper : str
        Newspaper title.
    cache_path : str
        Cache directory path.
    """
    # Build the actual newspaper
    for article_raw in news.build(NEWSPAPERS[lang][newspaper], memoize_articles=False).articles:
        article_uuid = uuid_lib.uuid3(uuid_lib.NAMESPACE_DNS, article_raw.url)
        if not is_in_cache(article_uuid, cache_path):
            try:
                article = news.Article(article_raw.url)
                article.download()
                article.parse()
                article.nlp()
                if (article.meta_lang == lang or article.meta_lang is None) and \
                    article.title != '' and \
                    article.title is not None and \
                    article.summary != '' and \
                    article.summary is not None: # TODO: WHY article.meta_lag can be None too?

                    if lang == 'nl' and 'Puzzel' in article.title:
                        # TODO: Should it also skip it for English?
                        continue

                    # create the cache obj
                    cache_object = {
                        'id': str(article_uuid),
                        'title': article.title,
                        'url': article.url,
                        'summary': article.summary,
                        'paragraphs': article.text.split("\n\n"),
                        'authors': article.authors,
                        'keywords': article.keywords,
                        'pubDate': date_to_iso(article),
                        'publicationId': str(uuid_lib.uuid3(uuid_lib.NAMESPACE_DNS, newspaper))
                    }
                    # save to the cache
                    save_to_cache(cache_object, cache_path)
                    print("Downloaded: " + article.title)
            except Exception as exception:
                print("Something went wrong: ", exception)
        else:
            print(f"'{newspaper}' collected from cache")

def print_usage():
    """
    Print command-line interface description.
    """

    print("Usage: ./download.py <nl | en>  <'newspaper' | -a>")
    print("\t-a for all sources.")


if __name__ == "__main__":
    # Check number of arguments
    if len(sys.argv) != 3:
        print(f"ERROR, Wrong number of arguments, given {len(sys.argv) - 1}, must be 2!")
        print_usage()
        sys.exit(1)
    # Check language provided
    lang_ = sys.argv[1].lower()
    if lang_ not in ['en', 'nl']:
        print("ERROR, Demo does not support this language!")
        sys.exit(1)
    cache_path_ = f'./cache-{lang_}/'
    # which newspaper to load?
    if sys.argv[2] == '-a':
        for newspaper_ in NEWSPAPERS[lang_].keys():
            build_actual_newspaper(
                lang=lang_,
                newspaper=newspaper_,
                cache_path=cache_path_
            )

    elif sys.argv[2] in NEWSPAPERS[lang_]:
        build_actual_newspaper(
            lang=lang_,
            newspaper=sys.argv[2],
            cache_path=cache_path_
        )
    else:
        print("ERROR, Choose a newspaper!")
        print(json.dumps(NEWSPAPERS[lang_], indent=4))
        sys.exit(1)
