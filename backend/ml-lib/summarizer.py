'''
This code skeleton was taken from NicknochNack at https://github.com/nicknochnack/Longform-Summarization-with-Hugging-Face/blob/main/LongSummarization.ipynb
Utility for summarizing texts
Used on h1 and p tags

Useful for:
    - summarizing federal, local and state department information
    - summarizing news articles, blog posts, social media posts to get their main topic/areas of concern

Idea: The first sentence is used as the title. The rest is used as the body.
'''
from transformers import pipeline
from bs4 import BeautifulSoup
import requests
import random


def summarize(url, min_summary=50, max_summary=200):
    summarizer = pipeline('summarization')

    # examples
    SAMPLE_URLS = ['https://www.smh.com.au/national/australia-news-live-nsw-and-victorian-covid-19-cases-and-exposure-sites-grow-masks-back-on-in-melbourne-20210715-p589uh.html',
                   'https://www.nature.com/articles/d41586-021-01893-0']
    URL = 'https://www.nature.com/articles/d41586-021-01935-7'

    r = requests.get(url)

    soup = BeautifulSoup(r.text, 'html.parser')
    # returns all tags in order
    results = soup.find_all(['h1', 'p'])

    print("\n\n=======PRELIMINARY FETCHING=======\n\n")
    print(results)

    # ?: can also use newline \n?
    joiner = ' '
    full_text = joiner.join([result.text for result in results])

    # 2 ways -> split to sentences (chunks) and pre-process OR do it all in one go -> requires a lot of VRAM

    def break_into_chunks(text):
        # Method 1: break up to chunks
        def break_function(x, y): return x.replace(y, y+'<eos>')
        chars = ['.', '!', '?']
        for c in chars:
            text = break_function(text, c)

        return text.split('<eos>')

    full_text = break_into_chunks(full_text)

    # Idea -> send chunks in 500 words, if a chunk is over 500 words, break it up until they become less than 500 words each
    # split each sentence to individual words
    # put them back together in chunks of 500 wrods
    max_chunk = 500
    current_chunk = 0
    chunks = []

    for sentence in full_text:
        # if we are on the current chunk
        if len(chunks) == current_chunk + 1:
            # and we can still fit more words
            if len(chunks[current_chunk]) + len(sentence.split(' ')) <= max_chunk:
                chunks[current_chunk].extend(sentence.split(' '))
            else:
                current_chunk += 1
                chunks.append(sentence.split(' '))
        else:
            print(current_chunk)
            # append the entire sentene, broken up into words
            chunks.append(sentence.split(' '))

    for chunk_id in range(len(chunks)):
        chunks[chunk_id] = joiner.join(chunks[chunk_id])

    result = summarizer(chunks, max_length=max_summary,
                        min_length=min_summary, do_sample=False)

    print("\n\n=======SUMMARY=======\n\n")
    print(joiner.join([summary['summary_text'] for summary in result]))

    return result


def place_departments(raw_data):
    '''
    Place chunks of data based on their clustered types.
    Extension: Label the data with the most commonly occuring label, e.g. 'Federal', 'NSW', 'St. George'.

    Then send the data back in /federal, /state/{state}, /state/{state}/{local}.

    @raw_data - List of raw data, separated into FEDERAL -> STATEs in that order
    i.e. ['federal data...', 'nsw data...', 'vic data..']
    '''
    FEDERAL_DEPARTMENT_TYPES = ['AGRICULTURE', 'ENVIRONMENT', 'DEFENCE', 'EDUCATION', 'SKILLS', 'EMPLOYMENT',
                                'FINANCE', 'FOREIGN AFFAIRS', 'TRADE', 'HEALTH', 'HOME AFFAIRS', 'INDUSTRY', 'SCIENCE', 'ENERGY', 'RESOURCES', 'INFRASTRUCTURE TRANSPORT', 'SOCIAL']
    STATE_DEPARTMENT_TYPES = ['TRANSPORT', 'BUSINESS', 'CITY', 'COMMUNITY', 'ENVIRONMENT',
                              'CULTURE', 'FAIR TRADING', 'HEALTH', 'COUNCIL', 'LAND', 'LAW', 'WILDLIFE', 'LEISURE', 'WORK']
    LOCAL_DEPARTMENT_TYPES = ['FIRE', 'POLICE', 'EMERGENCY', 'LIBRARY', 'PUBLIC WORKS', 'SCHOOLS',
                              'PARKS RECREATION', 'ROADS', 'SANITATION', 'SAFETY', 'HOUSING', 'CEMETARY', 'COMMUNITY', 'ENVIRONMENT']

    # for each data point
    #   encode the data with word2vec
    #   run HDBSCAN to cluster all the text into corresponding department types
    #   for each cluster of words
    #       run summarizer to summarize the data
